# Quick Start Guide - Enhanced Dashboard

## 🚀 What's New

The dashboard now displays **detailed student performance data** including:
- Student IDs
- Course information (code and title)
- Credit units
- Continuous Assessment scores (30%)
- Exam scores (70%)
- Final grades
- Semester information
- Study hours and extra-curricular activities

## 📋 Quick Start

### 1. Run the Dashboard

```bash
# Activate virtual environment
source ds-env/bin/activate

# Start the dashboard
streamlit run dashboard.py
```

### 2. View Sample Data

The dashboard automatically loads sample data showing:
- 10 student records
- 3 courses (CS101, CS102, CS103)
- 2 semesters (Fall 2024, Spring 2024)
- Complete academic information

### 3. Navigate the Tabs

**Tab 1: Model Metrics**
- View ML model performance
- See feature importance

**Tab 2: Visualizations**
- Correlation heatmap
- Performance box plots
- Study hours vs. grades scatter plot

**Tab 3: Data Preview** ⭐ **ENHANCED**
- **Raw Data Table**: All records
- **Detailed Performance Table**: Formatted view with all fields
- **Course Summary**: Average performance by course
- **Semester Summary**: Average performance by semester
- **Download Button**: Export data to CSV

## 📊 Understanding the Tables

### Detailed Student Performance Table
Shows each student's complete record:
```
Student ID | Hours | Course | Course Title | Credits | CA(30%) | Exam(70%) | Final | Semester
```

### Performance Summary by Course
Aggregated statistics per course:
```
Course | # Students | Avg Hours | Avg CA | Avg Exam | Avg Final Grade
```

### Performance Summary by Semester
Aggregated statistics per semester:
```
Semester | # Students | Avg Hours | Avg CA | Avg Exam | Avg Final Grade
```

## 📁 Upload Your Own Data

### CSV Format Required

Your CSV file should have these columns:

```csv
student_id,hours_studied,course,course_title,credit_unit,continuous_assessment,exam_score,semester,extra_curricular
STU001,5,CS101,Intro to Programming,3,25,55,Fall 2024,Yes
STU002,7,CS102,Data Structures,4,28,60,Fall 2024,No
```

### Column Descriptions

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| student_id | String | - | Unique identifier (e.g., STU001) |
| hours_studied | Integer | 0-∞ | Hours spent studying |
| course | String | - | Course code (e.g., CS101) |
| course_title | String | - | Full course name |
| credit_unit | Integer | 1-6 | Credit hours |
| continuous_assessment | Float | 0-30 | CA score (30% weight) |
| exam_score | Float | 0-70 | Exam score (70% weight) |
| semester | String | - | e.g., "Fall 2024" |
| extra_curricular | String | Yes/No | Participation status |

### Using Sample Data

A sample file `sample_detailed_data.csv` is included with 20 records. Use it as a template!

## 🎯 Key Features

✅ **Comprehensive Data**: Track all academic metrics in one place
✅ **Course Analytics**: See how different courses perform
✅ **Semester Trends**: Compare performance across semesters
✅ **Automatic Grading**: Final grade = CA(30%) + Exam(70%)
✅ **Export Ready**: Download processed data anytime
✅ **ML Predictions**: Built-in regression model
✅ **Visual Analytics**: Interactive charts and graphs

## 💡 Tips

1. **CA scores** should be out of 30 (representing 30% of final grade)
2. **Exam scores** should be out of 70 (representing 70% of final grade)
3. **Final grade** is automatically calculated (CA + Exam = 100)
4. Use consistent **semester naming** (e.g., "Fall 2024", "Spring 2025")
5. Keep **course codes** consistent for proper aggregation

## 🔍 Example Use Cases

### For Instructors
- Compare performance across different courses
- Identify students needing support
- Analyze correlation between study hours and grades

### For Administrators
- Generate semester-end reports
- Track overall academic trends
- Monitor course-wise performance

### For Students
- View complete academic record
- Compare personal performance with averages
- Track improvement over time

## 📞 Need Help?

- Check `ENHANCED_FEATURES.md` for detailed documentation
- See `CHANGES.md` for complete list of updates
- View `sample_detailed_data.csv` for data format example

## 🎓 Dashboard URL

Once running, access at: **http://localhost:8503**

---

**Enjoy your enhanced Student Performance Dashboard! 🚀**
