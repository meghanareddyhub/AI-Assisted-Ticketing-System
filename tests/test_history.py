import tickets

ticket_id = tickets.create_ticket("Test ticket", "desc", "High", 1)
print(tickets.get_ticket_by_id(ticket_id))

tickets.update_status(ticket_id, "In Progress", note="Started work")
print(tickets.get_ticket_by_id(ticket_id))

import history
print(history.get_history(ticket_id))