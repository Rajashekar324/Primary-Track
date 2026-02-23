from flask import Flask, request, redirect, url_for, render_template_string, abort
import sqlite3

app = Flask(__name__)
DB_NAME = "blog.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return redirect(url_for("blog_list"))

# -----------------------------
# VIEW BLOG LIST (READ)
# -----------------------------
@app.route("/blogs")
def blog_list():
    conn = get_db()
    blogs = conn.execute("SELECT * FROM blogs ORDER BY id DESC").fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog CRUD</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .card { border:1px solid #ddd; padding:12px; border-radius:10px; margin:10px 0; }
            a { text-decoration:none; margin-right:10px; }
            .top { display:flex; gap:12px; align-items:center; }
            .btn { border:1px solid #aaa; padding:6px 10px; border-radius:8px; }
            small { color:#555; }
        </style>
    </head>
    <body>
        <div class="top">
            <h2 style="margin:0;">📝 Blog CRUD System</h2>
            <a class="btn" href="{{ url_for('create_blog') }}">+ Create Blog</a>
        </div>

        {% if blogs %}
            {% for b in blogs %}
                <div class="card">
                    <h3 style="margin:0 0 6px 0;">{{ b['title'] }}</h3>
                    <small>By {{ b['author'] }} | {{ b['created_at'] }}</small>
                    <p>{{ (b['content'][:150] ~ '...') if b['content']|length > 150 else b['content'] }}</p>

                    <a href="{{ url_for('view_blog', blog_id=b['id']) }}">View</a>
                    <a href="{{ url_for('edit_blog', blog_id=b['id']) }}">Edit</a>
                    <a href="{{ url_for('delete_blog', blog_id=b['id']) }}"
                       onclick="return confirm('Delete this blog?')">Delete</a>
                </div>
            {% endfor %}
        {% else %}
            <p>No blogs yet. Click <b>Create Blog</b>.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, blogs=blogs)

# -----------------------------
# CREATE BLOG (CREATE)
# -----------------------------
@app.route("/blogs/create", methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not author or not content:
            return "Title, Author, and Content are required", 400

        conn = get_db()
        conn.execute(
            "INSERT INTO blogs (title, author, content) VALUES (?, ?, ?)",
            (title, author, content)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("blog_list"))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Create Blog</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input, textarea { width: 520px; padding: 8px; margin: 6px 0; }
            textarea { height: 180px; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h2>➕ Create Blog</h2>
        <form method="POST">
            <input name="title" placeholder="Title" />
            <br>
            <input name="author" placeholder="Author" />
            <br>
            <textarea name="content" placeholder="Content..."></textarea>
            <br>
            <button type="submit">Create</button>
            <a href="{{ url_for('blog_list') }}">Cancel</a>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

# -----------------------------
# VIEW SINGLE BLOG (READ)
# -----------------------------
@app.route("/blogs/<int:blog_id>")
def view_blog(blog_id):
    conn = get_db()
    blog = conn.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,)).fetchone()
    conn.close()
    if not blog:
        abort(404)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ blog['title'] }}</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .box { border:1px solid #ddd; padding:16px; border-radius:12px; max-width:800px; }
            small { color:#555; }
        </style>
    </head>
    <body>
        <a href="{{ url_for('blog_list') }}">⬅ Back</a>
        <div class="box">
            <h2 style="margin:0 0 6px 0;">{{ blog['title'] }}</h2>
            <small>By {{ blog['author'] }} | {{ blog['created_at'] }}</small>
            <hr>
            <p style="white-space: pre-wrap;">{{ blog['content'] }}</p>
            <hr>
            <a href="{{ url_for('edit_blog', blog_id=blog['id']) }}">Edit</a>
            <a href="{{ url_for('delete_blog', blog_id=blog['id']) }}"
               onclick="return confirm('Delete this blog?')">Delete</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, blog=blog)

# -----------------------------
# EDIT BLOG (UPDATE)
# -----------------------------
@app.route("/blogs/<int:blog_id>/edit", methods=["GET", "POST"])
def edit_blog(blog_id):
    conn = get_db()
    blog = conn.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,)).fetchone()
    if not blog:
        conn.close()
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()
        if not title or not author or not content:
            conn.close()
            return "Title, Author, and Content are required", 400

        conn.execute(
            "UPDATE blogs SET title = ?, author = ?, content = ? WHERE id = ?",
            (title, author, content, blog_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("view_blog", blog_id=blog_id))

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Blog</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input, textarea { width: 520px; padding: 8px; margin: 6px 0; }
            textarea { height: 180px; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h2>✏️ Edit Blog</h2>
        <form method="POST">
            <input name="title" value="{{ blog['title'] }}" />
            <br>
            <input name="author" value="{{ blog['author'] }}" />
            <br>
            <textarea name="content">{{ blog['content'] }}</textarea>
            <br>
            <button type="submit">Save</button>
            <a href="{{ url_for('view_blog', blog_id=blog['id']) }}">Cancel</a>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, blog=blog)

# -----------------------------
# DELETE BLOG (DELETE)
# -----------------------------
@app.route("/blogs/<int:blog_id>/delete")
def delete_blog(blog_id):
    conn = get_db()
    conn.execute("DELETE FROM blogs WHERE id = ?", (blog_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("blog_list"))

@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
        <h2>404 - Not Found</h2>
        <p><a href="{{ url_for('blog_list') }}">Go to Blog List</a></p>
    """), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)