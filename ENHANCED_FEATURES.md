# Enhanced Student Performance Dashboard

## Overview
The dashboard has been significantly enhanced to provide detailed student performance tracking with comprehensive academic metrics.

## New Features

### 1. Detailed Data Structure
The dashboard now supports an enhanced data schema with the following fields:

| Field Name | Description | Type |
|------------|-------------|------|
| `student_id` | Unique student identifier | String |
| `hours_studied` | Number of hours studied | Integer |
| `course` | Course code (e.g., CS101) | String |
| `course_title` | Full course name | String |
| `credit_unit` | Course credit hours | Integer |
| `continuous_assessment` | CA score (30% of final grade) | Float |
| `exam_score` | Exam score (70% of final grade) | Float |
| `final_grade` | Total grade (CA + Exam) | Float |
| `semester` | Academic semester | String |
| `extra_curricular` | Extra-curricular participation | String (Yes/No) |

### 2. Enhanced Data Tables

#### Main Performance Table
- Displays all student records with formatted column names
- Shows: Student ID, Hours Studied, Course Code, Course Title, Credit Units, CA (30%), Exam (70%), Final Grade, Semester
- Full-width display for better readability

#### Performance Summary by Course
Aggregates data by course showing:
- Number of students enrolled
- Average hours studied
- Average CA score
- Average exam score
- Average final grade

#### Performance Summary by Semester
Aggregates data by semester showing:
- Number of students
- Average hours studied
- Average CA score
- Average exam score
- Average final grade

### 3. Automatic Grade Calculation
- Final grades are automatically calculated as: `CA (30%) + Exam Score (70%)`
- If uploading data, you can include final_grade or it will be calculated automatically

### 4. Backward Compatibility
The dashboard maintains backward compatibility with the original simple data format:
- Basic format: `student_id`, `hours_studied`, `extra_curricular`, `final_grade`
- Detailed format: All fields listed above
- The dashboard will detect which format is uploaded and adapt accordingly

### 5. Enhanced Visualizations
- Correlation heatmaps show relationships between all numeric variables
- Box plots display grade distributions
- Scatter plots reveal study hours vs. performance relationships
- All visualizations adapt to available data fields

## Sample Data File

A sample CSV file (`sample_detailed_data.csv`) is included with 20 student records demonstrating the detailed data structure.

### CSV Format Example:
```csv
student_id,hours_studied,course,course_title,credit_unit,continuous_assessment,exam_score,semester,extra_curricular
STU001,2,CS101,Introduction to Programming,3,21,42,Fall 2024,Yes
STU002,5,CS102,Data Structures,4,27,56,Fall 2024,No
```

## Usage Instructions

### Running the Dashboard
```bash
# Activate virtual environment
source ds-env/bin/activate  # macOS/Linux
# or
ds-env\Scripts\activate     # Windows

# Run the dashboard
streamlit run dashboard.py
```

### Uploading Your Data
1. Click "Browse files" in the dashboard
2. Upload a CSV file with either:
   - Basic format (backward compatible)
   - Detailed format (recommended for full features)
3. The dashboard will automatically detect and process your data

### Using the Sample Data
If no file is uploaded, the dashboard displays sample data with:
- 10 student records
- 3 different courses
- 2 semesters (Fall 2024, Spring 2024)
- Mix of extra-curricular participation

## Technical Improvements

### Code Enhancements
- **Smart column detection**: Automatically identifies data format
- **Dynamic model training**: Selects appropriate features based on available columns
- **Robust error handling**: Clear messages for missing or incorrect data
- **Modern Streamlit API**: Updated to use `width='stretch'` instead of deprecated `use_container_width`

### Performance Optimizations
- Efficient data grouping for summary statistics
- Optimized DataFrame operations
- Minimal redundant calculations

## Future Enhancement Possibilities

1. **Student filtering**: Filter by course, semester, or grade range
2. **Grade predictions**: ML model to predict exam scores based on CA performance
3. **Trend analysis**: Track performance changes across semesters
4. **Export options**: Generate PDF reports with charts and statistics
5. **Database integration**: Connect to SQL/NoSQL databases for persistent storage
6. **User authentication**: Multi-user support with role-based access

## File Structure
```
.
├── dashboard.py                    # Main application
├── sample_detailed_data.csv        # Sample data with detailed fields
├── ENHANCED_FEATURES.md           # This documentation
├── README.md                       # Original project documentation
└── requirements.txt               # Python dependencies
```

## Notes
- All numeric calculations are rounded to 2 decimal places for clarity
- The CA score is out of 30 points (30% weight)
- The exam score is out of 70 points (70% weight)
- Final grade = CA + Exam (total 100 points)

---

**Last Updated**: November 3, 2025
**Version**: 2.0
