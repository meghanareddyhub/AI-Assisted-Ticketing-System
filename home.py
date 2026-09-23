import streamlit as st
import pandas as pd
import tickets

st.set_page_config(page_title="Ticketing Dashboard", layout="wide")

st.title("🎫 Ticket Dashboard")

all_tickets = tickets.get_all_tickets()

if not all_tickets:
    st.info("No tickets yet. Use the 'Create Ticket' page in the sidebar to add one.")
else:
    df = pd.DataFrame(all_tickets)
    df["assignee"] = df["assignee"].fillna("Unassigned")

    # --- Summary counts ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Open", int((df["status"] == "Open").sum()))
    col2.metric("In Progress", int((df["status"] == "In Progress").sum()))
    col3.metric("Blocked", int((df["status"] == "Blocked").sum()))
    col4.metric("Resolved", int((df["status"] == "Resolved").sum()))

    st.divider()

    # --- Filters ---
    st.sidebar.header("Filters")

    status_options = sorted(df["status"].unique().tolist())
    priority_options = sorted(df["priority"].unique().tolist())
    assignee_options = sorted(df["assignee"].unique().tolist())

    selected_statuses = st.sidebar.multiselect("Status", status_options, default=status_options)
    selected_priorities = st.sidebar.multiselect("Priority", priority_options, default=priority_options)
    selected_assignees = st.sidebar.multiselect("Assignee", assignee_options, default=assignee_options)

    filtered = df[
        df["status"].isin(selected_statuses)
        & df["priority"].isin(selected_priorities)
        & df["assignee"].isin(selected_assignees)
    ]

    st.subheader(f"Tickets ({len(filtered)})")
    st.dataframe(
        filtered[["id", "title", "priority", "status", "assignee", "created_at", "updated_at"]],
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Open the 'Ticket Detail' page from the sidebar and enter a ticket ID "
        "to view full details, change status, or see its history."
    )