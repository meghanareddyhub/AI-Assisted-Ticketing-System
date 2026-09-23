# from tickets import create_ticket

# ticket_id = create_ticket(
#     "Login problem",
#     "User is unable to login to the application.",
#     "High",
#     1
# )

# print("Ticket created with ID:", ticket_id)

from tickets import get_all_tickets

tickets = get_all_tickets()

for ticket in tickets:
    print(ticket)