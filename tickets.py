from db import get_connection
import history


VALID_STATUSES = ('Open', 'In Progress', 'Blocked', 'Resolved')
VALID_PRIORITIES = ('Low', 'Medium', 'High', 'Critical')


def create_ticket(title, description, priority, assignee_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO tickets
        (title, description, priority, assignee_id)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (title, description, priority, assignee_id))
    connection.commit()

    ticket_id = cursor.lastrowid

    cursor.close()
    connection.close()

    history.log_change(
        ticket_id=ticket_id,
        field_changed="status",
        old_value=None,
        new_value="Open",
        changed_by="system",
        note="Ticket created"
    )

    return ticket_id


def get_all_tickets():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            tickets.id,
            tickets.title,
            tickets.description,
            tickets.priority,
            tickets.status,
            users.name AS assignee,
            tickets.created_at,
            tickets.updated_at
        FROM tickets
        LEFT JOIN users
            ON tickets.assignee_id = users.id
        ORDER BY tickets.created_at DESC
    """

    cursor.execute(query)
    tickets = cursor.fetchall()

    cursor.close()
    connection.close()

    return tickets


def get_ticket_by_id(ticket_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            tickets.id,
            tickets.title,
            tickets.description,
            tickets.priority,
            tickets.status,
            tickets.assignee_id,
            users.name AS assignee,
            tickets.created_at,
            tickets.updated_at
        FROM tickets
        LEFT JOIN users
            ON tickets.assignee_id = users.id
        WHERE tickets.id = %s
    """

    cursor.execute(query, (ticket_id,))
    ticket = cursor.fetchone()

    cursor.close()
    connection.close()

    return ticket


def update_status(ticket_id, new_status, changed_by="system", note=None):
    if new_status not in VALID_STATUSES:
        raise ValueError(f"'{new_status}' is not a valid status. Must be one of {VALID_STATUSES}")

    current = get_ticket_by_id(ticket_id)
    if current is None:
        return False

    old_status = current["status"]
    if old_status == new_status:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    query = "UPDATE tickets SET status = %s WHERE id = %s"
    cursor.execute(query, (new_status, ticket_id))
    connection.commit()

    cursor.close()
    connection.close()

    history.log_change(
        ticket_id=ticket_id,
        field_changed="status",
        old_value=old_status,
        new_value=new_status,
        changed_by=changed_by,
        note=note
    )

    return True


def get_all_users():
    """
    Return all users as a list of dicts, for populating assignee dropdowns.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT id, name FROM users ORDER BY name"
    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users