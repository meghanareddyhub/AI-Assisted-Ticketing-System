import json
from groq import Groq
from db import get_connection
from config import GROQ_API_KEY
import tickets

client = Groq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"


# ---------- Tool functions (same logic as before) ----------

def count_tickets(status=None, priority=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM tickets WHERE 1=1"
    params = []

    if status:
        query += " AND status = %s"
        params.append(status)
    if priority:
        query += " AND priority = %s"
        params.append(priority)

    cursor.execute(query, tuple(params))
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return count


def get_ticket_by_id(ticket_id):
    return tickets.get_ticket_by_id(ticket_id)


def get_tickets_by_assignee(name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            tickets.id, tickets.title, tickets.priority, tickets.status,
            users.name AS assignee, tickets.created_at, tickets.updated_at
        FROM tickets
        JOIN users ON tickets.assignee_id = users.id
        WHERE LOWER(users.name) = LOWER(%s)
        ORDER BY tickets.created_at DESC
    """
    cursor.execute(query, (name,))
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result


def get_pending_tickets():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            tickets.id, tickets.title, tickets.priority, tickets.status,
            users.name AS assignee, tickets.created_at, tickets.updated_at
        FROM tickets
        LEFT JOIN users ON tickets.assignee_id = users.id
        WHERE tickets.status IN ('Open', 'In Progress')
        ORDER BY tickets.created_at DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result


# ---------- LLM tool-calling wiring ----------

SYSTEM_PROMPT = """You are a helpful assistant answering questions about a ticketing system.
You must ONLY answer using data returned by the tools provided to you — never invent ticket
numbers, counts, statuses, or names. If a question cannot be answered with the available
tools, say so clearly instead of guessing."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "count_tickets",
            "description": "Count tickets, optionally filtered by status and/or priority.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": list(tickets.VALID_STATUSES)},
                    "priority": {"type": "string", "enum": list(tickets.VALID_PRIORITIES)},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_by_id",
            "description": "Get full details of a single ticket by its numeric ID.",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "integer"}},
                "required": ["ticket_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tickets_by_assignee",
            "description": "Get all tickets assigned to a specific person by name.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pending_tickets",
            "description": "Get all tickets that are still pending (status Open or In Progress).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def call_tool(name, args):
    if name == "count_tickets":
        return count_tickets(status=args.get("status"), priority=args.get("priority"))
    elif name == "get_ticket_by_id":
        return get_ticket_by_id(args["ticket_id"])
    elif name == "get_tickets_by_assignee":
        return get_tickets_by_assignee(args["name"])
    elif name == "get_pending_tickets":
        return get_pending_tickets()
    else:
        raise ValueError(f"Unknown tool requested: {name}")


def answer_question(question, log=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    )
    message = response.choices[0].message

    while message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            try:
                result = call_tool(name, args)
            except Exception as e:
                result = f"Error: {e}"

            if log:
                print(f"[AI CHAT] tool={name} args={args} -> {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

    answer = message.content or ""

    if log:
        print(f"[AI CHAT] Q: {question!r} -> A: {answer!r}")

    return answer