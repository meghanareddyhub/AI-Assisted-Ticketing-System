# Feature: Ticket CRUD & Activity History

## Starting point
Had working `create_ticket()` and `get_all_tickets()` in tickets.py, plus
schema.sql, db.py, config.py already implemented and manually tested
(ticket creation confirmed via console output).

## Prompt
Asked the AI to review the current implementation against PLAN.md, report
completed vs incomplete work, and continue with the next logical step
without restarting or duplicating existing work.

## Key AI output
- Identified that no history logging existed yet — a gap against the
  "understand how a ticket reached its current status" requirement.
- Added `history.py` (`log_change`, `get_history`).
- Extended `tickets.py` with `get_ticket_by_id()` and `update_status()`,
  the latter validating against the four allowed statuses and logging
  every transition.
- Updated `create_ticket()` to log its own initial history entry, so every
  ticket's timeline starts from creation.

## Verification
Wrote and ran a manual test script confirming: ticket creation, status
update, and two ordered history entries (creation + update) all worked
correctly against the real MySQL database.

## Outcome
Backend CRUD + history complete and verified before any UI work began.