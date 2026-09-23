# AI-Assisted Ticketing System

A ticketing system with full CRUD, a status workflow, activity history,
and an AI chat interface that answers natural-language questions using
**live data from MySQL** — no hardcoded responses.

Built with Python, Streamlit (UI), MySQL (storage), and the Groq API
(AI chat, via tool/function calling).

See [`PLAN.md`](./PLAN.md) for the full architecture and design decisions,
and [`ai_chat_history/`](./ai_chat_history) for the AI-assisted development
process.

## Features

- Create and browse tickets (title, description, priority, assignee,
  timestamps)
- Status workflow: Open → In Progress → Blocked → Resolved
- Full activity history for every ticket — see exactly how it reached its
  current status
- AI chat that answers questions like:
  - "How many high-priority tickets are still open?"
  - "What is the status of ticket #104?"
  - "What is pending?"
  - "Which tickets are assigned to Rahul?"

## Tech Stack

- Python 3.x
- Streamlit (UI)
- MySQL (database)
- Groq API (`openai/gpt-oss-120b`) for AI chat, via tool calling
- pytest (automated tests)


## Setup

### 1. Prerequisites
- Python 3.9+
- MySQL Server running locally (or accessible remotely)
- A free Groq API key — sign up at [console.groq.com](https://console.groq.com)
  (no credit card required)

### 2. Clone and install dependencies

```bash
git clone <your-repo-url>
cd AI-Assisted-Ticketing-System
pip install -r requirements.txt
```

### 3. Set up the database

Log into MySQL and run:

```bash
mysql -u <your_mysql_user> -p < schema.sql
mysql -u <your_mysql_user> -p < data.sql
```

This creates the `ticketing_system` database with `users`, `tickets`, and
`ticket_history` tables, and seeds a few sample users.

### 4. Configure environment variables

Create a `.env` file in the project root:DB_HOST=localhost
DB_PORT=3306
DB_USER=<your_mysql_user>
DB_PASSWORD=<your_mysql_password>
DB_NAME=ticketing_system

GROQ_API_KEY=<your_groq_api_key>

### 5. Run the app

```bash
streamlit run home.py
```

This opens the dashboard in your browser. Use the sidebar to navigate to
"Create Ticket," "Ticket Detail," and "AI Chat."

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests run against your real MySQL database. Test tickets are created and
automatically cleaned up afterward — your actual ticket data is untouched.

## AI Chat: How It Works

The AI chat does **not** generate SQL or query the database directly.
Instead, it's given four fixed tools (Python functions in `ai_chat.py`):

1. `count_tickets(status, priority)`
2. `get_ticket_by_id(ticket_id)`
3. `get_tickets_by_assignee(name)`
4. `get_pending_tickets()`

For each question, the Groq model (`openai/gpt-oss-120b`) decides which
tool to call and with what arguments. The tool runs a real, parameterized
SQL query against MySQL, and the result is sent back to the model, which
phrases the final answer. If a question doesn't match any of the four
tools, the assistant says so rather than guessing.

Every tool call and final answer is printed to the terminal running
Streamlit, for debugging and verification. See
[`docs/ai_chat_verification.md`](./docs/ai_chat_verification.md) for a
worked example against the assignment's sample questions.

## Notes

- No user authentication — this is out of scope for the assignment.
  "Changed by" on status updates is a free-text field.
- The AI chat's scope is intentionally limited to the four tools above,
  per the project plan — this keeps answers grounded in real data rather
  than risking free-form SQL generation.
