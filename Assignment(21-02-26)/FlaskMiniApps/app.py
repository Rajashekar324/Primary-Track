from flask import Flask, request, render_template, redirect, session, url_for
import mysql.connector
import random
import string

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------------------
# Database Connection
# ----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sum2004",
        database="flaskdb"
    )

# ----------------------------
# 1. Home
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------
# 2. Hello User
# ----------------------------
@app.route("/user/<name>")
def hello_user(name):
    return render_template("hello_user.html", name=name)

# ----------------------------
# 3. Student List Viewer
# ----------------------------
@app.route("/students")
def students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template("student_list.html", students=data)

# ----------------------------
# 4. Todo List Viewer
# ----------------------------
@app.route("/todos")
def todos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    data = cursor.fetchall()
    conn.close()
    return render_template("todo_list.html", todos=data)

# ----------------------------
# 5. Product List + Detail
# ----------------------------
@app.route("/products")
def products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    conn.close()
    return render_template("product_list.html", products=data)

@app.route("/products/<int:id>")
def product_detail(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template("product_detail.html", product=product)

# ----------------------------
# 6. Blog Viewer
# ----------------------------
@app.route("/blogs")
def blogs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blogs")
    data = cursor.fetchall()
    conn.close()
    return render_template("blog_list.html", blogs=data)

@app.route("/blogs/<int:id>")
def blog_detail(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blogs WHERE id=%s", (id,))
    blog = cursor.fetchone()
    conn.close()
    return render_template("blog_detail.html", blog=blog)

# ----------------------------
# 7. Employee Directory
# ----------------------------
@app.route("/employees")
def employees():
    dept = request.args.get("department")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if dept:
        cursor.execute("SELECT * FROM employees WHERE department=%s", (dept,))
    else:
        cursor.execute("SELECT * FROM employees")

    data = cursor.fetchall()
    conn.close()
    return render_template("employee_list.html", employees=data)

# ----------------------------
# 8. Quotes
# ----------------------------
@app.route("/quote")
def quote():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotes ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return render_template("quote.html", quote=data)

# ----------------------------
# 9. Todo CRUD
# ----------------------------
@app.route("/todo-crud")
def todo_crud():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    data = cursor.fetchall()
    conn.close()
    return render_template("todo_list_crud.html", todos=data)

@app.route("/todo-crud/add", methods=["POST"])
def add_todo():
    task = request.form["task"]
    status = request.form["status"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, status) VALUES (%s,%s)", (task, status))
    conn.commit()
    conn.close()
    return redirect("/todo-crud")

@app.route("/todo-crud/delete/<int:id>")
def delete_todo(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/todo-crud")

# ----------------------------
# 10. Student Management
# ----------------------------
@app.route("/student-mgmt")
def student_mgmt():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template("student_mgmt.html", students=data)

# ----------------------------
# 11. Notes
# ----------------------------
@app.route("/notes")
def notes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes")
    data = cursor.fetchall()
    conn.close()
    return render_template("notes_list.html", notes=data)

@app.route("/notes/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s,%s)", (title, content))
    conn.commit()
    conn.close()
    return redirect("/notes")

@app.route("/notes/delete/<int:id>")
def delete_note(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/notes")

# ----------------------------
# 12. Books
# ----------------------------
@app.route("/books")
def books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return render_template("book_list.html", books=data)

# ----------------------------
# 13. Movies
# ----------------------------
@app.route("/movies")
def movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    data = cursor.fetchall()
    conn.close()
    return render_template("movie_list.html", movies=data)

@app.route("/movies/<int:id>")
def movie_detail(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE id=%s", (id,))
    movie = cursor.fetchone()
    conn.close()
    return render_template("movie_detail.html", movie=movie)

# ----------------------------
# 14. Contacts
# ----------------------------
@app.route("/contacts")
def contacts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return render_template("contacts_list.html", contacts=data)

# ----------------------------
# 15. Inventory
# ----------------------------
@app.route("/inventory")
def inventory():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    conn.close()
    return render_template("inventory_list.html", items=data)

# ----------------------------
# 16. Login / Logout
# ----------------------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        return "Invalid Credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ----------------------------
# 17. Blog with Comments
# ----------------------------
@app.route("/blog-comments")
def blog_comments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template("blog_comments.html", posts=posts)

# ----------------------------
# 18. Ecommerce
# ----------------------------
@app.route("/ecommerce")
def ecommerce():
    category = request.args.get("category")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if category:
        cursor.execute("SELECT * FROM products WHERE category=%s", (category,))
    else:
        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()
    conn.close()
    return render_template("ecommerce_list.html", products=products)

# ----------------------------
# 19. Enrollment
# ----------------------------
@app.route("/enrollment")
def enrollment():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.name AS student_name, c.name AS course_name
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        JOIN courses c ON e.course_id = c.id
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("enrollment_list.html", enrollments=data)

# ----------------------------
# 20. Events
# ----------------------------
@app.route("/events")
def events():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events")
    data = cursor.fetchall()
    conn.close()
    return render_template("events_list.html", events=data)

# ----------------------------
# 21. URL Shortener
# ----------------------------
@app.route("/url-shortener", methods=["GET","POST"])
def url_shortener():
    if request.method == "POST":
        original_url = request.form["original_url"]
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (%s,%s)",
                       (original_url, code))
        conn.commit()
        conn.close()

        return f"Short URL: http://127.0.0.1:5000/s/{code}"

    return render_template("url_shortener.html")

@app.route("/s/<code>")
def redirect_url(code):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT original_url FROM urls WHERE short_code=%s", (code,))
    data = cursor.fetchone()
    conn.close()

    if data:
        return redirect(data["original_url"])
    return "URL Not Found"

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)