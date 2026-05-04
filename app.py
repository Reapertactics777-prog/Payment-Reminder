import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page Config
st.set_page_config(page_title="PayTrack AI", page_icon="💸")

# 1. Automatic Refresh (Checks every 60 seconds)
st_autorefresh(interval=60000, key="datacheck")

# 2. Data Persistence Logic
if 'payments' not in st.session_state:
    # In a real app, you'd load from a CSV or Database here
    st.session_state.payments = []

def add_payment(name, amount, due_date):
    st.session_state.payments.append({
        "Name": name,
        "Amount": amount,
        "Due Date": due_date,
        "Status": "Pending"
    })

# --- UI Layout ---
st.title("💸 PayTrack Reminder")
st.markdown("Monitor your bills and subscriptions efficiently.")

# Sidebar for adding new payments
with st.sidebar:
    st.header("Add New Payment")
    name = st.text_input("Service Name", placeholder="e.g. Spotify")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    due_date = st.date_input("Due Date")
    
    if st.button("Add Reminder"):
        if name:
            add_payment(name, amount, due_date)
            st.success(f"Added {name}!")
        else:
            st.error("Please enter a name.")

# Display Dashboard
if st.session_state.payments:
    df = pd.DataFrame(st.session_state.payments)
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    
    # Sort by closest date
    df = df.sort_values(by="Due Date")

    # Check for Reminders
    today = datetime.now().date()
    upcoming = df[df['Due Date'] == today]

    if not upcoming.empty:
        for _, row in upcoming.iterrows():
            st.warning(f"🚨 **REMINDER:** Your payment for **{row['Name']}** (${row['Amount']}) is due today!")

    # Display Table
    st.subheader("Your Subscriptions")
    st.dataframe(df, use_container_width=True)

    if st.button("Clear All Data"):
        st.session_state.payments = []
        st.rerun()
else:
    st.info("No active reminders. Add one in the sidebar to get started!")

# Footer
st.divider()
st.caption("Note: This app stores data in the current session. For permanent storage, connect a database like Supabase or a Google Sheet.")
