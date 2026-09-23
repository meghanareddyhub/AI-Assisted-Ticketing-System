import streamlit as st
import tickets
import history

st.set_page_config(page_title="Ticket Detail")

st.title("🔍 Ticket Detail")

all_tickets = tickets.get_all_tickets()

if not all_tickets:
    st.info("No tickets yet. Create one from the 'Create Ticket' page.")
    st.stop()

ticket_ids = [t["id"] for t in all_tickets]
selected_id = st.number_input(
    "Ticket ID",
    min_value=min(ticket_ids),
    max_value=max(ticket_ids),
    value=min(ticket_ids),
    step=1,
)

ticket = tickets.get_ticket_by_id(selected_id)

if ticket is None:
    st.warning(f"No ticket found with ID {selected_id}.")
    st.stop()

# --- Ticket details ---
st.subheader(ticket["title"])
st.write(ticket["description"] or "_No description provided._")

col1, col2, col3 = st.columns(3)
col1.metric("Priority", ticket["priority"])
col2.metric("Status", ticket["status"])
col3.metric("Assignee", ticket["assignee"] or "Unassigned")

st.caption(f"Created: {ticket['created_at']}  |  Last updated: {ticket['updated_at']}")

st.divider()

# --- Status update ---
st.subheader("Update Status")

other_statuses = [s for s in tickets.VALID_STATUSES if s != ticket["status"]]
new_status = st.selectbox("New status", other_statuses)
changed_by = st.text_input("Your name (optional)", value="")
note = st.text_input("Note (optional)", value="")

if st.button("Update Status"):
    updated = tickets.update_status(
        ticket_id=ticket["id"],
        new_status=new_status,
        changed_by=changed_by.strip() or "system",
        note=note.strip() or None,
    )
    if updated:
        st.success(f"Status changed to '{new_status}'.")
        st.rerun()
    else:
        st.warning("Status was not changed.")

st.divider()

# --- History timeline ---
st.subheader("History")

entries = history.get_history(ticket["id"])

if not entries:
    st.write("No history recorded yet.")
else:
    for entry in entries:
        line = f"**{entry['changed_at']}** — {entry['field_changed']}: "
        line += f"`{entry['old_value']}` → `{entry['new_value']}`"
        if entry["note"]:
            line += f" — _{entry['note']}_"
        line += f"  (by {entry['changed_by']})"
        st.markdown(line)