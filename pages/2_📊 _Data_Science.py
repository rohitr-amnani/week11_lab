import streamlit as st
import pandas as pd
import datetime
from services.database_manager import DatabaseManager
from models.dataset import DatasetRepository, Dataset
from services.ai_assistant import AIAssistant

st.set_page_config(page_title="Data Science", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("📊 Data Science Dashboard")

# Initialize Services
db_manager = DatabaseManager()
dataset_repo = DatasetRepository(db_manager)

# Initialize AI
if "chatbot_ds" not in st.session_state:
    st.session_state.chatbot_ds = AIAssistant(
        api_key="sk-proj-...", 
        system_role="You are a data science expert skilled in Python, SQL, and Statistics.",
        session_key="data_messages",
        role_name="Data Science"
    )
chatbot = st.session_state.chatbot_ds

if "ds_section" not in st.session_state:
    st.session_state.ds_section = "View"

# --- TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("View Datasets", use_container_width=True): st.session_state.ds_section = "View"
with col2:
    if st.button("Manage Data", use_container_width=True): st.session_state.ds_section = "Manage"
with col3:
    if st.button("AI Assistant", use_container_width=True): st.session_state.ds_section = "AI"

st.divider()

# Fetch Data
datasets = dataset_repo.get_all_datasets()

# --- SECTION 1: VIEW DATA ---
if st.session_state.ds_section == "View":
    if datasets:
        data = [d.to_dict() for d in datasets]
        df = pd.DataFrame(data)

        # Metrics
        total_files = len(datasets)
        total_records = sum([d.get_row_count() for d in datasets])
        total_size = sum([d.get_size_mb() for d in datasets])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Datasets", total_files)
        m2.metric("Total Records", f"{total_records:,}")
        m3.metric("Total Storage (MB)", f"{total_size:.2f}")

        st.divider()

        # --- GRAPHS ---
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("📂 Datasets by Category")
            # Simple bar chart for counts
            cat_counts = df["Category"].value_counts()
            st.bar_chart(cat_counts, color="#1E90FF")

        with col_g2:
            st.subheader("⚖️ Size vs. Records Analysis")
            # Scatter chart to see correlation between size and rows
            # Rename columns to map easily if needed, but st.scatter_chart auto-detects
            chart_data = df[["Record Count", "Size (MB)", "Category"]]
            st.scatter_chart(
                chart_data,
                x="Record Count",
                y="Size (MB)",
                color="Category",
                size="Size (MB)" # Bubbles are bigger if file is bigger
            )

        st.divider()
        st.subheader("Dataset Registry")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No datasets registered.")

# --- SECTION 2: MANAGE DATA ---
elif st.session_state.ds_section == "Manage":
    tab_add, tab_upd, tab_del = st.tabs(["Register Dataset", "Update Count", "Delete"])

    with tab_add:
        with st.form("add_ds"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Dataset Name")
                cat = st.selectbox("Category", ["Finance", "Health", "Sales", "Operations", "Security", "Marketing"])
            with col_b:
                cnt = st.number_input("Record Count", min_value=0)
                size = st.number_input("Size (MB)", min_value=0.0)
            
            src = st.text_input("Source URL/Path")
            
            if st.form_submit_button("Register"):
                dataset_repo.insert_dataset(name, cat, src, str(datetime.date.today()), cnt, size)
                st.success("Registered!"); st.rerun()

    with tab_upd:
        if datasets:
            opts = {f"{d.get_name()}": d for d in datasets}
            sel = st.selectbox("Select Dataset", list(opts.keys()))
            obj = opts[sel]
            nc = st.number_input("New Record Count", value=obj.get_row_count())
            if st.button("Update Count"):
                dataset_repo.update_dataset_record_count(obj.get_id(), nc)
                st.success("Updated!"); st.rerun()

    with tab_del:
        if datasets:
            ids = [d.get_id() for d in datasets]
            did = st.selectbox("Select ID to Delete", ids)
            if st.button("Confirm Delete", type="primary"):
                dataset_repo.delete_dataset(did)
                st.success("Deleted."); st.rerun()

# --- SECTION 3: AI ASSISTANT ---
elif st.session_state.ds_section == "AI":
    st.subheader(" Data Science Assistant")
    chatbot.display_chat()