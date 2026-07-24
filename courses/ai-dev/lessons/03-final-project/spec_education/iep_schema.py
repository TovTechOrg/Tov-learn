"""
iep_schema.py

IEP = Individualized Education Program (תוכנית חינוכית אישית) - a document used in special education in Israel.

Pydantic schema + validation logic for the Document Intelligence Service
(תח"י / ועדת שילוב extraction project).

IMPORTANT: Pydantic validates *structured data* (the JSON returned by Vertex AI's
Structured Output), not the raw PDF bytes themselves. The flow is:

    PDF file -> extract_text_from_pdf() -> [redaction] -> call_vertex_ai() -> raw JSON
             -> validate_extraction(raw JSON) -> IEPExtraction (validated) or ValidationError

This file gives you:
  1. The IEPExtraction schema (with field-level validators for the special-ed domain)
  2. extract_text_from_pdf() - pulls text out of an uploaded PDF (pypdf)
  3. call_vertex_ai() - a STUB. Replace the body with your real Vertex AI call.
     Left unimplemented here because this environment has no Vertex AI credentials/network.
  4. validate_pdf() - ties the whole pipeline together end to end
  5. A CLI entry point so you can run: python iep_schema.py path/to/document.pdf
"""

from __future__ import annotations

import json
import sys
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


# ---------------------------------------------------------------------------
# 1. Schema
# ---------------------------------------------------------------------------

class PlacementType(str, Enum):
    FULL_INCLUSION = "הכלה מלאה"
    PARTIAL_INCLUSION = "הכלה חלקית"
    SPECIAL_CLASS = 'כיתה מיוחדת בבי"ס רגיל'
    SEPARATE_SPECIAL_ED = "חינוך מיוחד נפרד"


class IEPExtraction(BaseModel):
    student_id: Optional[str] = Field(
        default=None,
        description="מזהה תלמיד פנימי בלבד (למשל STU-0001) — לעולם לא שם מלא",
    )
    school_year: str = Field(description='שנת לימודים, למשל תשפ"ז')
    disability_category: Optional[str] = Field(
        default=None, description="קטגוריית הליקוי כפי שמופיע במסמך"
    )
    placement_type: PlacementType = Field(description="סוג השיבוץ")
    weekly_support_hours: Optional[float] = Field(
        default=None, ge=0, le=40, description="שעות תמיכה שבועיות שהוקצו"
    )
    goals: list[str] = Field(default_factory=list, description="יעדים חינוכיים/טיפוליים")
    review_date: Optional[date] = Field(default=None, description="תאריך הוועדה/עדכון הבא")
    accommodations: list[str] = Field(default_factory=list, description="התאמות נדרשות")
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="ציון ביטחון בחילוץ, 0-1. שדה חובה — לעולם לא None, גם כשמסמך חלקי.",
    )

    @field_validator("student_id")
    @classmethod
    def reject_real_names(cls, v: Optional[str]) -> Optional[str]:
        """
        Guards against the redaction layer failing silently: if student_id looks
        like a real multi-word name instead of an internal ID, fail loudly here
        rather than let it reach the database.
        """
        if v and " " in v.strip() and not v.upper().startswith("STU"):
            raise ValueError(
                "student_id looks like a real name, not an internal ID — "
                "check that redaction ran before this document reached the model"
            )
        return v

    @field_validator("weekly_support_hours")
    @classmethod
    def zero_becomes_none(cls, v: Optional[float]) -> Optional[float]:
        # A model sometimes returns 0 instead of omitting the field - normalize it.
        return None if v == 0 else v


# ---------------------------------------------------------------------------
# 2. PDF text extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_and_redact(pdf_path: str):
    """
    PDF -> raw text -> redacted text, ready to send to an external AI provider.
    Returns the redaction.RedactionResult (redacted_text + local-audit-only matches).
    """
    from redaction import redact_text

    raw_text = extract_text_from_pdf(pdf_path)
    return redact_text(raw_text)


# ---------------------------------------------------------------------------
# 3. Vertex AI call - STUB, replace with the real implementation
# ---------------------------------------------------------------------------

def call_vertex_ai(redacted_document_text: str) -> dict:
    from google import genai
    import json

    client = genai.Client(
        vertexai=True,
        project="eternal-insight-501811-v4",
        location="us-central1",
    )

    prompt = f"""
חלץ מהמסמך הבא נתונים לפי הסכימה. אם שדה לא מופיע במסמך במפורש, החזר null
עבורו — אל תמציא ערך. שדה confidence הוא חובה (0-1), משקף עד כמה החילוץ הכולל
מלא ואמין.

מסמך:
{redacted_document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": IEPExtraction,
        },
    )
    return json.loads(response.text)

# ---------------------------------------------------------------------------
# 4. End-to-end validation
# ---------------------------------------------------------------------------

def validate_extraction(raw: dict) -> IEPExtraction:
    """Validate a raw JSON dict (already produced by Vertex AI) against the schema."""
    return IEPExtraction.model_validate(raw)


def validate_pdf(pdf_path: str) -> IEPExtraction:
    """Full pipeline: PDF -> text -> redact -> Vertex AI -> validated IEPExtraction."""
    redaction_result = extract_and_redact(pdf_path)
    raw = call_vertex_ai(redaction_result.redacted_text)
    return validate_extraction(raw)


# ---------------------------------------------------------------------------
# 5. CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python iep_schema.py path/to/document.pdf")
        sys.exit(1)

    try:
        result = validate_pdf(sys.argv[1])
        print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
    except ValidationError as e:
        print("Validation failed:")
        print(e)
        sys.exit(1)
    except NotImplementedError as e:
        print(e)
        sys.exit(1)