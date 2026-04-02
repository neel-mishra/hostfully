# 📝 Meeting Summarizer & Action Protocol

## 1. Metadata Capture
* **Meeting Name:** {{MEETING_TITLE}}
* **Participants:** {{ATTENDEES}}
* **Date & Context:** {{DATE}} (e.g., Weekly Sync, Discovery Call, Board Prep.)

## 2. Executive Summary (bottom line)
* **One-Sentence Goal:** {{WHY_WE_MET}}
* **Key Outcome:** {{BIGGEST_TAKEAWAY}}
* **Sentiment Check:** {{TEAM_VIBE}} (e.g., Aligned, Pivoting, Concerned.)

## 3. Decision Log
* **[Decision 1]:** {{DECISION_MADE}} | **Rationale:** {{WHY_DECIDED}}
* **[Decision 2]:** {{DECISION_MADE}} | **Rationale:** {{WHY_DECIDED}}

## 4. The Action Matrix
| Action Item | Owner | Priority | Deadline | Linked File |
| :--- | :--- | :--- | :--- | :--- |
| {{TASK_1}} | {{NAME}} | {{P1/P2/P3}} | {{DATE}} | {{e.g. @prd_template.md}} |

## 5. Strategic Implications
* **Impact on Roadmap:** {{HOW_THIS_CHANGES_PLANS}}
* **Messaging Shift:** {{DOES_THIS_AFFECT_@brand_voice_matrix.md?}}

---
### 🤖 AI Agent Context Rule:
When processing a transcript, ignore small talk. Focus heavily on sentences starting with "We decided to," "The goal is," or "The problem is." If a task is assigned, cross-reference it against the **{{P1/P2/P3}}** priority definitions in `@business_context.md`.