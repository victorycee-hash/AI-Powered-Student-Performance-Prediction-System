# System Architecture

## Student Performance Dashboard v3.0

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                    (Streamlit Web Browser)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AUTHENTICATION LAYER                         │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  login.py    │───▶│   auth.py    │───▶│  database.py │      │
│  │              │    │              │    │              │      │
│  │ • Login UI   │    │ • User Auth  │    │ • MongoDB    │      │
│  │ • Signup UI  │    │ • Password   │    │ • Connection │      │
│  │ • Validation │    │   Hashing    │    │ • Collections│      │
│  │ • Forms      │    │ • Sessions   │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MAIN APPLICATION                            │
│                      (dashboard.py)                              │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Data Upload  │    │  ML Models   │    │  Analytics   │      │
│  │ • CSV Files  │    │ • Training   │    │ • Course     │      │
│  │ • Validation │    │ • Prediction │    │ • Semester   │      │
│  │ • Processing │    │ • Evaluation │    │ • Performance│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │Visualizations│    │  DB Ops      │    │  Export      │      │
│  │ • Heatmaps   │    │ • Save Data  │    │ • Download   │      │
│  │ • Box Plots  │    │ • Load Data  │    │   CSV        │      │
│  │ • Scatter    │    │ • User Data  │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                               │
│                    (MongoDB Atlas Cloud)                         │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  users          │  │  students       │  │  courses        │ │
│  │  Collection     │  │  Collection     │  │  Collection     │ │
│  │                 │  │                 │  │                 │ │
│  │ • username ◄──┐ │  │ • student_id   │  │ • course_code  │ │
│  │ • email       │ │  │ • hours_studied│  │ • title        │ │
│  │ • password    │ │  │ • course       │  │ • credits      │ │
│  │ • full_name   │ │  │ • CA score     │  │                │ │
│  │ • created_at  │ │  │ • exam_score   │  │                │ │
│  │ • last_login  │ │  │ • semester     │  │                │ │
│  │ • role        │ │  │ • uploaded_by ─┼──┘                │ │
│  │               │ │  │ • uploaded_at  │                    │ │
│  └───────────────┘ │  └────────────────┘  └──────────────────┘ │
│                    │                                             │
│  Indexes:          │  Indexes:                                  │
│  • username (unique)  • student_id                              │
│  • email (unique)    │  • uploaded_by                           │
│                      │  • uploaded_at                           │
│                      │  • course + semester                     │
└─────────────────────┴──────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│                                                                   │
│  • MongoDB Atlas Cluster (cluster0.tfooa5n.mongodb.net)         │
│  • Cloud Database Storage                                        │
│  • Automatic Backups                                             │
│  • High Availability                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Registration
```
User → login.py → auth.py → database.py → MongoDB (users collection)
```

### 2. User Login
```
User → login.py → auth.py → Verify Password → Create Session → Dashboard
```

### 3. Upload Student Data
```
User → Upload CSV → dashboard.py → Process Data → Display Tables
```

### 4. Save to Database
```
Dashboard → Get Data → Add Metadata → database.py → MongoDB (students collection)
```

### 5. Load from Database
```
User → Click Load → database.py → Query by username → Return Data → Display
```

---

## Security Flow

```
┌──────────────┐
│ User Enters  │
│   Password   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Bcrypt Hash │
│   Generated  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Stored in  │
│   MongoDB    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Login: Hash  │
│   Compared   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Session    │
│   Created    │
└──────────────┘
```

---

## File Dependencies

```
dashboard.py
    ├── login.py
    │   └── auth.py
    │       └── database.py
    ├── database.py
    └── [ML/Visualization Libraries]

init_db.py
    └── database.py
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.13 |
| **Database** | MongoDB Atlas |
| **Authentication** | Bcrypt |
| **ML/Analytics** | Scikit-learn, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Connection** | PyMongo |

---

## Deployment Architecture

```
┌─────────────────┐
│   Local Dev     │
│  localhost:8501 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   Streamlit     │─────▶│  MongoDB Atlas   │
│   Application   │      │  Cloud Database  │
└─────────────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│   Users Access  │
│   via Browser   │
└─────────────────┘
```

---

## Scalability

### Current Capacity
- **Users**: Unlimited
- **Data per User**: Unlimited
- **Concurrent Users**: 100+ (Streamlit default)
- **Database**: Cloud-based, auto-scaling

### Performance Optimization
- MongoDB indexes for fast queries
- Streamlit caching for connections
- Efficient data aggregation
- Lazy loading of large datasets

---

## Backup & Recovery

### MongoDB Atlas Features
- ✅ Automatic daily backups
- ✅ Point-in-time recovery
- ✅ Geographic redundancy
- ✅ High availability (99.95% uptime)

### Data Retention
- User accounts: Permanent
- Student data: Permanent
- Session data: Browser session only

---

**Architecture Version**: 3.0  
**Last Updated**: November 3, 2025
