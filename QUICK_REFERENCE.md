# 🚀 Quick Reference Card

## Student Performance Dashboard v3.0
**With Authentication & MongoDB Database**

---

## ⚡ Quick Start

```bash
# Run the dashboard
streamlit run dashboard.py

# Access at: http://localhost:8501
```

---

## 🔐 First Time User

### Sign Up
1. Visit dashboard → Click "Sign Up"
2. Fill form (Name, Username, Email, Password)
3. Click "Create Account"
4. ✅ Success → Redirected to login

### Login
1. Enter Username & Password
2. Click "Login"
3. ✅ Access dashboard

---

## 📊 Using the Dashboard

### Upload Data
- Click "Browse files"
- Select CSV file
- Data loads automatically

### Save to Database
- Go to "Data Preview" tab
- Click "💾 Save Data to Database"
- ✅ Data saved with your username

### Load from Database
- Click "📂 Load Data from Database"
- See your uploaded records
- ✅ Data displayed in table

### Logout
- Click "Logout" button (top-right)
- Redirected to login page

---

## 🔒 Password Requirements

✅ At least 8 characters  
✅ One uppercase letter  
✅ One lowercase letter  
✅ One number  

**Example**: `MyPass123`, `SecurePass1`, `Dashboard2024`

---

## 🗄️ Database Info

**Connection**: MongoDB Atlas (Cloud)  
**Database**: `student_performance_db`  
**Collections**: users, students, courses  

**Your Data**: Isolated by username  
**Storage**: Unlimited uploads  
**Access**: Only you can see your data  

---

## 📱 Features

✨ User Authentication  
✨ Secure Login/Signup  
✨ Data Persistence  
✨ Cloud Database  
✨ Performance Analytics  
✨ Course Summaries  
✨ Semester Trends  
✨ Export to CSV  
✨ ML Predictions  

---

## 🆘 Quick Help

**Can't Login?**
- Check username/password (case-sensitive)
- Try creating new account

**Database Error?**
- Check internet connection
- Verify MongoDB is accessible

**Need Help?**
- See `AUTH_DATABASE_GUIDE.md`
- See `QUICK_START.md`

---

## 📞 Support Files

- `AUTH_DATABASE_GUIDE.md` - Full auth guide
- `COMPLETION_REPORT.md` - Implementation summary
- `QUICK_START.md` - Dashboard guide
- `ENHANCED_FEATURES.md` - Feature docs

---

## ✅ Status

🟢 **Dashboard**: Running  
🟢 **Database**: Connected  
🟢 **Authentication**: Active  
🟢 **Features**: All operational  

---

**Version**: 3.0  
**URL**: http://localhost:8501  
**Status**: Production Ready ✅
