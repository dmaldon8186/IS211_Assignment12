from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "password"

logged_in = False 

def insert_data():
    conn = sqlite3.connect('hw13.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (id, first_name, last_name) VALUES (1, 'John', 'Smith')")
    c.execute("INSERT INTO quizzes (id, subject, num_questions, date_given) VALUES (1, 'Python Basics', 5, 'February 5, 2015')")
    c.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (1, 1, 85)")
    conn.commit()
    conn.close()

@app.before_first_request
def before_first_request():
    insert_data()

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

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/addrec', methods = ['POST', 'GET'])

def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            quiz = request.form['quiz']
            results = request.form['results']
            with sqlite3.connect("hw13") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, quiz, results) VALUES (?,?,?)", (name, quiz, results))
                con.commit()
                msg = "Quiz Records Updated"
        except:
            con.rollback()
            msg = "ERROR, record cannot be added."
        finally:
            con.close()
            return render_template("quiz.html", msg = msg)
        
@app.route('/liststudents')

def listStudents():
    con = sqlite3.connect("hw13.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall();
    return render_template("dashboard.html", rows = rows)

if __name__ == '__main__':
    app.run()