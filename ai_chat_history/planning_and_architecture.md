# Feature: Planning & Architecture (PLAN.md)

## Prompt
Asked the AI to analyze the assignment (ticketing system + AI chat) and
produce a development plan and architecture for a Python + Streamlit +
MySQL + LLM API stack, explicitly avoiding Django/Flask/React and
from-scratch frontend work, before any implementation.

## Key AI output
- Proposed a 3-layer architecture: Streamlit UI -> Python service modules
  (tickets.py, history.py, ai_chat.py) -> MySQL, with the LLM never
  querying MySQL directly.
- Proposed schema: users, tickets, ticket_history (with relationships).
- Proposed AI chat via LLM tool/function-calling as the primary approach,
  with text-to-SQL only as a fallback.

## Decisions made (revisions requested)
- Restricted AI chat to tool-calling only (Approach A) — dropped the
  text-to-SQL fallback entirely unless proven necessary later.
- Scoped AI chat to four specific tools: count tickets by status/priority,
  get ticket by ID, get tickets by assignee, get pending tickets.
- Clarified that `ai_chat_history/` documents development, not runtime
  chat storage; a separate optional `chat_log` table would handle runtime
  logging if ever needed.
- Reordered Git strategy so PLAN.md is committed before any implementation.

## Outcome
Finalized PLAN.md (see project root) incorporating all of the above.