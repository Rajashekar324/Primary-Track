from flask import Flask, render_template_string, abort, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "products.db"

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # enables p["name"] and p.name
    return conn

# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    """)

    # Insert sample data if empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
            [
                ("Laptop", 65000, "Good for coding and office work"),
                ("Phone", 25000, "Fast performance with good camera"),
                ("Headphones", 2000, "Clear sound and comfortable fit"),
                ("Keyboard", 1500, "Mechanical keyboard"),
            ]
        )

    conn.commit()
    conn.close()

# -----------------------------
# HOME ROUTE (fixes 404 on /)
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("products"))

# -----------------------------
# PRODUCT LIST PAGE
# -----------------------------
@app.route("/products")
def products():
    conn = get_db()
    products_list = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Products</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .card { border: 1px solid #ddd; padding: 12px; margin: 10px 0; border-radius: 8px; }
            a { text-decoration: none; }
        </style>
    </head>
    <body>
        <h2>Product List</h2>

        {% if products %}
            {% for p in products %}
                <div class="card">
                    <b>{{ p["name"] }}</b> - ₹{{ p["price"] }} <br>
                    <a href="{{ url_for('product_detail', pid=p['id']) }}">View Details</a>
                </div>
            {% endfor %}
        {% else %}
            <p>No products found.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, products=products_list)

# -----------------------------
# PRODUCT DETAIL PAGE
# -----------------------------
@app.route("/products/<int:pid>")
def product_detail(pid):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    conn.close()

    if not product:
        abort(404)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ product["name"] }}</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .box { border: 1px solid #ddd; padding: 16px; border-radius: 10px; width: 350px; }
        </style>
    </head>
    <body>
        <h2>Product Detail</h2>

        <div class="box">
            <h3>{{ product["name"] }}</h3>
            <p><b>Price:</b> ₹{{ product["price"] }}</p>
            <p><b>Description:</b> {{ product["description"] }}</p>
        </div>

        <br>
        <a href="{{ url_for('products') }}">⬅ Back to Products</a>
    </body>
    </html>
    """
    return render_template_string(html, product=product)

# -----------------------------
# CUSTOM 404 PAGE (optional)
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
        <h2>404 - Page Not Found</h2>
        <p>Go back to <a href="{{ url_for('products') }}">Products</a></p>
    """), 404

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)