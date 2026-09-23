import pytest
import tickets
import history


def test_create_ticket_starts_open(new_ticket):
    ticket = tickets.get_ticket_by_id(new_ticket)
    assert ticket is not None
    assert ticket["status"] == "Open"
    assert ticket["title"] == "Pytest test ticket"


def test_create_ticket_logs_initial_history(new_ticket):
    entries = history.get_history(new_ticket)
    assert len(entries) == 1
    assert entries[0]["new_value"] == "Open"
    assert entries[0]["old_value"] is None


def test_get_ticket_by_id_returns_none_for_missing_ticket():
    assert tickets.get_ticket_by_id(999999) is None


def test_update_status_changes_status_and_logs_history(new_ticket):
    updated = tickets.update_status(
        new_ticket, "In Progress", changed_by="pytest", note="test note"
    )
    assert updated is True

    ticket = tickets.get_ticket_by_id(new_ticket)
    assert ticket["status"] == "In Progress"

    entries = history.get_history(new_ticket)
    assert len(entries) == 2  # creation + this update
    assert entries[-1]["old_value"] == "Open"
    assert entries[-1]["new_value"] == "In Progress"
    assert entries[-1]["note"] == "test note"


def test_update_status_same_status_is_noop(new_ticket):
    result = tickets.update_status(new_ticket, "Open")
    assert result is False


def test_update_status_invalid_status_raises(new_ticket):
    with pytest.raises(ValueError):
        tickets.update_status(new_ticket, "Not A Real Status")


def test_update_status_nonexistent_ticket_returns_false():
    assert tickets.update_status(999999, "Resolved") is False