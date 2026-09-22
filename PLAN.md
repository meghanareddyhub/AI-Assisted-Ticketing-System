# PLAN.md — AI-Assisted Ticketing System

## 1. Overview
A ticketing system with full CRUD, a status workflow, activity history, and
an AI chat interface that answers natural-language questions using live data
from the MySQL database. Built with Python, Streamlit (UI), MySQL (storage),
and an LLM API (chat, via function/tool calling).

## 2. Tech Stack
- Language: Python 3.x
- UI: Streamlit (multipage app)
- Database: MySQL
- AI: LLM API using tool/function calling only
- Version control: Git/GitHub

No other frameworks (no Flask/Django, no custom frontend, no text-to-SQL
layer) unless a real limitation is hit during development.

## 3. Architecture
Streamlit UI → Python service modules (tickets.py, history.py, ai_chat.py) →
MySQL. The LLM never queries MySQL directly. It is given a small, fixed set
of Python "tools" (functions). For each user question, the LLM selects a
tool and arguments, Python executes the real parameterized SQL query, and
the LLM turns the returned data into a natural-language answer. There is no
fallback query path — if a question doesn't map to a defined tool, the AI
says so rather than guessing or generating ad hoc SQL.

## 4. Database Schema

### users
- id (PK), name

### tickets
- id (PK), title, description, priority (Low/Medium/High/Critical),
  status (Open/In Progress/Blocked/Resolved), assignee_id (FK -> users),
  created_at, updated_at

### ticket_history
- id (PK), ticket_id (FK -> tickets), field_changed, old_value, new_value,
  changed_by, note, changed_at

Relationships: users 1—N tickets (assignee); tickets 1—N ticket_history.
Every ticket create/update writes a corresponding history row.

### chat_log (optional — implement only if needed for verification evidence)
- id (PK), question, tool_used, tool_args, tool_result_summary, answer,
  created_at

This table is a purely optional runtime feature (e.g. a "recent questions"
view, or persisted evidence for grading). It is not required to satisfy the
assignment and is entirely separate from the `ai_chat_history/` development
documentation folder described in Section 9. Build it only if it turns out
to be genuinely useful or explicitly needed.

## 5. Features & Scope
1. Create ticket (title, description, priority, assignee)
2. Dashboard: list/filter/sort tickets by status, priority, assignee
3. Ticket detail view: full info + history timeline
4. Status workflow: Open -> In Progress -> Blocked -> Resolved (validated
   transitions)
5. Activity history: auto-logged on every field change
6. AI chat: answers questions using live DB data via a fixed set of tools
   only. In scope:
   - Count tickets by status and/or priority
   - Get ticket by ID
   - Get tickets by assignee
   - Get pending tickets (Open + In Progress)
   Anything outside this set gets a clear "I can't answer that yet" response
   rather than an invented or hardcoded one.

## 6. Streamlit Pages
- Home.py — Dashboard
- pages/1_Create_Ticket.py — New ticket form
- pages/2_Ticket_Detail.py — Detail + status change + history
- pages/3_AI_Chat.py — Chat interface

## 7. Python Modules
- db.py — MySQL connection + query helpers
- tickets.py — ticket CRUD + status transition logic
- history.py — history logging/reading
- ai_chat.py — tool definitions, tool-calling loop, LLM API integration
- config.py — environment/config loading
- schema.sql / seed_data.sql

## 8. AI Chat Design (Tool-Calling Only)
- Tools (Python functions, each running one parameterized, read-only query):
  1. `count_tickets(status=None, priority=None)`
  2. `get_ticket_by_id(ticket_id)`
  3. `get_tickets_by_assignee(name)`
  4. `get_pending_tickets()` (Open + In Progress)
- Flow: user question -> LLM picks a tool + arguments -> Python runs the
  real SQL -> raw result returned to the LLM -> LLM phrases the final
  natural-language answer. No text-to-SQL, no free-form query generation.
- If the LLM cannot map a question to one of the four tools, the app returns
  a fixed "not supported yet" style message instead of a guessed answer.
- Every chat interaction (question, tool called, arguments, raw result,
  final answer) should be logged in-memory/console at minimum for
  demoing/debugging; persisting it in `chat_log` is optional (Section 4).

## 9. Development Documentation Strategy
- `ai_chat_history/` folder: relevant AI-assisted development conversations
  organized by major feature, including prompts, useful AI responses,
  implementation decisions, and debugging interactions. This is
  documentation of *how the app was built*, not a runtime feature, and is
  never used as application chat storage.
- README.md: setup steps, run instructions, architecture summary, demo
  notes.
- docs/ or screenshots/: test evidence, verification screenshots.

## 10. Testing Strategy
- pytest unit tests for ticket creation, status transitions, history
  logging.
- Fixed test set covering the four supported AI-chat question types, plus
  edge cases (nonexistent ticket ID, no tickets matching a filter, an
  out-of-scope question) with expected vs. actual answers recorded.
- Manual end-to-end QA checklist: create -> list -> update status -> check
  history -> ask AI chat -> verify answer matches DB.

## 11. Git Strategy
PLAN.md is committed first, before any implementation work begins:
1. `docs: add PLAN.md`
2. `chore: initial repo structure + requirements.txt`
3. `feat: MySQL schema (tickets, ticket_history, users)`
4. `feat: db.py connection layer`
5. `feat: ticket creation + listing`
6. `feat: dashboard page with filters`
7. `feat: ticket detail page + status workflow`
8. `feat: activity history logging`
9. `feat: AI chat tools (count/get-by-id/get-by-assignee/pending)`
10. `feat: AI chat Streamlit UI`
11. `test: unit tests for ticket logic + AI chat tool tests`
12. `docs: ai_chat_history logs + README`
13. `fix/chore` commits as needed during debugging
14. `feat: optional chat_log table` (only if implemented)

## 12. Milestones
1. PLAN.md + repo scaffold (no app code yet)
2. Schema + DB layer + ticket CRUD (tested via script/pytest, no UI yet)
3. Streamlit dashboard + create/detail pages
4. Status workflow + history logging wired to UI
5. AI chat: four tool functions, tested directly against MySQL
6. AI chat: LLM tool-calling integration + Streamlit chat UI
7. Testing pass + documentation + README + final commit
8. (Optional) chat_log persistence, only if needed