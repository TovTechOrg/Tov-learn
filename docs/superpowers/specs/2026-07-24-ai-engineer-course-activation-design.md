# AI Engineer Course — Activation & Content Completion

**Date:** 2026-07-24
**Status:** Approved (design), pending implementation plan

## Motivation

The learner enrolled in a course whose live syllabus (`ai-engineer.pages.dev/courses/ai-engineer/syllabus`) is a full 7-module, 46-lesson, 160-hour "AI Engineer" curriculum (Edition 2.0, March 2026). Locally, this course exists only as an incomplete archive at `courses/_archive/ai-engineer/` (modules 00, 01, 03, 05 — 26 lessons), while the repo's active default course is the smaller "AI Dev" (18 lessons, 4 modules). The learner wants AI Engineer restored to active status as the new default, with the missing modules built out to match the syllabus, while keeping AI Dev available as a second option.

Fetched syllabus reference (module → hours → lesson count):
- 00 AI Foundations + Prompt Engineering — 8h — 3 lessons (0.1–0.3) — **exists**
- 01 Business Automation — 26h — 9 lessons (1.1–1.9) — **exists**
- 02 Chatbots and AI Agents — 28h — 8 lessons (2.1–2.8) — **missing**
- 03 Vibe Coding—AI-Powered App Development — 26h — 8 lessons (3.1–3.8) — **exists**
- 04 Visual and Audio Content with AI — 18h — 6 lessons (4.1–4.6) — **missing**
- 05 APIs and Technical Integration — 20h — 6 lessons (5.1–5.6) — **exists**
- 06 AI for Marketing, Sales, and Freelancing — 14h — 5 lessons (6.1–6.5) — **missing**
- 07 Capstone Project — 20h — 1 project — **missing**

Existing local module numbering/lesson counts for 00, 01, 03, 05 already match the fetched syllabus exactly — no renumbering needed there.

## Section 1 — Structural migration

1. `git mv courses/_archive/ai-engineer courses/ai-engineer` (preserve history; it's no longer archived).
2. `courses/ai-engineer/COURSE.md`:
   - Remove the "בארכיון" banner.
   - `course.path` → `courses/ai-engineer/lessons`.
   - Extend the module table with rows for 02, 04, 06, 07.
3. Root `CLAUDE.md` course table:
   - AI Engineer row → `courses/ai-engineer/`, `courses/ai-engineer/lessons`, status `פעיל (ברירת מחדל)`.
   - AI Dev row → status `פעיל (אפשרות שנייה)`.
   - Drop the "בארכיון" row entirely (only two rows remain).
4. `.claude/commands/learn/setup.md`: swap which course is presented/pre-selected first during course selection.
5. Sweep `.claude/commands/learn/*.md` (resume.md, teaching.md, others) for hardcoded assumptions that AI Dev is the sole/default course, and update to reflect AI Engineer as default.

## Section 2 — Content conventions & new lesson list

File pair per lesson (matches existing convention exactly — no `solutions.md`, that's learner-generated during teaching, not course content):

- **`X.Y_script.txt`** — Hebrew narration (English tech terms kept in English), split into slides via `[מעבר שקף]` markers. Each paragraph opens with a TTS emotion tag (`[warm]`, `[calm]`, `[calm, confident]`, `[clear]`, etc.). Includes a hook, framing/discussion questions for the learner, concrete numbers, and references to real or plausible 2026-era tools/companies, matching the tone of existing lessons.
- **`X.Y_exercises.md`** — wrapped in `<div dir="rtl" lang="he">`; header block with lesson number/name/type/duration; numbered exercises with scenarios, tables, and submission format; closing weighted evaluation-criteria table.

New lessons to write (module → lesson → hours → type, per fetched syllabus):

**Module 02 — Chatbots and AI Agents (28h)**
| # | Lesson | Hours | Type |
|---|--------|-------|------|
| 2.1 | AI Agents vs. standard chatbots | 2 | theoretical |
| 2.2 | WhatsApp chatbot with ManyChat | 4 | practical |
| 2.3 | Telegram bot with Python | 4 | practical |
| 2.4 | AI Agent creation with Make.com | 4 | practical |
| 2.5 | OpenAI/Anthropic APIs — Assistants, Tool Use | 4 | practical |
| 2.6 | n8n AI Agent | 2 | practical |
| 2.7 | RAG implementation | 2 | practical |
| 2.8 | Complex/Multi-Agent systems | 4 | practical |

**Module 04 — Visual and Audio Content with AI (18h)**
| # | Lesson | Hours | Type |
|---|--------|-------|------|
| 4.1 | Image generation | 4 | practical |
| 4.2 | Logos/branding/product images | 2 | practical |
| 4.3 | Video creation | 4 | practical |
| 4.4 | Speaking avatars | 2 | practical |
| 4.5 | Voice cloning & Hebrew TTS | 2 | practical |
| 4.6 | Marketing/corporate videos end-to-end | 4 | practical |

**Module 06 — AI for Marketing, Sales, and Freelancing (14h)**
| # | Lesson | Hours | Type |
|---|--------|-------|------|
| 6.1 | Marketing content creation | 2 | practical |
| 6.2 | AI Scraping Pipeline | 4 | practical |
| 6.3 | Automated lead generation | 2 | practical |
| 6.4 | Data analysis, dashboards, ROI | 2 | practical |
| 6.5 | Selling automation services as a freelancer | 4 | practical |

**Module 07 — Capstone (20h)**: one project brief document (mirrors `courses/ai-dev/lessons/03-final-project/spec_education`'s shape), listing the 7 project options from the syllabus (business automation system, e2e business AI agent, full SaaS app, lead-gen machine, visual+audio pipeline, multi-platform bot with RAG, HR/recruiting system) and submission requirements (documentation, working demo, 10-minute presentation, ROI/cost analysis).

**Consistency fix:** `0.1_script.txt`'s course-overview slide currently narrates the old 8-module breakdown (24/28/28/16/20/12/20h = 156h total) which predates modules 02/04/06/07 existing at all. Update it to narrate all 8 modules with the new hours (8+26+28+26+18+20+14+20 = 160h), matching the real structure being built.

## Execution plan

Decomposed into 5 independent implementation cycles, each with its own plan:
1. **Structural migration** (Section 1) — small, done first, unblocks everything else.
2. **Module 02 content** — 8 lessons.
3. **Module 04 content** — 6 lessons.
4. **Module 06 content** — 5 lessons.
5. **Module 07 capstone brief** — 1 document.

Per the learner's preference, modules are done **one at a time with a checkpoint in between** (review the module before moving to the next), rather than all 20 lessons in one pass. Within a module, individual lessons are independent of each other and can be written in parallel (e.g. via the Agent tool), then reviewed together as a batch.

## Out of scope

- Rewriting existing modules 00/01/03/05 content (only the 0.1 overview-numbers fix above).
- Changing AI Dev's content or status beyond the CLAUDE.md table wording.
- Any change to the archived `ai-engineer` course being anything other than moved (no other archived courses exist to consider).
