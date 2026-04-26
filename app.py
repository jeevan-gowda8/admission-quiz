from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import random
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'admission_quiz_secret_2024')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

DB_CONFIG = {
    'host':     os.environ.get('DB_HOST',     'localhost'),
    'user':     os.environ.get('DB_USER',     'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME',     'admission_quiz'),
    'port':     int(os.environ.get('DB_PORT', 3306)),
}

# ─── QUESTION BANK ────────────────────────────────────────────────────────────
QUESTION_BANK = {
    "Mathematics": [
        {"question": "What is the value of √144?", "options": ["10", "11", "12", "13"], "answer": "C", "difficulty": "easy"},
        {"question": "What is 15% of 200?", "options": ["25", "30", "35", "40"], "answer": "B", "difficulty": "easy"},
        {"question": "If 3x = 27, what is x?", "options": ["6", "7", "8", "9"], "answer": "D", "difficulty": "easy"},
        {"question": "What is the area of a rectangle with length 8 cm and width 5 cm?", "options": ["35 cm²", "40 cm²", "45 cm²", "50 cm²"], "answer": "B", "difficulty": "easy"},
        {"question": "What is the LCM of 4 and 6?", "options": ["8", "10", "12", "14"], "answer": "C", "difficulty": "easy"},
        {"question": "What is 2³ + 3²?", "options": ["15", "16", "17", "18"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the perimeter of a square with side 7 cm?", "options": ["21 cm", "28 cm", "35 cm", "49 cm"], "answer": "B", "difficulty": "easy"},
        {"question": "Which of these is a prime number?", "options": ["9", "15", "17", "21"], "answer": "C", "difficulty": "easy"},
        {"question": "What is 25% of 80?", "options": ["15", "20", "25", "30"], "answer": "B", "difficulty": "easy"},
        {"question": "If a triangle has angles 60° and 80°, what is the third angle?", "options": ["30°", "40°", "50°", "60°"], "answer": "B", "difficulty": "medium"},
        {"question": "What is the HCF of 12 and 18?", "options": ["3", "6", "9", "12"], "answer": "B", "difficulty": "medium"},
        {"question": "A train travels 180 km in 3 hours. What is its speed?", "options": ["50 km/h", "55 km/h", "60 km/h", "65 km/h"], "answer": "C", "difficulty": "medium"},
    ],
    "Science": [
        {"question": "What is the chemical symbol for water?", "options": ["WO", "H2O", "HO2", "W2O"], "answer": "B", "difficulty": "easy"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Vacuole"], "answer": "C", "difficulty": "easy"},
        {"question": "What gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": "C", "difficulty": "easy"},
        {"question": "How many bones are in the adult human body?", "options": ["196", "206", "216", "226"], "answer": "B", "difficulty": "easy"},
        {"question": "What is the unit of electric current?", "options": ["Volt", "Watt", "Ampere", "Ohm"], "answer": "C", "difficulty": "easy"},
        {"question": "Which organ pumps blood throughout the body?", "options": ["Liver", "Lungs", "Kidney", "Heart"], "answer": "D", "difficulty": "easy"},
        {"question": "What is the speed of light approximately?", "options": ["2x10⁸ m/s", "3x10⁸ m/s", "4x10⁸ m/s", "5x10⁸ m/s"], "answer": "B", "difficulty": "medium"},
        {"question": "Which of these is a conductor of electricity?", "options": ["Rubber", "Wood", "Copper", "Plastic"], "answer": "C", "difficulty": "easy"},
        {"question": "What force pulls objects toward Earth?", "options": ["Magnetic force", "Friction", "Gravity", "Tension"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the chemical formula for table salt?", "options": ["KCl", "NaCl", "CaCl2", "MgCl2"], "answer": "B", "difficulty": "medium"},
        {"question": "Which part of the plant makes food using sunlight?", "options": ["Root", "Stem", "Leaf", "Flower"], "answer": "C", "difficulty": "easy"},
    ],
    "English": [
        {"question": "What is the plural of 'child'?", "options": ["Childs", "Childes", "Children", "Childrens"], "answer": "C", "difficulty": "easy"},
        {"question": "Which word is a synonym for 'happy'?", "options": ["Sad", "Angry", "Joyful", "Tired"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the past tense of 'run'?", "options": ["Runned", "Ran", "Runed", "Running"], "answer": "B", "difficulty": "easy"},
        {"question": "Which sentence is grammatically correct?", "options": ["She don't like it.", "She doesn't likes it.", "She doesn't like it.", "She not like it."], "answer": "C", "difficulty": "easy"},
        {"question": "What is the antonym of 'ancient'?", "options": ["Old", "Modern", "Historic", "Aged"], "answer": "B", "difficulty": "easy"},
        {"question": "Which word is spelled correctly?", "options": ["Accomodate", "Accommodate", "Acommodate", "Acomodate"], "answer": "B", "difficulty": "medium"},
        {"question": "Choose the correct article: '___ apple a day keeps the doctor away.'", "options": ["A", "An", "The", "No article"], "answer": "B", "difficulty": "easy"},
        {"question": "What part of speech is the word 'quickly'?", "options": ["Noun", "Verb", "Adjective", "Adverb"], "answer": "D", "difficulty": "easy"},
        {"question": "Which is the correct passive voice of 'She wrote a letter'?", "options": ["A letter was written by her.", "A letter is written by her.", "A letter were written by her.", "A letter has written by her."], "answer": "A", "difficulty": "medium"},
        {"question": "What does the idiom 'break the ice' mean?", "options": ["Break something cold", "Start a conversation", "End a friendship", "Cause trouble"], "answer": "B", "difficulty": "medium"},
    ],
    "General Knowledge": [
        {"question": "Who is known as the Father of the Nation in India?", "options": ["Jawaharlal Nehru", "B.R. Ambedkar", "Mahatma Gandhi", "Sardar Patel"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the capital of India?", "options": ["Mumbai", "Kolkata", "Chennai", "New Delhi"], "answer": "D", "difficulty": "easy"},
        {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "answer": "C", "difficulty": "easy"},
        {"question": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Ganges", "Yangtze"], "answer": "B", "difficulty": "easy"},
        {"question": "Which country invented paper?", "options": ["India", "Egypt", "China", "Greece"], "answer": "C", "difficulty": "easy"},
        {"question": "What is the national animal of India?", "options": ["Lion", "Elephant", "Tiger", "Leopard"], "answer": "C", "difficulty": "easy"},
        {"question": "Which is the largest ocean in the world?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "D", "difficulty": "easy"},
        {"question": "In which year did India gain independence?", "options": ["1945", "1946", "1947", "1948"], "answer": "C", "difficulty": "easy"},
        {"question": "Who wrote the Indian National Anthem?", "options": ["Bankim Chandra", "Rabindranath Tagore", "Sarojini Naidu", "Subramanya Bharathi"], "answer": "B", "difficulty": "easy"},
        {"question": "Which planet is the largest in our solar system?", "options": ["Saturn", "Neptune", "Uranus", "Jupiter"], "answer": "D", "difficulty": "easy"},
    ],
    "Logical Reasoning": [
        {"question": "What comes next in the series: 2, 4, 8, 16, ___?", "options": ["24", "28", "32", "36"], "answer": "C", "difficulty": "easy"},
        {"question": "Find the odd one out: Apple, Mango, Carrot, Banana", "options": ["Apple", "Mango", "Carrot", "Banana"], "answer": "C", "difficulty": "easy"},
        {"question": "What comes next: Monday, Wednesday, Friday, ___?", "options": ["Saturday", "Sunday", "Monday", "Tuesday"], "answer": "B", "difficulty": "easy"},
        {"question": "A is taller than B. B is taller than C. Who is the shortest?", "options": ["A", "B", "C", "Cannot determine"], "answer": "C", "difficulty": "easy"},
        {"question": "If 5 + 3 = 28 and 9 + 1 = 810, then 7 + 2 = ?", "options": ["59", "63", "514", "95"], "answer": "C", "difficulty": "medium"},
        {"question": "What comes next: 1, 4, 9, 16, ___?", "options": ["20", "24", "25", "30"], "answer": "C", "difficulty": "easy"},
        {"question": "If all cats are animals and some animals are wild, which is definitely true?", "options": ["All cats are wild", "Some cats may be wild", "No cats are wild", "All animals are cats"], "answer": "B", "difficulty": "medium"},
        {"question": "Complete the pattern: AZ, BY, CX, ___?", "options": ["DE", "DW", "EW", "DX"], "answer": "B", "difficulty": "medium"},
    ],
    "Basic Computer Knowledge": [
        {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Core Processing Unit"], "answer": "A", "difficulty": "easy"},
        {"question": "Which of these is an input device?", "options": ["Monitor", "Printer", "Keyboard", "Speaker"], "answer": "C", "difficulty": "easy"},
        {"question": "What does 'www' stand for in a website address?", "options": ["World Wide Web", "World Web Wide", "Wide World Web", "Web World Wide"], "answer": "A", "difficulty": "easy"},
        {"question": "Which key is used to delete text to the left of the cursor?", "options": ["Delete", "Backspace", "Escape", "Shift"], "answer": "B", "difficulty": "easy"},
        {"question": "What is the full form of RAM?", "options": ["Read Access Memory", "Random Access Memory", "Rapid Access Memory", "Read All Memory"], "answer": "B", "difficulty": "easy"},
        {"question": "Which of these is a web browser?", "options": ["Microsoft Word", "Google Chrome", "VLC Player", "Notepad"], "answer": "B", "difficulty": "easy"},
        {"question": "What does PDF stand for?", "options": ["Portable Document Format", "Printed Document File", "Personal Data Format", "Public Document File"], "answer": "A", "difficulty": "easy"},
        {"question": "Which shortcut key is used to copy selected text?", "options": ["Ctrl+X", "Ctrl+V", "Ctrl+C", "Ctrl+Z"], "answer": "C", "difficulty": "easy"},
    ]
}

# ─── QUIZ GENERATION ──────────────────────────────────────────────────────────
def generate_quiz():
    distribution = {
        "Mathematics": 6, "Science": 6, "English": 5,
        "General Knowledge": 5, "Logical Reasoning": 4,
        "Basic Computer Knowledge": 4,
    }
    selected = []
    qid = 1
    for subject, count in distribution.items():
        pool = QUESTION_BANK[subject].copy()
        random.shuffle(pool)
        for q in pool[:count]:
            selected.append({
                "id": qid, "subject": subject,
                "difficulty": q["difficulty"], "question": q["question"],
                "options": q["options"], "answer": q["answer"],
            })
            qid += 1
    random.shuffle(selected)
    for i, q in enumerate(selected, 1):
        q["id"] = i
    return selected

# ─── DB HELPERS ───────────────────────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS admission_quiz CHARACTER SET utf8mb4")
    cur.execute("USE admission_quiz")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            reg_no VARCHAR(100) UNIQUE NOT NULL,
            attempted BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reg_no VARCHAR(100) NOT NULL,
            score INT NOT NULL,
            total INT DEFAULT 30,
            status ENUM('Selected', 'Rejected') NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reg_no) REFERENCES students(reg_no)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# ─── AUTH DECORATORS ──────────────────────────────────────────────────────────
def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'student_reg' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─── STUDENT ROUTES ───────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('student_login'))

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        name   = request.form.get('name',   '').strip()
        reg_no = request.form.get('reg_no', '').strip()
        if not name or not reg_no:
            return render_template('student_login.html', error="Please fill all fields.")

        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cur.fetchone()

        if student:
            if student['attempted']:
                cur.close(); conn.close()
                return render_template('student_login.html',
                    error="You have already attempted this quiz. Multiple attempts are not allowed.")
            cur.execute("UPDATE students SET name=%s WHERE reg_no=%s", (name, reg_no))
        else:
            cur.execute("INSERT INTO students (name, reg_no) VALUES (%s, %s)", (name, reg_no))

        conn.commit()
        cur.close(); conn.close()
        session['student_reg']  = reg_no
        session['student_name'] = name
        return redirect(url_for('quiz'))

    return render_template('student_login.html')

@app.route('/quiz')
@student_required
def quiz():
    reg_no = session['student_reg']
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT attempted FROM students WHERE reg_no = %s", (reg_no,))
    student = cur.fetchone()
    cur.close(); conn.close()
    if not student or student['attempted']:
        session.clear()
        return redirect(url_for('student_login'))
    return render_template('quiz.html', student_name=session['student_name'], reg_no=reg_no)

@app.route('/api/generate_quiz')
@student_required
def api_generate_quiz():
    reg_no = session['student_reg']
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT attempted FROM students WHERE reg_no = %s", (reg_no,))
    student = cur.fetchone()
    cur.close(); conn.close()
    if not student or student['attempted']:
        return jsonify({'error': 'Already attempted'}), 403
    questions = generate_quiz()
    client_questions = [
        {'id': q['id'], 'subject': q['subject'],
         'difficulty': q['difficulty'], 'question': q['question'],
         'options': q['options']}
        for q in questions
    ]
    session['quiz_questions'] = questions
    return jsonify(client_questions)

@app.route('/api/submit_quiz', methods=['POST'])
@student_required
def submit_quiz():
    reg_no = session['student_reg']
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT attempted FROM students WHERE reg_no = %s", (reg_no,))
    student = cur.fetchone()
    if not student or student['attempted']:
        cur.close(); conn.close()
        return jsonify({'error': 'Already submitted'}), 403
    data         = request.get_json()
    user_answers = data.get('answers', {})
    questions    = session.get('quiz_questions', [])
    if not questions:
        cur.close(); conn.close()
        return jsonify({'error': 'No quiz data found'}), 400
    score  = sum(1 for q in questions if user_answers.get(str(q['id'])) == q['answer'])
    status = 'Selected' if score >= 20 else 'Rejected'
    cur.execute("INSERT INTO results (reg_no, score, total, status) VALUES (%s,%s,%s,%s)",
                (reg_no, score, 30, status))
    cur.execute("UPDATE students SET attempted=TRUE WHERE reg_no=%s", (reg_no,))
    conn.commit()
    cur.close(); conn.close()
    session.pop('quiz_questions', None)
    session['quiz_submitted'] = True
    return jsonify({'success': True})

@app.route('/submitted')
def submitted():
    if not session.get('quiz_submitted') and not session.get('student_reg'):
        return redirect(url_for('student_login'))
    return render_template('submitted.html', name=session.get('student_name', ''))

# ─── ADMIN ROUTES ─────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password', '') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error="Invalid password.")
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.name, r.reg_no, r.score, r.total, r.status, r.timestamp,
               RANK() OVER (ORDER BY r.score DESC) AS `rank`
        FROM results r
        JOIN students s ON s.reg_no = r.reg_no
        ORDER BY r.score DESC
    """)
    results = cur.fetchall()
    cur.execute("SELECT COUNT(*) AS total    FROM students WHERE attempted=TRUE")
    stats    = cur.fetchone()
    cur.execute("SELECT COUNT(*) AS selected FROM results  WHERE status='Selected'")
    selected = cur.fetchone()
    cur.execute("SELECT COUNT(*) AS rejected FROM results  WHERE status='Rejected'")
    rejected = cur.fetchone()
    cur.close(); conn.close()
    return render_template('admin_dashboard.html',
                           results=results,
                           total_attempted=stats['total'],
                           total_selected=selected['selected'],
                           total_rejected=rejected['rejected'])

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
