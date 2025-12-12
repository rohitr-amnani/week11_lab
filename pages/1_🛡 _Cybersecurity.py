import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.security_incidents import Incident, SecurityIncident
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="Cybersecurity", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("🛡️ Cybersecurity Dashboard")

# Initialize Services
db_manager = DatabaseManager()
incident_repo = Incident(db_manager)

# Initialize AI
if "chatbot_sec" not in st.session_state:
    st.session_state.chatbot_sec = AIAssistant(
        api_key="sk-proj-...", 
        system_role="You are a cybersecurity expert specializing in threat analysis.",
        session_key="cyber_messages",
        role_name="Cybersecurity"
    )
chatbot = st.session_state.chatbot_sec

if "sec_section" not in st.session_state:
    st.session_state.sec_section = "View"

# --- TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("View Incidents", use_container_width=True): st.session_state.sec_section = "View"
with col2:
    if st.button("Manage Records", use_container_width=True): st.session_state.sec_section = "Manage"
with col3:
    if st.button("AI Assistant", use_container_width=True): st.session_state.sec_section = "AI"

st.divider()

# Fetch Data
incidents_list = incident_repo.get_all_incidents()

# --- SECTION 1: VIEW DATA ---
if st.session_state.sec_section == "View":
    if incidents_list:
        data = [i.to_dict() for i in incidents_list]
        df = pd.DataFrame(data)

        # Metrics
        total = len(incidents_list)
        critical = len([i for i in incidents_list if i.get_severity() == 'Critical'])
        open_cases = len([i for i in incidents_list if i.get_status() == 'Open'])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Incidents", total)
        m2.metric("Critical Threats", critical, delta="Alert", delta_color="inverse")
        m3.metric("Open Cases", open_cases)
        
        st.divider()

        # --- GRAPHS ---
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader(" Attack Trend (Over Time)")
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
                # Group by date to show timeline
                trend_data = df.groupby("Date").size()
                st.line_chart(trend_data, color="#FF4B4B") # Red Line
            else:
                st.info("Date data unavailable for trend.")

        with col_g2:
            st.subheader("🛡️ Incidents by Type")
            # Bar chart for categorical comparison
            type_counts = df["Incident Type"].value_counts()
            st.bar_chart(type_counts, color="#FFA500") # Orange Bars

        st.divider()
        st.subheader(" Detailed Incident Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data available.")

# --- SECTION 2: MANAGE DATA ---
elif st.session_state.sec_section == "Manage":
    tab_add, tab_upd, tab_del = st.tabs(["Add Incident", "Update Status", "Delete"])
    
    with tab_add:
        with st.form("add_inc"):
            date = st.date_input("Date")
            typ = st.selectbox("Type", ["Malware", "Phishing", "DDoS", "Intrusion", "Data Leak"])
            sev = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            stat = st.selectbox("Status", ["Open", "Closed", "Investigating"])
            desc = st.text_area("Description")
            
            if st.form_submit_button("Submit"):
                reporter = st.session_state.get("username", "Unknown")
                incident_repo.insert_incident(str(date), typ, sev, stat, desc, reporter)
                st.success("Added!"); st.rerun()

    with tab_upd:
        if incidents_list:
            opts = {f"{i.get_type()} (ID: {i.get_id()})": i for i in incidents_list}
            sel = st.selectbox("Select Incident", list(opts.keys()))
            obj = opts[sel]
            new_s = st.selectbox("New Status", ["Open", "Closed", "Investigating", "Resolved"])
            if st.button("Update Status"):
                incident_repo.update_incident_status(obj.get_id(), new_s)
                st.success("Updated!"); st.rerun()

    with tab_del:
        if incidents_list:
            ids = [i.get_id() for i in incidents_list]
            did = st.selectbox("Select ID to Delete", ids)
            if st.button("Confirm Delete", type="primary"):
                incident_repo.delete_incident(did)
                st.success("Deleted."); st.rerun()

# --- SECTION 3: AI ASSISTANT ---
elif st.session_state.sec_section == "AI":
    st.subheader("Security Analyst Chat")
    chatbot.display_chat()