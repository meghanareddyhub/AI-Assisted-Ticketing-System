import os
import sys

# Ensure the project root is importable regardless of how pytest is invoked
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from db import get_connection
import tickets


@pytest.fixture
def new_ticket():
    """
    Creates a fresh test ticket, yields its ID, then deletes it
    (and its history rows) afterwards so tests don't leave junk data behind.
    """
    ticket_id = tickets.create_ticket(
        title="Pytest test ticket",
        description="Created by automated test",
        priority="Medium",
        assignee_id=None,
    )

    yield ticket_id

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ticket_history WHERE ticket_id = %s", (ticket_id,))
    cursor.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
    connection.commit()
    cursor.close()
    connection.close()