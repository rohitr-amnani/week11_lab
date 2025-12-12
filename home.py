import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(page_title="Login", page_icon="🏢", layout="wide")

db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.logged_in:
    st.success(f"✅ Welcome back, {st.session_state.username}!")
    st.info("👈 Please select a Dashboard from the sidebar to begin.")
    
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

else:
    st.title("🔒 Multi-Domain Intelligence Platform")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Log In", type="primary"):
            if auth_manager.login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab_register:
        st.subheader("Register New Account")
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        new_role = st.selectbox("Select Role", ["User", "Admin"], key="reg_role")

        if st.button("Create Account"):
            valid_u, msg_u = auth_manager.validate_username(new_user)
            valid_p, msg_p = auth_manager.validate_password(new_pass)

            if not valid_u:
                st.error(msg_u)
            elif not valid_p:
                st.error(msg_p)
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                success, msg = auth_manager.register_user(new_user, new_pass, role=new_role)
                if success:
                    st.success(msg + " Please log in.")
                else:
                    st.error(msg)