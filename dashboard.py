import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from login import show_auth_page
from auth import logout, init_session_state
from database import get_students_collection

# Set page config
st.set_page_config(page_title="Student Performance Dashboard", page_icon=":mortar_board:", layout="wide")

# Initialize session state
init_session_state()

# Check authentication
if not show_auth_page():
    st.stop()

# User is authenticated, show dashboard
# Header with user info and logout button
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("Student Performance Prediction Dashboard")
with col_header2:
    st.markdown(f"**Welcome, {st.session_state.user['full_name'] or st.session_state.user['username']}**")
    if st.button("Logout", key="logout_btn"):
        logout()
        st.rerun()

st.markdown("---")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Check if the uploaded file has the detailed columns or the basic columns
    detailed_columns = {'student_id', 'hours_studied', 'course', 'course_title', 'credit_unit', 
                       'continuous_assessment', 'exam_score', 'semester'}
    basic_columns = {'hours_studied', 'final_grade', 'extra_curricular'}
    
    if detailed_columns.issubset(df.columns):
        # Calculate final grade if not present
        if 'final_grade' not in df.columns:
            df['final_grade'] = df['continuous_assessment'] + df['exam_score']
        # Validate required columns for detailed data
        st.success("Detailed student data loaded successfully!")
    elif basic_columns.issubset(df.columns):
        st.info("Basic data format detected. For full features, upload data with: student_id, hours_studied, course, course_title, credit_unit, continuous_assessment, exam_score, semester")
    else:
        st.error(f"The uploaded file must contain either basic columns ({', '.join(basic_columns)}) or detailed columns ({', '.join(detailed_columns)})")
        st.stop()
    
    # Data preprocessing
    if 'extra_curricular' in df.columns:
        df['extra_curricular'] = df['extra_curricular'].map({'Yes': 1, 'No': 0})
    
    # Sidebar for model parameters
    st.sidebar.header("Model Parameters")
    test_size = st.sidebar.slider("Test Size", 0.1, 0.5, 0.2, 0.1)
    random_state = st.sidebar.number_input("Random State", 0, 100, 42)

    # Model Training - handle both detailed and basic data
    exclude_cols = ['student_id', 'final_grade']
    if 'course' in df.columns:
        exclude_cols.extend(['course', 'course_title', 'semester'])
    
    X = df.drop(columns=[col for col in exclude_cols if col in df.columns])
    y = df['final_grade']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Model Metrics", "Visualizations", "Data Preview", "Predictions & Advice", "Prediction Logs"])

    with tab1:
        st.subheader("Model Evaluation Metrics")
        col1, col2 = st.columns(2)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        col1.metric("Mean Squared Error", f"{mse:.2f}")
        col2.metric("R-squared", f"{r2:.2f}")
        
        # Feature importance
        st.subheader("Feature Importance")
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.coef_
        })
        st.bar_chart(importance_df.set_index('Feature'))

    with tab2:
        st.subheader("Data Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1, ax1 = plt.subplots(figsize=(6,4))
            sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax1)
            st.pyplot(fig1)
            
        with col2:
            if 'extra_curricular' in df.columns:
                fig2, ax2 = plt.subplots(figsize=(6,4))
                sns.boxplot(data=df, x='extra_curricular', y='final_grade', ax=ax2)
                st.pyplot(fig2)
            
        # Scatter plot
        fig3, ax3 = plt.subplots(figsize=(8,4))
        if 'extra_curricular' in df.columns:
            sns.scatterplot(data=df, x='hours_studied', y='final_grade', hue='extra_curricular')
        else:
            sns.scatterplot(data=df, x='hours_studied', y='final_grade')
        st.pyplot(fig3)

    with tab3:
        st.subheader("Sample Data Preview")
        st.dataframe(df)
        
        # Detailed table view
        st.subheader("Detailed Student Performance Table")
        
        # Create a formatted display dataframe
        if all(col in df.columns for col in ['student_id', 'course', 'course_title', 'credit_unit', 'continuous_assessment', 'exam_score', 'semester']):
            display_df = df[['student_id', 'hours_studied', 'course', 'course_title', 'credit_unit', 
                            'continuous_assessment', 'exam_score', 'final_grade', 'semester']].copy()
            
            # Format column names for better display
            display_df.columns = ['Student ID', 'Hours Studied', 'Course Code', 'Course Title', 
                                 'Credit Units', 'CA (30%)', 'Exam (70%)', 'Final Grade', 'Semester']
            
            st.dataframe(display_df, width='stretch')
            
            # Summary statistics by course
            st.subheader("Performance Summary by Course")
            if 'course' in df.columns:
                course_summary = df.groupby('course').agg({
                    'student_id': 'count',
                    'hours_studied': 'mean',
                    'continuous_assessment': 'mean',
                    'exam_score': 'mean',
                    'final_grade': 'mean'
                }).round(2)
                course_summary.columns = ['Number of Students', 'Avg Hours Studied', 'Avg CA Score', 'Avg Exam Score', 'Avg Final Grade']
                st.dataframe(course_summary, width='stretch')
            
            # Summary by semester
            st.subheader("Performance Summary by Semester")
            if 'semester' in df.columns:
                semester_summary = df.groupby('semester').agg({
                    'student_id': 'count',
                    'hours_studied': 'mean',
                    'continuous_assessment': 'mean',
                    'exam_score': 'mean',
                    'final_grade': 'mean'
                }).round(2)
                semester_summary.columns = ['Number of Students', 'Avg Hours Studied', 'Avg CA Score', 'Avg Exam Score', 'Avg Final Grade']
                st.dataframe(semester_summary, width='stretch')
        else:
            st.info("Upload detailed data to see comprehensive performance tables")
        
        # Download button for processed data
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download processed data as CSV",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )
    
    # Tab 4: Predictions & Advice
    with tab4:
        st.subheader("📊 Prediction Results & Student Advice")
        
        # Prediction Results Output
        st.markdown("### Individual Student Predictions")
        # Use the indices from y_test to get corresponding student IDs
        test_indices = y_test.index
        results_df = pd.DataFrame({
            'Student ID': df.loc[test_indices, 'student_id'].values if 'student_id' in df.columns else test_indices,
            'Actual Grade': y_test.values,
            'Predicted Grade': y_pred.round(2),
            'Difference': (y_test.values - y_pred).round(2),
            'Status': ['✅ On Track' if abs(a - p) < 5 else '⚠️ Needs Attention' for a, p in zip(y_test.values, y_pred)]
        })
        st.dataframe(results_df, use_container_width=True)
        
        # Explanation of Prediction Factors
        st.markdown("### 🔍 Explanation of Prediction Factors")
        st.write("**How the model predicts student performance:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Key Factors Considered:**
            - 📚 **Hours Studied**: More study time typically leads to better grades
            - 🎯 **Credit Units**: Course difficulty and workload
            - 📝 **Continuous Assessment**: CA scores indicate ongoing performance
            - 🎓 **Extra-Curricular**: Activities may impact study time
            """)
        
        with col2:
            # Feature importance chart
            st.markdown("**Feature Impact on Predictions:**")
            importance_data = pd.DataFrame({
                'Feature': X.columns,
                'Impact': abs(model.coef_)
            }).sort_values('Impact', ascending=False)
            st.bar_chart(importance_data.set_index('Feature'))
        
        st.markdown("---")
        
        # Advice and Suggestions Interface
        st.markdown("### 💡 Personalized Advice & Suggestions")
        
        # Generate advice for each student
        for idx, row in results_df.iterrows():
            with st.expander(f"Student {row['Student ID']} - {row['Status']}"):
                actual = row['Actual Grade']
                predicted = row['Predicted Grade']
                diff = row['Difference']
                
                if 'student_id' in df.columns:
                    student_data = df[df['student_id'] == row['Student ID']].iloc[0]
                else:
                    student_data = df.iloc[idx]
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("Actual Grade", f"{actual:.1f}", delta=f"{diff:.1f}")
                    st.metric("Hours Studied", student_data['hours_studied'])
                    if 'continuous_assessment' in df.columns:
                        st.metric("CA Score", f"{student_data['continuous_assessment']}/30")
                
                with col_b:
                    st.metric("Predicted Grade", f"{predicted:.1f}")
                    if 'exam_score' in df.columns:
                        st.metric("Exam Score", f"{student_data['exam_score']}/70")
                    if 'extra_curricular' in df.columns:
                        extra = "Yes" if student_data['extra_curricular'] == 1 else "No"
                        st.metric("Extra-Curricular", extra)
                
                # Generate personalized advice
                st.markdown("**📋 Recommendations:**")
                
                if actual < 50:
                    st.error("""
                    **🚨 Urgent Intervention Needed:**
                    - Schedule immediate meeting with academic advisor
                    - Consider peer tutoring or study groups
                    - Review foundational concepts
                    - Increase study hours by at least 50%
                    """)
                elif actual < 65:
                    st.warning("""
                    **⚠️ Improvement Needed:**
                    - Increase study hours to 6-8 hours per week
                    - Focus on areas with low CA scores
                    - Attend all tutorials and consultations
                    - Form study groups with high-performing peers
                    """)
                elif actual < 75:
                    st.info("""
                    **📈 Good Progress - Room for Improvement:**
                    - Maintain current study schedule
                    - Focus on exam preparation techniques
                    - Review past papers and practice questions
                    - Consider advanced topics for deeper understanding
                    """)
                else:
                    st.success("""
                    **🌟 Excellent Performance:**
                    - Keep up the excellent work!
                    - Consider mentoring other students
                    - Explore advanced projects or research
                    - Maintain work-life balance
                    """)
                
                # Specific recommendations based on features
                if student_data['hours_studied'] < 4:
                    st.markdown("- 📚 **Increase study hours**: Current hours are below recommended minimum")
                
                if 'continuous_assessment' in df.columns and student_data['continuous_assessment'] < 20:
                    st.markdown("- 📝 **Improve CA performance**: Focus on assignments and quizzes")
                
                if 'extra_curricular' in df.columns and student_data['extra_curricular'] == 1 and actual < 60:
                    st.markdown("- ⚖️ **Balance activities**: Consider reducing extra-curricular commitments temporarily")
    
    # Tab 5: Prediction Logs
    with tab5:
        st.subheader("📝 Prediction Log File Output")
        
        # Create comprehensive log
        from datetime import datetime
        log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.markdown("### System Prediction Log")
        st.text(f"Generated: {log_timestamp}")
        st.text(f"User: {st.session_state.user['username']}")
        st.text(f"Model: Linear Regression")
        st.text(f"Dataset Size: {len(df)} records")
        st.text(f"Test Set Size: {len(y_test)} records")
        st.text(f"Model Performance: R² = {r2:.4f}, MSE = {mse:.4f}")
        st.markdown("---")
        
        # Detailed log entries
        log_content = f"""
STUDENT PERFORMANCE PREDICTION SYSTEM - LOG FILE
================================================
Timestamp: {log_timestamp}
User: {st.session_state.user['username']}
Model Type: Linear Regression
Dataset: {'Uploaded File' if uploaded_file else 'Sample Data'}

MODEL CONFIGURATION:
- Test Size: {test_size}
- Random State: {random_state}
- Features Used: {', '.join(X.columns)}
- Training Samples: {len(X_train)}
- Testing Samples: {len(X_test)}

MODEL PERFORMANCE:
- R-squared Score: {r2:.4f}
- Mean Squared Error: {mse:.4f}
- Model Accuracy: {(r2 * 100):.2f}%

FEATURE IMPORTANCE:
"""
        
        for feature, coef in zip(X.columns, model.coef_):
            log_content += f"- {feature}: {coef:.4f}\n"
        
        log_content += f"\nPREDICTION RESULTS:\n"
        log_content += "="*60 + "\n"
        
        for idx, (actual, predicted) in enumerate(zip(y_test.values, y_pred)):
            student_id = results_df.iloc[idx]['Student ID']
            status = "PASS" if predicted >= 50 else "FAIL"
            log_content += f"Student {student_id}: Actual={actual:.2f}, Predicted={predicted:.2f}, Status={status}\n"
        
        log_content += "\n" + "="*60
        log_content += f"\nEnd of Log - {log_timestamp}\n"
        
        # Display log in text area
        st.text_area("Log Output", log_content, height=400)
        
        # Download log file
        st.download_button(
            label="📥 Download Prediction Log",
            data=log_content,
            file_name=f'prediction_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
            mime='text/plain',
        )
        
        # Performance chart display
        st.markdown("### 📈 Performance Chart Display")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Actual vs Predicted comparison
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(y_test, y_pred, alpha=0.6)
            ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            ax.set_xlabel('Actual Grades')
            ax.set_ylabel('Predicted Grades')
            ax.set_title('Actual vs Predicted Performance')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            # Prediction error distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            errors = y_test.values - y_pred
            ax.hist(errors, bins=15, edgecolor='black', alpha=0.7)
            ax.set_xlabel('Prediction Error')
            ax.set_ylabel('Frequency')
            ax.set_title('Prediction Error Distribution')
            ax.axvline(x=0, color='r', linestyle='--', linewidth=2)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

else:
    # Sample Data as fallback with detailed information
    data = {
        'student_id': ['STU001', 'STU002', 'STU003', 'STU004', 'STU005', 'STU006', 'STU007', 'STU008', 'STU009', 'STU010'],
        'hours_studied': [2, 5, 3, 7, 4, 6, 8, 3, 5, 4],
        'course': ['CS101', 'CS102', 'CS101', 'CS103', 'CS102', 'CS101', 'CS103', 'CS102', 'CS101', 'CS103'],
        'course_title': ['Introduction to Programming', 'Data Structures', 'Introduction to Programming', 
                        'Database Systems', 'Data Structures', 'Introduction to Programming',
                        'Database Systems', 'Data Structures', 'Introduction to Programming', 'Database Systems'],
        'credit_unit': [3, 4, 3, 3, 4, 3, 3, 4, 3, 3],
        'continuous_assessment': [21, 27, 18, 28, 24, 26, 29, 20, 25, 22],
        'exam_score': [42, 56, 49, 63, 52, 58, 65, 44, 53, 48],
        'semester': ['FIRST', 'FIRST', 'SECOND', 'FIRST', 'SECOND', 
                    'FIRST', 'SECOND', 'FIRST', 'SECOND', 'FIRST'],
        'extra_curricular': ['Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No']
    }
    df = pd.DataFrame(data)
    
    # Calculate final grade (CA 30% + Exam 70%)
    df['final_grade'] = df['continuous_assessment'] + df['exam_score']
    
    # Data preprocessing
    df['extra_curricular'] = df['extra_curricular'].map({'Yes': 1, 'No': 0})

    # Sidebar for model parameters
    st.sidebar.header("Model Parameters")
    test_size = st.sidebar.slider("Test Size", 0.1, 0.5, 0.2, 0.1)
    random_state = st.sidebar.number_input("Random State", 0, 100, 42)

    # Model Training - exclude non-numeric and identifier columns
    exclude_cols = ['student_id', 'final_grade', 'course', 'course_title', 'semester']
    X = df.drop(columns=[col for col in exclude_cols if col in df.columns])
    y = df['final_grade']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Model Metrics", "Visualizations", "Data Preview", "Predictions & Advice", "Prediction Logs"])

    with tab1:
        st.subheader("Model Evaluation Metrics")
        col1, col2 = st.columns(2)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        col1.metric("Mean Squared Error", f"{mse:.2f}")
        col2.metric("R-squared", f"{r2:.2f}")
        
        # Feature importance
        st.subheader("Feature Importance")
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.coef_
        })
        st.bar_chart(importance_df.set_index('Feature'))

    with tab2:
        st.subheader("Data Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1, ax1 = plt.subplots(figsize=(6,4))
            sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax1)
            st.pyplot(fig1)
            
        with col2:
            fig2, ax2 = plt.subplots(figsize=(6,4))
            sns.boxplot(data=df, x='extra_curricular', y='final_grade', ax=ax2)
            st.pyplot(fig2)
            
        # Scatter plot
        fig3, ax3 = plt.subplots(figsize=(8,4))
        sns.scatterplot(data=df, x='hours_studied', y='final_grade', hue='extra_curricular')
        st.pyplot(fig3)

    with tab3:
        st.subheader("Sample Data Preview")
        st.dataframe(df)
        
        # Detailed table view
        st.subheader("Detailed Student Performance Table")
        
        # Create a formatted display dataframe
        display_df = df[['student_id', 'hours_studied', 'course', 'course_title', 'credit_unit', 
                        'continuous_assessment', 'exam_score', 'final_grade', 'semester']].copy()
        
        # Format column names for better display
        display_df.columns = ['Student ID', 'Hours Studied', 'Course Code', 'Course Title', 
                             'Credit Units', 'CA (30%)', 'Exam (70%)', 'Final Grade', 'Semester']
        
        st.dataframe(display_df, width='stretch')
        
        # Summary statistics by course
        st.subheader("Performance Summary by Course")
        course_summary = df.groupby('course').agg({
            'student_id': 'count',
            'hours_studied': 'mean',
            'continuous_assessment': 'mean',
            'exam_score': 'mean',
            'final_grade': 'mean'
        }).round(2)
        course_summary.columns = ['Number of Students', 'Avg Hours Studied', 'Avg CA Score', 'Avg Exam Score', 'Avg Final Grade']
        st.dataframe(course_summary, width='stretch')
        
        # Summary by semester
        st.subheader("Performance Summary by Semester")
        semester_summary = df.groupby('semester').agg({
            'student_id': 'count',
            'hours_studied': 'mean',
            'continuous_assessment': 'mean',
            'exam_score': 'mean',
            'final_grade': 'mean'
        }).round(2)
        semester_summary.columns = ['Number of Students', 'Avg Hours Studied', 'Avg CA Score', 'Avg Exam Score', 'Avg Final Grade']
        st.dataframe(semester_summary, width='stretch')
        
        # Save to database button
        st.subheader("Database Operations")
        col_db1, col_db2 = st.columns(2)
        
        with col_db1:
            if st.button("💾 Save Data to Database", key="save_to_db"):
                students_collection = get_students_collection()
                if students_collection is not None:
                    try:
                        # Convert DataFrame to list of dictionaries
                        records = df.to_dict('records')
                        # Add metadata
                        for record in records:
                            record['uploaded_by'] = st.session_state.user['username']
                            record['uploaded_at'] = pd.Timestamp.now()
                        
                        # Insert into database
                        result = students_collection.insert_many(records)
                        st.success(f"Successfully saved {len(result.inserted_ids)} student records to database!")
                    except Exception as e:
                        st.error(f"Error saving to database: {e}")
                else:
                    st.error("Database connection failed")
        
        with col_db2:
            # Load from database button
            if st.button("📂 Load Data from Database", key="load_from_db"):
                students_collection = get_students_collection()
                if students_collection is not None:
                    try:
                        # Load data uploaded by current user
                        cursor = students_collection.find(
                            {"uploaded_by": st.session_state.user['username']}
                        ).sort("uploaded_at", -1).limit(100)
                        
                        records = list(cursor)
                        if records:
                            # Remove MongoDB _id field and metadata
                            for record in records:
                                record.pop('_id', None)
                                record.pop('uploaded_by', None)
                                record.pop('uploaded_at', None)
                            
                            loaded_df = pd.DataFrame(records)
                            st.success(f"Loaded {len(loaded_df)} records from database")
                            st.dataframe(loaded_df)
                        else:
                            st.info("No data found in database for your account")
                    except Exception as e:
                        st.error(f"Error loading from database: {e}")
                else:
                    st.error("Database connection failed")
        
        # Download button for processed data
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download processed data as CSV",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )
    
    # Tab 4: Predictions & Advice
    with tab4:
        st.subheader("📊 Prediction Results & Student Advice")
        
        # Prediction Results Output
        st.markdown("### Individual Student Predictions")
        results_df = pd.DataFrame({
            'Student ID': df.loc[y_test.index, 'student_id'].values,
            'Actual Grade': y_test.values,
            'Predicted Grade': y_pred.round(2),
            'Difference': (y_test.values - y_pred).round(2),
            'Status': ['✅ On Track' if abs(a - p) < 5 else '⚠️ Needs Attention' for a, p in zip(y_test.values, y_pred)]
        })
        st.dataframe(results_df, use_container_width=True)
        
        # Explanation of Prediction Factors
        st.markdown("### 🔍 Explanation of Prediction Factors")
        st.write("**How the model predicts student performance:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Key Factors Considered:**
            - 📚 **Hours Studied**: More study time typically leads to better grades
            - 🎯 **Credit Units**: Course difficulty and workload
            - 📝 **Continuous Assessment**: CA scores indicate ongoing performance
            - 🎓 **Extra-Curricular**: Activities may impact study time
            """)
        
        with col2:
            # Feature importance chart
            st.markdown("**Feature Impact on Predictions:**")
            importance_data = pd.DataFrame({
                'Feature': X.columns,
                'Impact': abs(model.coef_)
            }).sort_values('Impact', ascending=False)
            st.bar_chart(importance_data.set_index('Feature'))
        
        st.markdown("---")
        
        # Advice and Suggestions Interface
        st.markdown("### 💡 Personalized Advice & Suggestions")
        
        # Generate advice for each student
        for idx, row in results_df.iterrows():
            with st.expander(f"Student {row['Student ID']} - {row['Status']}"):
                actual = row['Actual Grade']
                predicted = row['Predicted Grade']
                diff = row['Difference']
                
                student_data = df[df['student_id'] == row['Student ID']].iloc[0]
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("Actual Grade", f"{actual:.1f}", delta=f"{diff:.1f}")
                    st.metric("Hours Studied", student_data['hours_studied'])
                    st.metric("CA Score", f"{student_data['continuous_assessment']}/30")
                
                with col_b:
                    st.metric("Predicted Grade", f"{predicted:.1f}")
                    st.metric("Exam Score", f"{student_data['exam_score']}/70")
                    extra = "Yes" if student_data['extra_curricular'] == 1 else "No"
                    st.metric("Extra-Curricular", extra)
                
                # Generate personalized advice
                st.markdown("**📋 Recommendations:**")
                
                if actual < 50:
                    st.error("""
                    **🚨 Urgent Intervention Needed:**
                    - Schedule immediate meeting with academic advisor
                    - Consider peer tutoring or study groups
                    - Review foundational concepts
                    - Increase study hours by at least 50%
                    """)
                elif actual < 65:
                    st.warning("""
                    **⚠️ Improvement Needed:**
                    - Increase study hours to 6-8 hours per week
                    - Focus on areas with low CA scores
                    - Attend all tutorials and consultations
                    - Form study groups with high-performing peers
                    """)
                elif actual < 75:
                    st.info("""
                    **📈 Good Progress - Room for Improvement:**
                    - Maintain current study schedule
                    - Focus on exam preparation techniques
                    - Review past papers and practice questions
                    - Consider advanced topics for deeper understanding
                    """)
                else:
                    st.success("""
                    **🌟 Excellent Performance:**
                    - Keep up the excellent work!
                    - Consider mentoring other students
                    - Explore advanced projects or research
                    - Maintain work-life balance
                    """)
                
                # Specific recommendations based on features
                if student_data['hours_studied'] < 4:
                    st.markdown("- 📚 **Increase study hours**: Current hours are below recommended minimum")
                
                if student_data['continuous_assessment'] < 20:
                    st.markdown("- 📝 **Improve CA performance**: Focus on assignments and quizzes")
                
                if student_data['extra_curricular'] == 1 and actual < 60:
                    st.markdown("- ⚖️ **Balance activities**: Consider reducing extra-curricular commitments temporarily")
    
    # Tab 5: Prediction Logs
    with tab5:
        st.subheader("📝 Prediction Log File Output")
        
        # Create comprehensive log
        from datetime import datetime
        log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.markdown("### System Prediction Log")
        st.text(f"Generated: {log_timestamp}")
        st.text(f"User: {st.session_state.user['username']}")
        st.text(f"Model: Linear Regression")
        st.text(f"Dataset Size: {len(df)} records")
        st.text(f"Test Set Size: {len(y_test)} records")
        st.text(f"Model Performance: R² = {r2:.4f}, MSE = {mse:.4f}")
        st.markdown("---")
        
        # Detailed log entries
        log_content = f"""
STUDENT PERFORMANCE PREDICTION SYSTEM - LOG FILE
================================================
Timestamp: {log_timestamp}
User: {st.session_state.user['username']}
Model Type: Linear Regression
Dataset: Sample Data

MODEL CONFIGURATION:
- Test Size: {test_size}
- Random State: {random_state}
- Features Used: {', '.join(X.columns)}
- Training Samples: {len(X_train)}
- Testing Samples: {len(X_test)}

MODEL PERFORMANCE:
- R-squared Score: {r2:.4f}
- Mean Squared Error: {mse:.4f}
- Model Accuracy: {(r2 * 100):.2f}%

FEATURE IMPORTANCE:
"""
        
        for feature, coef in zip(X.columns, model.coef_):
            log_content += f"- {feature}: {coef:.4f}\n"
        
        log_content += f"\nPREDICTION RESULTS:\n"
        log_content += "="*60 + "\n"
        
        for idx, (actual, predicted) in enumerate(zip(y_test.values, y_pred)):
            student_id = results_df.iloc[idx]['Student ID']
            status = "PASS" if predicted >= 50 else "FAIL"
            log_content += f"Student {student_id}: Actual={actual:.2f}, Predicted={predicted:.2f}, Status={status}\n"
        
        log_content += "\n" + "="*60
        log_content += f"\nEnd of Log - {log_timestamp}\n"
        
        # Display log in text area
        st.text_area("Log Output", log_content, height=400)
        
        # Download log file
        st.download_button(
            label="📥 Download Prediction Log",
            data=log_content,
            file_name=f'prediction_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
            mime='text/plain',
        )
        
        # Performance chart display
        st.markdown("### 📈 Performance Chart Display")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Actual vs Predicted comparison
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(y_test, y_pred, alpha=0.6)
            ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            ax.set_xlabel('Actual Grades')
            ax.set_ylabel('Predicted Grades')
            ax.set_title('Actual vs Predicted Performance')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            # Prediction error distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            errors = y_test.values - y_pred
            ax.hist(errors, bins=15, edgecolor='black', alpha=0.7)
            ax.set_xlabel('Prediction Error')
            ax.set_ylabel('Frequency')
            ax.set_title('Prediction Error Distribution')
            ax.axvline(x=0, color='r', linestyle='--', linewidth=2)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
