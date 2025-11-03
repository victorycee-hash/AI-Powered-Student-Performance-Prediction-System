"""
Database configuration and connection management
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import streamlit as st

# MongoDB Connection String
MONGODB_URI = "mongodb+srv://giddel100_db_user:EeKT6VT5VLVCjTrt@cluster0.tfooa5n.mongodb.net/"
DATABASE_NAME = "student_performance_db"

@st.cache_resource
def init_connection():
    """Initialize MongoDB connection"""
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        return None

def get_database():
    """Get database instance"""
    client = init_connection()
    if client is not None:
        return client[DATABASE_NAME]
    return None

def get_users_collection():
    """Get users collection"""
    db = get_database()
    if db is not None:
        return db.users
    return None

def get_students_collection():
    """Get students performance collection"""
    db = get_database()
    if db is not None:
        return db.students
    return None

def get_courses_collection():
    """Get courses collection"""
    db = get_database()
    if db is not None:
        return db.courses
    return None
