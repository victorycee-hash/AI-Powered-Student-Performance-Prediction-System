"""
Database initialization script
Run this once to set up the database with indexes and initial configuration
"""
from database import get_database
import sys

def initialize_database():
    """Initialize the database with proper indexes"""
    db = get_database()
    
    if db is None:
        print("❌ Failed to connect to database")
        sys.exit(1)
    
    print("✅ Connected to MongoDB successfully")
    
    # Create indexes for users collection
    users_collection = db.users
    
    print("Creating indexes for 'users' collection...")
    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)
    print("✅ User indexes created")
    
    # Create indexes for students collection
    students_collection = db.students
    
    print("Creating indexes for 'students' collection...")
    students_collection.create_index("student_id")
    students_collection.create_index("uploaded_by")
    students_collection.create_index("uploaded_at")
    students_collection.create_index([("course", 1), ("semester", 1)])
    print("✅ Student indexes created")
    
    # Create indexes for courses collection
    courses_collection = db.courses
    
    print("Creating indexes for 'courses' collection...")
    courses_collection.create_index("course_code", unique=True)
    print("✅ Course indexes created")
    
    # Display collection stats
    print("\n📊 Database Statistics:")
    print(f"Users: {users_collection.count_documents({})}")
    print(f"Students: {students_collection.count_documents({})}")
    print(f"Courses: {courses_collection.count_documents({})}")
    
    print("\n🎉 Database initialization complete!")
    print("\nYou can now run the dashboard with: streamlit run dashboard.py")

if __name__ == "__main__":
    print("🚀 Initializing Student Performance Database...")
    print("=" * 50)
    initialize_database()
