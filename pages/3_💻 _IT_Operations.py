import streamlit as st
import pandas as pd
import datetime
from services.database_manager import DatabaseManager
from models.it_ticket import TicketRepository, ITTicket
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="IT Operations", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("💻 IT Operations Dashboard")

# Initialize Services
db_manager = DatabaseManager()
ticket_repo = TicketRepository(db_manager)

# Initialize AI
if "chatbot_it" not in st.session_state:
    st.session_state.chatbot_it = AIAssistant(
        api_key="sk-proj-...", 
        system_role="You are an IT Support specialist. Be concise and technical.",
        session_key="it_messages",
        role_name="IT Support"
    )
chatbot = st.session_state.chatbot_it

if "it_section" not in st.session_state:
    st.session_state.it_section = "View"

# --- TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 View Tickets", use_container_width=True): st.session_state.it_section = "View"
with col2:
    if st.button("🛠️ Manage Tickets", use_container_width=True): st.session_state.it_section = "Manage"
with col3:
    if st.button("🤖 AI Assistant", use_container_width=True): st.session_state.it_section = "AI"

st.divider()

# Fetch Data
tickets = ticket_repo.get_all_tickets()

# --- SECTION 1: VIEW DATA ---
if st.session_state.it_section == "View":
    if tickets:
        data = [t.to_dict() for t in tickets]
        df = pd.DataFrame(data)

        # Metrics
        total = len(tickets)
        high = len([t for t in tickets if t.get_priority() == 'High'])
        open_t = len([t for t in tickets if t.get_status() == 'Open'])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tickets", total)
        m2.metric("High Priority", high, delta="Urgent", delta_color="inverse")
        m3.metric("Open Tickets", open_t)

        st.divider()

        # --- GRAPHS ---
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("🌊 Ticket Volume (Area Chart)")
            # Convert created date and count frequency
            if "Created Date" in df.columns:
                df["Created Date"] = pd.to_datetime(df["Created Date"])
                daily_tickets = df.groupby("Created Date").size()
                # Area chart emphasizes volume
                st.area_chart(daily_tickets, color="#9B59B6") 
            else:
                st.info("No Date data for volume analysis.")

        with col_g2:
            st.subheader("🚦 Priority Distribution")
            prio_counts = df["Priority"].value_counts()
            st.bar_chart(prio_counts, color="#E74C3C")

        st.divider()
        st.subheader("📋 Ticket Queue")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tickets found.")

# --- SECTION 2: MANAGE DATA ---
elif st.session_state.it_section == "Manage":
    tab_add, tab_upd, tab_del = st.tabs(["➕ Create Ticket", "🔄 Update Status", "❌ Delete"])

    with tab_add:
        with st.form("add_tick"):
            col_a, col_b = st.columns(2)
            with col_a:
                tid = st.text_input("Ticket ID (e.g. T-100)")
                sub = st.text_input("Subject")
            with col_b:
                pri = st.selectbox("Priority", ["Low", "Medium", "High"])
                cat = st.selectbox("Category", ["Hardware", "Software", "Network", "Access Control"])
            dsc = st.text_area("Description")
            
            if st.form_submit_button("Submit Ticket"):
                ticket_repo.insert_ticket(tid, pri, "Open", cat, sub, dsc, str(datetime.date.today()))
                st.success("Created!"); st.rerun()

    with tab_upd:
        if tickets:
            opts = {f"{t.get_subject()} (ID: {t.get_id()})": t for t in tickets}
            sel = st.selectbox("Select Ticket", list(opts.keys()))
            obj = opts[sel]
            ns = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
            if st.button("Update Status"):
                ticket_repo.update_ticket_status(obj.get_id(), ns)
                st.success("Updated!"); st.rerun()

    with tab_del:
        if tickets:
            ids = [t.get_id() for t in tickets]
            did = st.selectbox("Select ID to Delete", ids)
            if st.button("Confirm Delete", type="primary"):
                ticket_repo.delete_ticket(did)
                st.success("Deleted."); st.rerun()

# --- SECTION 3: AI ASSISTANT ---
elif st.session_state.it_section == "AI":
    st.subheader("🤖 IT Support Assistant")
    chatbot.display_chat()