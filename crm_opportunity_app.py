# CRM Opportunity Management App (Streamlit)
# Features: Auth, sidebar menu, modern theme, opportunity CRUD, status management

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime

st.set_page_config(page_title="CRM Opportunity Management", layout="wide")

# --- Streamlit Theme (modern bright) ---
st.markdown("""
    <style>
    body, .stApp { background-color: #f8fafc !important; }
    .css-1d391kg { background: #f8fafc !important; }
    .st-bw { background: #fff !important; border-radius: 8px; }
    .stButton>button { background: #217346; color: white; border-radius: 6px; }
    .stTextInput>div>input { background: #fff; border-radius: 6px; }
    .stSelectbox>div>div { background: #fff; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# --- Main App (no authentication) ---
st.title("CRM Opportunity Management")
# --- Sidebar menu ---
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Opportunities", "Customers", "Reports", "Settings"],
        icons=["briefcase", "people", "bar-chart", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )
# --- Data storage (in-memory for demo) ---
if "opportunities" not in st.session_state:
    st.session_state["opportunities"] = []
# --- Opportunity Management ---
if selected == "Opportunities":
    st.header("Manage Opportunities")
    # --- Editable Table for Opportunities ---
    import copy
    if "opportunities" not in st.session_state:
        st.session_state["opportunities"] = []
    # Prepare DataFrame
    df = pd.DataFrame(st.session_state["opportunities"])
    # Ensure all columns exist
    columns = [
        "Customer", "Contact", "Address", "Industry", "Channel", "Referred By", "Status", "Created Datetime", "Created By"
    ]
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="opps_editor",
        column_config={
            "Created Datetime": st.column_config.Column(disabled=True),
            "Created By": st.column_config.Column(disabled=True)
        }
    )
    # Save changes button
    if st.button("Save Changes"):
        # Only update editable fields, keep Created Datetime/By if present
        new_data = []
        for idx, row in edited_df.iterrows():
            # If Created Datetime/By missing, add them
            created_datetime = row.get("Created Datetime") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            created_by = row.get("Created By") or "admin"
            new_row = dict(row)
            new_row["Created Datetime"] = created_datetime
            new_row["Created By"] = created_by
            new_data.append(new_row)
        st.session_state["opportunities"] = new_data
        st.success("Opportunities updated.")
    # Show opportunities table
    if st.session_state["opportunities"]:
        df = pd.DataFrame(st.session_state["opportunities"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No opportunities yet.")
# --- Customers tab ---
if selected == "Customers":
    st.header("Customer Management (Coming Soon)")
# --- Reports tab ---
if selected == "Reports":
    st.header("Reports (Coming Soon)")
# --- Settings tab ---
if selected == "Settings":
    st.header("Settings (Coming Soon)")
