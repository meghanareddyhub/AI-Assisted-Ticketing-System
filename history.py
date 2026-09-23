from db import get_connection


def log_change(ticket_id, field_changed, old_value, new_value, changed_by="system", note=None):
    """
    Insert one row into ticket_history recording a single field change.
    old_value can be None (e.g. when a ticket is first created).
    """
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO ticket_history
        (ticket_id, field_changed, old_value, new_value, changed_by, note)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (ticket_id, field_changed, old_value, new_value, changed_by, note))
    connection.commit()

    cursor.close()
    connection.close()


def get_history(ticket_id):
    """
    Return all history rows for a ticket, oldest first, so it reads as a timeline.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, field_changed, old_value, new_value, changed_by, note, changed_at
        FROM ticket_history
        WHERE ticket_id = %s
        ORDER BY changed_at ASC
    """

    cursor.execute(query, (ticket_id,))
    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return history