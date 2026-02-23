import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vangala@2004",
    database="student_db",
)

@app.route("/")
def home():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template("students.html", students=students)

@app.route("/student/<int:id>")
def student_detail(id):
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    return render_template("student_detail.html", student=student)

if __name__ == "__main__":
    app.run(debug=True)