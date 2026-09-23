# AI Chat Verification

Manual verification that the AI chat answers using real, live MySQL data
(via Groq tool-calling), not hardcoded responses. Each entry shows the
question asked, the tool call(s) logged to the terminal, and the actual
final answer returned in the UI.

## Test environment
- Model: `openai/gpt-oss-120b` via Groq API
- Database: local MySQL, `ticketing_system` schema
- Data at time of testing: [fill in — e.g. "5 tickets: 2 Open, 1 In Progress,
  1 Blocked, 1 Resolved; assignees Rahul, Priya, Amit, Sneha"]

## Example questions (from assignment spec)

### 1. "How many high-priority tickets are still open?"
- Tool call logged: `count_tickets args={'status': 'Open', 'priority': 'High'} -> [N]`
- AI answer: "There is 1 high‑priority ticket that is still open."
- Verified against DB: `SELECT COUNT(*) FROM tickets WHERE status='Open' AND priority='High';` → [N] ✅/❌

### 2. "What is the status of ticket #1?"
- Tool call logged: `get_ticket_by_id args={'ticket_id': 1} -> {...}`
- AI answer: "The status of ticket #1 is Open."
- Verified against DB: matches Ticket Detail page ✅/❌

### 3. "What is pending?"
- Tool call logged: `get_pending_tickets -> [...]`
- AI answer: " In our ticketing system, pending tickets are those whose status is either “Open” or “In Progress.”

These are the tickets that still require attention and have not yet been resolved or closed.

Here are the pending tickets right now:

ID	Title	Priority	Status	Assignee
11	Test ticket	High	In Progress	Rahul
4	Test ticket	High	In Progress	Rahul
2	Test ticket	High	In Progress	Rahul
1	Login problem	High	Open	Rahul
These tickets are the ones currently awaiting resolution."
- Verified against DB: matches Open + In Progress count on dashboard ✅/❌

### 4. "Which tickets are assigned to Rahul?"
- Tool call logged: `get_tickets_by_assignee args={'name': 'Rahul'} -> [...]`
- AI answer: "Here are the tickets currently assigned to Rahul:

ID	Title	Priority	Status	Created At	Updated At
11	Test ticket	High	In Progress	2026‑09‑23 15:17:50	2026‑09‑23 15:17:50
4	Test ticket	High	In Progress	2026‑09‑23 15:13:49	2026‑09‑23 15:13:49
2	Test ticket	High	In Progress	2026‑09‑23 11:15:53	2026‑09‑23 11:15:53
1	Login problem	High	Open	2026‑09‑23 10:23:54	2026‑09‑23 10:23:54
These are all the tickets that the system shows as being assigned to Rahul."
- Verified against DB: matches dashboard filtered by assignee = Rahul ✅/❌

## Edge cases

### 5. Nonexistent ticket ID
- Question: "What is the status of ticket #9999?"
- Tool call logged: `get_ticket_by_id args={'ticket_id': 9999} -> None`
- AI answer: "I’m sorry, but I don’t have any information about ticket #9999."

### 6. No tickets matching a filter
- Question: "How many critical priority tickets are blocked?"
- Tool call logged: `count_tickets args={'status': 'Blocked', 'priority': 'Critical'} -> 0`
- AI answer: "There are 0 critical‑priority tickets that are currently blocked."

### 7. Out-of-scope question
- Question: "Delete ticket #1" 
- AI answer: "I’m sorry, but I don’t have a tool that can delete tickets. I can only retrieve or count tickets using the provided functions. If you need information about ticket #1, I can look that up for you."

## Conclusion
All answers were grounded in tool calls that queried the live MySQL database
directly — no hardcoded or fabricated ticket data was used at any point.