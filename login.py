"""
Login and Signup page for Student Performance Dashboard
"""
import streamlit as st
from auth import create_user, authenticate_user, init_session_state, logout
import re

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    """Check if password meets strength requirements"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def show_login_page():
    """Display login page"""
    st.markdown("# 🎓 Student Performance Dashboard")
    st.markdown("### Welcome Back!")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 Login")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col_btn2:
                signup_btn = st.form_submit_button("Sign Up", use_container_width=True, type="secondary")
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success(f"Welcome back, {user['full_name'] or username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            if signup_btn:
                st.session_state.page = 'signup'
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Forgot password?** Contact your administrator")

def show_signup_page():
    """Display signup page"""
    st.markdown("# 🎓 Student Performance Dashboard")
    st.markdown("### Create Your Account")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 📝 Sign Up")
        
        with st.form("signup_form", clear_on_submit=True):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            st.markdown("""
            **Password Requirements:**
            - At least 8 characters long
            - Contains uppercase and lowercase letters
            - Contains at least one number
            """)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Create Account", use_container_width=True)
            with col_btn2:
                back_btn = st.form_submit_button("Back to Login", use_container_width=True, type="secondary")
            
            if submit:
                # Validation
                errors = []
                
                if not full_name or not username or not email or not password or not confirm_password:
                    errors.append("All fields are required")
                
                if len(username) < 3:
                    errors.append("Username must be at least 3 characters long")
                
                if not is_valid_email(email):
                    errors.append("Invalid email format")
                
                if not is_strong_password(password):
                    errors.append("Password does not meet requirements")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Create user
                    if create_user(username, email, password, full_name):
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = 'login'
                        st.balloons()
                        st.rerun()
            
            if back_btn:
                st.session_state.page = 'login'
                st.rerun()

def show_auth_page():
    """Main authentication page router"""
    init_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .stMarkdown {
            color: white;
        }
        div[data-testid="column"] {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        div[data-testid="column"] .stMarkdown {
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        return True
    
    if st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'signup':
        show_signup_page()
    
    return False

if __name__ == "__main__":
    show_auth_page()
