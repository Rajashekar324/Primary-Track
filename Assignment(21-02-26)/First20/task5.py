from flask import Flask, render_template_string, abort, redirect, url_for

app = Flask(__name__)

# -----------------------------
# STATIC BLOG DATA (like DB)
# -----------------------------
BLOGS = [
    {
        "id": 1,
        "title": "Python Basics",
        "author": "Rajashekar",
        "date": "2026-02-21",
        "content": "Python is a beginner-friendly language. It is used in web, data, AI, and automation."
    },
    {
        "id": 2,
        "title": "Flask Templates",
        "author": "Rajashekar",
        "date": "2026-02-21",
        "content": "Flask uses Jinja2 templates. You can use loops, if conditions, and variables in HTML."
    },
    {
        "id": 3,
        "title": "REST API Intro",
        "author": "Rajashekar",
        "date": "2026-02-21",
        "content": "A REST API is a web service that uses HTTP methods like GET, POST, PUT, DELETE."
    }
]

def get_blog(blog_id: int):
    return next((b for b in BLOGS if b["id"] == blog_id), None)

# -----------------------------
# HOME (redirect to blogs)
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("blog_list"))

# -----------------------------
# BLOG LIST PAGE
# -----------------------------
@app.route("/blogs")
def blog_list():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog List</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .card { border: 1px solid #ddd; padding: 12px; margin: 10px 0; border-radius: 10px; }
            a { text-decoration: none; }
            small { color: #555; }
        </style>
    </head>
    <body>
        <h2>Blog List</h2>

        {% for blog in blogs %}
            <div class="card">
                <h3>{{ blog.title }}</h3>
                <small>By {{ blog.author }} | {{ blog.date }}</small><br><br>
                <a href="{{ url_for('blog_detail', blog_id=blog.id) }}">Read More →</a>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, blogs=BLOGS)

# -----------------------------
# BLOG DETAIL PAGE
# -----------------------------
@app.route("/blogs/<int:blog_id>")
def blog_detail(blog_id):
    blog = get_blog(blog_id)
    if not blog:
        abort(404)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ blog.title }}</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .box { border: 1px solid #ddd; padding: 16px; border-radius: 10px; max-width: 700px; }
            small { color: #555; }
        </style>
    </head>
    <body>
        <a href="{{ url_for('blog_list') }}">⬅ Back to Blogs</a>
        <h2>{{ blog.title }}</h2>
        <small>By {{ blog.author }} | {{ blog.date }}</small>

        <div class="box">
            <p>{{ blog.content }}</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, blog=blog)

# -----------------------------
# CUSTOM 404
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
        <h2>404 - Blog Not Found</h2>
        <p>Go to <a href="{{ url_for('blog_list') }}">Blog List</a></p>
    """), 404

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)