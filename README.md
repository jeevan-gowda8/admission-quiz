# 🎓 College Admission Quiz System

An online quiz system for college admission screening.
Students attempt a timed quiz, and only admins can view scores and results.

---

## 🛠 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Question Bank | Built-in (no API needed) |

---

## 📋 Prerequisites

- Python 3.8+ → https://www.python.org/downloads/
- MySQL 8.0+ → https://dev.mysql.com/downloads/installer/
- MySQL Workbench (comes with MySQL Installer)

---

## ⚙️ Installation Steps

### Step 1 — Install Python packages

```cmd
pip install flask mysql-connector-python
```

### Step 2 — Set up the Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE IF NOT EXISTS admission_quiz;
USE admission_quiz;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    reg_no VARCHAR(100) UNIQUE NOT NULL,
    attempted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_no VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    total INT DEFAULT 30,
    status ENUM('Selected', 'Rejected') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reg_no) REFERENCES students(reg_no)
);
```

### Step 3 — Configure MySQL Password

Open `app.py` and update:

```python
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'your_mysql_password_here',  # ← add your password
    'database': 'admission_quiz'
}
```

### Step 4 — Run the App

```cmd
cd C:\Users\YourName\Desktop\quiz_system
python app.py
```

Open browser → `http://localhost:5000`

---

## 🌐 Application URLs

| URL | Description |
|---|---|
| `http://localhost:5000` | Student login page |
| `http://localhost:5000/quiz` | Quiz page (requires login) |
| `http://localhost:5000/submitted` | After quiz submission |
| `http://localhost:5000/admin/login` | Admin login |
| `http://localhost:5000/admin/dashboard` | Admin results dashboard |

---

## 🔐 Login Credentials

### Student Login
- Name: Any student name
- Register Number: Any unique register number
- No password required
- Each register number can only attempt **once**

### Admin Login
- URL: `http://localhost:5000/admin/login`
- Password: `admin123`

---

## 📘 Quiz Details

| Property | Value |
|---|---|
| Total Questions | 30 |
| Time Limit | 20 minutes |
| Passing Score | 20 out of 30 |
| Question Type | Multiple Choice (4 options) |

### Subject Distribution

| Subject | Questions |
|---|---|
| Mathematics | 6 |
| Science | 6 |
| English | 5 |
| General Knowledge | 5 |
| Logical Reasoning | 4 |
| Basic Computer Knowledge | 4 |

---

## 🏆 Selection Criteria

| Score | Status |
|---|---|
| 20 or above | ✅ Selected |
| Below 20 | ❌ Rejected |

---

## 🗄️ Database Management

### View all students and results
```sql
USE admission_quiz;
SELECT * FROM students;
SELECT * FROM results;
```

### View full ranked report
```sql
USE admission_quiz;
SELECT s.name, r.reg_no, r.score, r.status, r.timestamp
FROM results r
JOIN students s ON s.reg_no = r.reg_no
ORDER BY r.score DESC;
```

### Delete a specific student (for re-testing)
```sql
USE admission_quiz;
DELETE FROM results WHERE reg_no = 'your_register_number';
DELETE FROM students WHERE reg_no = 'your_register_number';
```

### Delete ALL data and start fresh
```sql
USE admission_quiz;
DELETE FROM results;
DELETE FROM students;
```

---

## 📁 Project Structure

```
quiz_system/
│
├── app.py                   ← Main Flask application
├── requirements.txt         ← Python dependencies
├── README.md                ← This file
│
└── templates/
    ├── student_login.html   ← Student login page
    ├── quiz.html            ← Quiz page with timer
    ├── submitted.html       ← Confirmation after submission
    ├── admin_login.html     ← Admin login page
    └── admin_dashboard.html ← Admin results dashboard
```

---

## 🔒 Security Features

- Students can attempt the quiz only **once**
- Correct answers are **never sent to the browser**
- Quiz page is **session protected**
- Scores are **hidden from students**
- Admin dashboard is **password protected**
- Browser back button is **disabled** during quiz

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|---|---|
| `Access denied for user 'root'` | Add your MySQL password to `DB_CONFIG` in `app.py` |
| `Unknown database 'admission_quiz'` | Run the database setup SQL in MySQL Workbench |
| `mysql is not recognized` | Add MySQL bin folder to Windows PATH |
| `ModuleNotFoundError: flask` | Run `pip install flask mysql-connector-python` |
| `Can't connect to MySQL server` | Run `net start MySQL80` in cmd as Administrator |

---

## 🚀 Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Also change the last line of `app.py` to:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```
