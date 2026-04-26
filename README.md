# College Admission Quiz System — Setup Guide

## Prerequisites
- Python 3.8+
- MySQL 8.0+
- OpenAI API key

---

## 1. Database Setup

```bash
mysql -u root -p < schema.sql
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

The app runs at **http://localhost:5000**

---

## URL Routes

| Route | Description |
|-------|-------------|
| `/` | Redirects to student login |
| `/student/login` | Student login page |
| `/quiz` | Quiz page (session required) |
| `/submitted` | Post-submission confirmation |
| `/admin/login` | Admin login |
| `/admin/dashboard` | Admin results dashboard |
| `/admin/logout` | Logout admin |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate_quiz` | GET | Generates 30 AI questions (session required) |
| `/api/submit_quiz` | POST | Submits answers, saves score |

---

## Selection Criteria

- Score ≥ 20 / 30 → **Selected**
- Score < 20 / 30 → **Rejected**

---

## Security Notes

- Students can only attempt once (enforced DB + session)
- Quiz answers are never sent to the client
- Admin dashboard is session-protected
- Direct URL access to `/quiz` without login is blocked
- Browser back button is disabled on the quiz page

---

## Production Deployment

For production, use **Gunicorn** + **Nginx**:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Set `DEBUG=False` in production by modifying the last line of `app.py`.
