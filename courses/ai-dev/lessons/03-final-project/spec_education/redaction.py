"""
redaction.py

PII (Personally Identifiable Information) redaction layer for the Document Intelligence Service.

MUST run on document text BEFORE that text is sent to Vertex AI (an external,
third-party provider) — see SPEC.md, "דרישות אבטחה ופרטיות".

This is a rule-based (regex + heuristics) redactor, not a full NER model.
That's a deliberate, documented trade-off for a course-project scope — see the
"Known limitations" section at the bottom of this file. It is combined with
the `student_id` validator in iep_schema.py as defense-in-depth: even if a
real name slips past this layer and the model echoes it back as `student_id`,
that validator rejects it before it reaches the database.

IMPORTANT: `RedactionResult.matches` contains the ORIGINAL sensitive values
(for local audit logging only, e.g. "we redacted 1 ID number and 2 names").
Never send `matches` anywhere external, never persist it next to the document,
and never pass it to call_vertex_ai().
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Israeli national ID: 9 digits, optionally spaced/dashed, often preceded by ת.ז / תעודת זהות
ISRAELI_ID_CONTEXT_RE = re.compile(
    r'(ת\.?\s*ז\.?|תעודת\s+זהות)\s*[:\-]?\s*(\d[\d\-\s]{7,10}\d)'
)
BARE_9_DIGIT_RE = re.compile(r'(?<!\d)(\d{9})(?!\d)')

PHONE_RE = re.compile(
    r'(?<!\d)(0(?:5\d|[23489]|7\d)[\-\s]?\d{3}[\-\s]?\d{4})(?!\d)'
)

EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')

# Labeled-name patterns: "שם התלמיד/ה: X Y", "שם ההורה: X Y", etc.
NAME_LABEL_RE = re.compile(
    r'(שם\s+ה?(?:תלמיד|הורה|מורה|יועצת|יועץ|מחנך|מחנכת|נציג|נציגת)(?:/ה)?\s*[:\-]?\s*)'
    r'([\u05D0-\u05EA]+(?:\s+[\u05D0-\u05EA]{2,})?)'
)

# Common Hebrew first names (extend as needed) - used to catch unlabeled
# "First Last" mentions in free text. Deliberately conservative (first-name
# gated) to avoid over-redacting ordinary Hebrew nouns.
COMMON_FIRST_NAMES = {
    "נועם", "איתי", "יעל", "מאיה", "דניאל", "אביגיל", "עומר", "שירה",
    "ליאור", "רותם", "תומר", "הדר", "יהונתן", "נועה", "אריאל", "עדן",
    "יוסי", "משה", "דוד", "שרה", "רחל", "מרים", "אברהם", "יצחק", "רבקה",
}
_names_pattern = "|".join(sorted(COMMON_FIRST_NAMES, key=len, reverse=True))
FREE_NAME_RE = re.compile(
    rf'(?:{_names_pattern})\s+[\u05D0-\u05EA]{{2,}}'
)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class RedactionMatch:
    kind: str          # "israeli_id" | "phone" | "email" | "labeled_name" | "free_name"
    original: str       # the sensitive value found - LOCAL AUDIT USE ONLY


@dataclass
class RedactionResult:
    redacted_text: str
    matches: list[RedactionMatch] = field(default_factory=list)

    def summary(self) -> str:
        """Safe to log: counts only, never the actual values."""
        counts: dict[str, int] = {}
        for m in self.matches:
            counts[m.kind] = counts.get(m.kind, 0) + 1
        return ", ".join(f"{k}={v}" for k, v in counts.items()) or "no PII detected"


# ---------------------------------------------------------------------------
# Israeli ID checksum (Luhn-like) — used to avoid false positives on bare 9-digit numbers
# ---------------------------------------------------------------------------

def _is_valid_israeli_id(digits: str) -> bool:
    digits = digits.strip()
    if len(digits) != 9 or not digits.isdigit():
        return False
    total = 0
    for i, ch in enumerate(digits):
        d = int(ch) * (1 if i % 2 == 0 else 2)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def redact_text(text: str) -> RedactionResult:
    matches: list[RedactionMatch] = []
    out = text

    def _sub(pattern: re.Pattern, kind: str, placeholder: str, group: int = 0):
        nonlocal out
        def repl(m: re.Match) -> str:
            matches.append(RedactionMatch(kind=kind, original=m.group(group)))
            if group == 0:
                return placeholder
            return m.group(0).replace(m.group(group), placeholder)
        out = pattern.sub(repl, out)

    # Order matters: labeled names first (more specific), then IDs/phones/emails,
    # then unlabeled free-text names last (most heuristic / highest false-positive risk).
    _sub(NAME_LABEL_RE, "labeled_name", "[REDACTED_NAME]", group=2)

    def id_context_repl(m: re.Match) -> str:
        matches.append(RedactionMatch(kind="israeli_id", original=m.group(2)))
        return f"{m.group(1)} [REDACTED_ID]"
    out = ISRAELI_ID_CONTEXT_RE.sub(id_context_repl, out)

    def bare_id_repl(m: re.Match) -> str:
        if _is_valid_israeli_id(m.group(1)):
            matches.append(RedactionMatch(kind="israeli_id", original=m.group(1)))
            return "[REDACTED_ID]"
        return m.group(0)  # not a valid ID checksum -> leave alone (likely e.g. a school symbol)
    out = BARE_9_DIGIT_RE.sub(bare_id_repl, out)

    _sub(PHONE_RE, "phone", "[REDACTED_PHONE]", group=1)
    _sub(EMAIL_RE, "email", "[REDACTED_EMAIL]", group=0)
    _sub(FREE_NAME_RE, "free_name", "[REDACTED_NAME]", group=0)

    return RedactionResult(redacted_text=out, matches=matches)


# ---------------------------------------------------------------------------
# Known limitations (documented deliberately, for SPEC.md / demo talking points)
# ---------------------------------------------------------------------------
# 1. Name detection is heuristic (labeled context + a fixed first-name list),
#    not a trained NER model. Institution names (e.g. "כנפי רוח") and generic
#    Hebrew nouns are NOT in the first-name list, so they should NOT trigger
#    false positives — but an uncommon real first name not in the list could
#    slip through free-text redaction (labeled redaction still catches it if
#    it follows "שם התלמיד:" etc).
# 2. School institution symbols (7-8 digit codes) are NOT redacted — they are
#    public, institution-level identifiers, not personal data.
# 3. This module has no false-negative guarantee. It is one layer of a
#    defense-in-depth design; the `student_id` validator in iep_schema.py is
#    the second layer, catching leaked real names in the model's *output*.
# 4. Production upgrade path: swap in a Hebrew NER model (e.g. via Presidio +
#    a Hebrew spaCy/transformers pipeline) behind the same redact_text()
#    interface, without changing any calling code.


if __name__ == "__main__":
    sample = (
        "שם התלמיד/ה: נועם כהן, ת.ז. 123456782. "
        "ניתן ליצור קשר עם ההורים בטלפון 050-1234567 או במייל parent@example.com. "
        "התלמיד איתי לוי נמצא באותה כיתה. מספר סמל מוסד: 440495."
    )
    result = redact_text(sample)
    print("--- Redacted text ---")
    print(result.redacted_text)
    print("\n--- Audit summary (safe to log) ---")
    print(result.summary())