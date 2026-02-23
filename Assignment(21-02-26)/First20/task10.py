from flask import Flask, request, redirect, url_for, render_template_string, abort
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return redirect(url_for("student_list"))

# -----------------------------
# VIEW LIST (READ)
# -----------------------------
@app.route("/students")
def student_list():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student CRUD</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; width: 820px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align:left; }
            th { background:#f5f5f5; }
            a { text-decoration:none; margin-right:10px; }
            .btn { border:1px solid #aaa; padding:6px 10px; border-radius:8px; }
        </style>
    </head>
    <body>
        <h2>🎓 Student Management System (CRUD)</h2>
        <a class="btn" href="{{ url_for('add_student') }}">+ Add Student</a>
        <br><br>

        {% if students %}
        <table>
            <tr>
                <th>ID</th><th>Name</th><th>Age</th><th>Course</th><th>Actions</th>
            </tr>
            {% for s in students %}
            <tr>
                <td>{{ s['id'] }}</td>
                <td>{{ s['name'] }}</td>
                <td>{{ s['age'] }}</td>
                <td>{{ s['course'] }}</td>
                <td>
                    <a href="{{ url_for('edit_student', student_id=s['id']) }}">Edit</a>
                    <a href="{{ url_for('delete_student', student_id=s['id']) }}"
                       onclick="return confirm('Delete this student?')">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
            <p>No students yet.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# -----------------------------
# ADD STUDENT (CREATE)
# -----------------------------
@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        course = request.form.get("course", "").strip()

        if not name or not age.isdigit() or not course:
            return "Name, valid Age, and Course are required", 400

        conn = get_db()
        conn.execute(
            "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
            (name, int(age), course)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("student_list"))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Student</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input { width: 360px; padding: 8px; margin: 6px 0; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h2>➕ Add Student</h2>
        <form method="POST">
            <input name="name" placeholder="Name" />
            <br>
            <input name="age" placeholder="Age (number)" />
            <br>
            <input name="course" placeholder="Course" />
            <br>
            <button type="submit">Add</button>
            <a href="{{ url_for('student_list') }}">Cancel</a>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

# -----------------------------
# EDIT STUDENT (UPDATE)
# -----------------------------
@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        course = request.form.get("course", "").strip()

        if not name or not age.isdigit() or not course:
            conn.close()
            return "Name, valid Age, and Course are required", 400

        conn.execute(
            "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
            (name, int(age), course, student_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("student_list"))

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input { width: 360px; padding: 8px; margin: 6px 0; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h2>✏️ Edit Student #{{ student['id'] }}</h2>
        <form method="POST">
            <input name="name" value="{{ student['name'] }}" />
            <br>
            <input name="age" value="{{ student['age'] }}" />
            <br>
            <input name="course" value="{{ student['course'] }}" />
            <br>
            <button type="submit">Save</button>
            <a href="{{ url_for('student_list') }}">Cancel</a>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

# -----------------------------
# DELETE STUDENT (DELETE)
# -----------------------------
@app.route("/students/<int:student_id>/delete")
def delete_student(student_id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("student_list"))

@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
        <h2>404 - Not Found</h2>
        <p><a href="{{ url_for('student_list') }}">Go to Students</a></p>
    """), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)