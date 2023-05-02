from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
            with sqlite3.connect("hw13.db") as con:
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