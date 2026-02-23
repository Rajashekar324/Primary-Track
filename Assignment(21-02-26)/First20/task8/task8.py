from flask import Flask, request, redirect, url_for, render_template_string, abort
import sqlite3

app = Flask(__name__)
DB_NAME = "todo.db"

# -----------------------------
# DB helpers
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Home -> redirect to tasks
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("task_list"))

# -----------------------------
# LIST + ADD (Read + Create)
# -----------------------------
@app.route("/tasks", methods=["GET", "POST"])
def task_list():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            return "Title is required", 400

        conn = get_db()
        conn.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
        conn.commit()
        conn.close()
        return redirect(url_for("task_list"))

    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>To-Do App</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .box { max-width: 700px; }
            form { margin-bottom: 18px; }
            input[type="text"] { padding: 8px; width: 70%; }
            button { padding: 8px 12px; cursor: pointer; }
            .task { border: 1px solid #ddd; padding: 12px; margin: 10px 0; border-radius: 10px; }
            .done { text-decoration: line-through; color: #666; }
            .actions a { margin-right: 10px; }
            .badge { font-size: 12px; padding: 2px 8px; border: 1px solid #aaa; border-radius: 999px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>✅ To-Do App (Full CRUD)</h2>

            <form method="POST" action="{{ url_for('task_list') }}">
                <input type="text" name="title" placeholder="Enter new task..." />
                <button type="submit">Add</button>
            </form>

            {% if tasks %}
                {% for t in tasks %}
                    <div class="task">
                        <div>
                            <span class="{% if t['completed'] == 1 %}done{% endif %}">
                                <b>#{{ t['id'] }}</b> {{ t['title'] }}
                            </span>
                            {% if t['completed'] == 1 %}
                                <span class="badge">Completed</span>
                            {% else %}
                                <span class="badge">Pending</span>
                            {% endif %}
                        </div>

                        <div class="actions" style="margin-top:10px;">
                            <a href="{{ url_for('toggle_task', task_id=t['id']) }}">
                                {% if t['completed'] == 1 %}Mark Incomplete{% else %}Mark Complete{% endif %}
                            </a>
                            <a href="{{ url_for('edit_task', task_id=t['id']) }}">Edit</a>
                            <a href="{{ url_for('delete_task', task_id=t['id']) }}"
                               onclick="return confirm('Delete this task?')">Delete</a>
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <p>No tasks yet. Add one above 👆</p>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, tasks=tasks)

# -----------------------------
# TOGGLE COMPLETE (Update)
# -----------------------------
@app.route("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        abort(404)

    new_value = 0 if task["completed"] == 1 else 1
    conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_value, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("task_list"))

# -----------------------------
# EDIT PAGE (Update)
# -----------------------------
@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        abort(404)

    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        if not new_title:
            conn.close()
            return "Title is required", 400

        conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for("task_list"))

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Task</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input[type="text"] { padding: 8px; width: 350px; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h2>✏️ Edit Task #{{ task['id'] }}</h2>

        <form method="POST">
            <input type="text" name="title" value="{{ task['title'] }}" />
            <button type="submit">Save</button>
            <a href="{{ url_for('task_list') }}">Cancel</a>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, task=task)

# -----------------------------
# DELETE (Delete)
# -----------------------------
@app.route("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("task_list"))

# -----------------------------
# 404 handler (optional)
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
        <h2>404 - Not Found</h2>
        <p><a href="{{ url_for('task_list') }}">Go to Tasks</a></p>
    """), 404

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)