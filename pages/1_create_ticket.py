import streamlit as st
import tickets

st.set_page_config(page_title="Create Ticket")

st.title("➕ Create Ticket")

users = tickets.get_all_users()
user_options = {"Unassigned": None}
user_options.update({u["name"]: u["id"] for u in users})

with st.form("create_ticket_form", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", tickets.VALID_PRIORITIES, index=1)
    assignee_name = st.selectbox("Assignee", list(user_options.keys()))

    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        if not title.strip():
            st.error("Title is required.")
        else:
            assignee_id = user_options[assignee_name]
            new_id = tickets.create_ticket(
                title=title.strip(),
                description=description.strip(),
                priority=priority,
                assignee_id=assignee_id
            )
            st.success(f"Ticket #{new_id} created successfully.")
            st.info("Go to the Home page to see it in the dashboard.")