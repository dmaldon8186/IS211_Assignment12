from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "password"
DATABASE = 'hw13.db'

logged_in = False 

@app.route('/')
def home():
    if not logged_in: 
        return redirect('/login')
    return redirect('/dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    error = None
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            logged_in = True
            return redirect('/dashboard')
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM Students')
    students = c.fetchall()
    c.execute('SELECT * FROM Quizzes')
    quizzes = c.fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO Students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            return render_template('add_student.html', error=str(e))
        
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':
        return render_template('add_quiz.html')
    elif request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        date_given = request.form['date_given']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO Quizzes (subject, num_questions, date_given) VALUES (?, ?, ?)', (subject, num_questions, date_given))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            return render_template('add_quiz.html', error=str(e))
        
@app.route('/student/<int:id>')
def student_results(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM students WHERE student_id=?", (id,))
    student = cursor.fetchone()
    if not student:
        return "No Results"
    cursor.execute("SELECT quizzes.subject, results.quiz_id, results.score FROM results INNER JOIN quizzes ON results.quiz_id = quizzes.quiz_id WHERE results.student_id=?", (id,))
    results = cursor.fetchall()
    return render_template('student_results.html', student=student, results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        grade = request.form['grade']
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)", (student_id, quiz_id, grade))
            conn.commit()
            return redirect('/dashboard')
    else:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            cur.execute("SELECT * FROM quizzes")
            quizzes = cur.fetchall()
        return render_template('add_result.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    app.run()