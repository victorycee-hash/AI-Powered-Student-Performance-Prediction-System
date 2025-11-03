# 🔐 Authentication & Database Integration Guide

## Overview

The Student Performance Dashboard now includes:
- **User Authentication** (Login/Signup)
- **MongoDB Database Integration**
- **Secure Password Hashing**
- **Session Management**
- **Data Persistence**

---

## 🗄️ Database Configuration

### MongoDB Connection
- **Database**: MongoDB Atlas (Cloud)
- **Connection String**: `mongodb+srv://giddel100_db_user:EeKT6VT5VLVCjTrt@cluster0.tfooa5n.mongodb.net/`
- **Database Name**: `student_performance_db`

### Collections
1. **users** - Stores user accounts and authentication data
2. **students** - Stores student performance records
3. **courses** - Stores course information (future use)

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install pymongo bcrypt python-dotenv
```

All required packages are listed in `requirements.txt`:
- `pymongo` - MongoDB driver
- `bcrypt` - Password hashing
- `python-dotenv` - Environment variables

### 2. Run the Application

```bash
streamlit run dashboard.py
```

### 3. First Time Setup

**Create an Account:**
1. Click "Sign Up" on the login page
2. Fill in all required fields:
   - Full Name
   - Username (min 3 characters)
   - Email (valid format)
   - Password (see requirements below)
3. Click "Create Account"

**Login:**
1. Enter your username and password
2. Click "Login"
3. Access the full dashboard

---

## 🔒 Security Features

### Password Requirements
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one number

**Example valid passwords:**
- `MyPass123`
- `SecureP@ss1`
- `Dashboard2024`

### Password Security
- Passwords are hashed using **bcrypt** (industry-standard)
- Original passwords are never stored
- Hashes are salted for additional security
- No plain-text passwords in database

### Session Management
- Sessions persist across page refreshes
- Automatic logout on closing browser
- Manual logout available via button

---

## 📊 Database Operations

### Saving Data to Database

1. Upload or use sample data in the dashboard
2. Navigate to "Data Preview" tab
3. Click "💾 Save Data to Database"
4. Data is saved with:
   - Your username (uploaded_by)
   - Timestamp (uploaded_at)
   - All student performance fields

### Loading Data from Database

1. Click "📂 Load Data from Database"
2. Loads up to 100 most recent records
3. Shows only data you uploaded
4. Data is displayed in a table

### Data Ownership
- Each user can only see their own uploaded data
- Admin users (future feature) can see all data
- Data is isolated by username

---

## 🏗️ Project Structure

```
student-performance-dashboard-main/
├── dashboard.py              # Main application (requires auth)
├── login.py                  # Login & Signup UI
├── auth.py                   # Authentication logic
├── database.py               # MongoDB connection & collections
├── requirements.txt          # Python dependencies
├── sample_detailed_data.csv  # Sample data file
└── [other files...]
```

### New Files Added

1. **auth.py** - Authentication module
   - User registration
   - Password hashing/verification
   - Session state management
   - Login/logout functions

2. **database.py** - Database configuration
   - MongoDB connection
   - Collection accessors
   - Connection caching

3. **login.py** - UI for authentication
   - Login form
   - Signup form
   - Form validation
   - Custom styling

---

## 👤 User Management

### User Roles
- **user** - Standard user (default)
- **instructor** - Can view student data
- **admin** - Full access (future feature)

### User Data Stored
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "<bcrypt_hash>",
  "full_name": "John Doe",
  "created_at": "2024-11-03T12:00:00Z",
  "last_login": "2024-11-03T14:30:00Z",
  "role": "user"
}
```

### Student Data Schema
```json
{
  "student_id": "STU001",
  "hours_studied": 5,
  "course": "CS101",
  "course_title": "Introduction to Programming",
  "credit_unit": 3,
  "continuous_assessment": 25,
  "exam_score": 55,
  "final_grade": 80,
  "semester": "Fall 2024",
  "extra_curricular": "Yes",
  "uploaded_by": "john_doe",
  "uploaded_at": "2024-11-03T14:35:00Z"
}
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file for sensitive data:

```env
MONGODB_URI=mongodb+srv://giddel100_db_user:EeKT6VT5VLVCjTrt@cluster0.tfooa5n.mongodb.net/
DATABASE_NAME=student_performance_db
SECRET_KEY=your_secret_key_here
```

### Changing Database Connection

Edit `database.py`:

```python
# Change this line
MONGODB_URI = "your_new_connection_string_here"
DATABASE_NAME = "your_database_name"
```

---

## 🐛 Troubleshooting

### Connection Issues

**Error**: "Failed to connect to MongoDB"

**Solutions:**
1. Check internet connection
2. Verify MongoDB Atlas cluster is running
3. Check firewall/network settings
4. Verify connection string is correct

### Login Issues

**Error**: "Invalid username or password"

**Solutions:**
1. Verify username and password are correct
2. Usernames are case-sensitive
3. Try resetting password (contact admin)

### Database Operations Fail

**Error**: "Database connection failed"

**Solutions:**
1. Check MongoDB connection
2. Verify database permissions
3. Check network connectivity
4. View logs for detailed error

---

## 📱 User Interface

### Login Page
- Clean, modern design
- Purple gradient background
- White card-style form
- Clear error messages
- "Forgot password" link

### Signup Page
- Full name, username, email fields
- Password strength requirements
- Confirmation password field
- Real-time validation
- "Back to Login" button

### Dashboard
- Welcome message with user's name
- Logout button (top-right)
- All original dashboard features
- Database save/load buttons
- User-specific data access

---

## 🔄 Workflow Example

### First-Time User
1. Visit dashboard → Redirected to login
2. Click "Sign Up"
3. Fill registration form
4. Create account successfully
5. Return to login page
6. Enter credentials
7. Access dashboard

### Returning User
1. Visit dashboard → Login page
2. Enter username/password
3. Click "Login"
4. Access dashboard immediately
5. Upload/view data
6. Save to database
7. Logout when done

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Password reset via email
- [ ] Two-factor authentication (2FA)
- [ ] Admin panel for user management
- [ ] Role-based access control (RBAC)
- [ ] Activity logs and audit trails
- [ ] Data sharing between users
- [ ] Export reports as PDF
- [ ] Email notifications
- [ ] API access for integrations
- [ ] Mobile-responsive design

---

## 📞 Support

### Common Questions

**Q: Can I change my password?**
A: Contact administrator or wait for password reset feature.

**Q: Is my data secure?**
A: Yes! Passwords are hashed with bcrypt, and data is isolated by user.

**Q: Can other users see my data?**
A: No, each user can only access their own uploaded data.

**Q: How much data can I store?**
A: Currently limited to 100 most recent records per query.

**Q: Can I delete my account?**
A: Contact administrator for account deletion.

---

## 📊 Testing Credentials

For testing purposes, you can create a test account:

**Username:** test_user  
**Email:** test@example.com  
**Password:** TestPass123  
**Full Name:** Test User

---

## ✅ Success Indicators

After successful setup, you should see:
- ✅ Login page loads with styled form
- ✅ Signup creates account successfully
- ✅ Login redirects to dashboard
- ✅ Welcome message shows your name
- ✅ Logout button appears
- ✅ Database save/load buttons work
- ✅ Data persists between sessions

---

**Version:** 3.0 (With Authentication & Database)  
**Last Updated:** November 3, 2025  
**Status:** Production Ready ✅
