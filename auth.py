"""
User authentication module
"""
import bcrypt
import streamlit as st
from database import get_users_collection
from datetime import datetime

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def user_exists(username: str) -> bool:
    """Check if a user already exists"""
    users = get_users_collection()
    if users is not None:
        return users.find_one({"username": username}) is not None
    return False

def email_exists(email: str) -> bool:
    """Check if an email already exists"""
    users = get_users_collection()
    if users is not None:
        return users.find_one({"email": email}) is not None
    return False

def create_user(username: str, email: str, password: str, full_name: str = "") -> bool:
    """Create a new user"""
    users = get_users_collection()
    if users is None:
        st.error("Database connection failed")
        return False
    
    if user_exists(username):
        st.error("Username already exists")
        return False
    
    if email_exists(email):
        st.error("Email already registered")
        return False
    
    hashed_pw = hash_password(password)
    
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_pw,
        "full_name": full_name,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "role": "user"  # Can be 'user', 'admin', 'instructor'
    }
    
    try:
        users.insert_one(user_data)
        return True
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return False

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user"""
    users = get_users_collection()
    if users is None:
        st.error("Database connection failed")
        return None
    
    user = users.find_one({"username": username})
    
    if not user:
        return None
    
    if verify_password(password, user['password']):
        # Update last login
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return {
            "username": user["username"],
            "email": user["email"],
            "full_name": user.get("full_name", ""),
            "role": user.get("role", "user"),
            "created_at": user["created_at"]
        }
    
    return None

def init_session_state():
    """Initialize session state for authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.page = 'login'
