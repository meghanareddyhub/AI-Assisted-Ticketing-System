import ai_chat
import tickets


def test_count_tickets_returns_nonnegative_int():
    count = ai_chat.count_tickets()
    assert isinstance(count, int)
    assert count >= 0


def test_count_tickets_with_status_filter_le_total():
    total = ai_chat.count_tickets()
    open_count = ai_chat.count_tickets(status="Open")
    assert open_count <= total


def test_get_ticket_by_id_tool_matches_tickets_module(new_ticket):
    direct = tickets.get_ticket_by_id(new_ticket)
    via_tool = ai_chat.get_ticket_by_id(new_ticket)
    assert direct == via_tool


def test_get_tickets_by_assignee_case_insensitive():
    # Assumes 'Rahul' exists in the users table (from data.sql seed)
    upper = ai_chat.get_tickets_by_assignee("RAHUL")
    lower = ai_chat.get_tickets_by_assignee("rahul")
    assert upper == lower


def test_get_pending_tickets_only_open_or_in_progress():
    pending = ai_chat.get_pending_tickets()
    for t in pending:
        assert t["status"] in ("Open", "In Progress")