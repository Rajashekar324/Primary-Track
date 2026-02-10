import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db, login_manager
from models import User, Product
from flask import session

# ------------------
# APP CONFIG
# ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")

db.init_app(app)
login_manager.init_app(app)

# ------------------
# LOGIN MANAGER
# ------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------
# ROUTES
# ------------------
@app.route("/", methods=["GET"])
@login_required
def products():
    search = request.args.get("search")
    max_price = request.args.get("price")

    query = Product.query

    if search:
        query = query.filter(Product.name.contains(search))
    if max_price:
        query = query.filter(Product.price <= max_price)

    return render_template("products.html", products=query.all())


# ------------------
# AUTH
# ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("products"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# ------------------
# PRODUCT DETAIL PAGE
# ------------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get(product_id)

    if not product:
        return abort(404)
    
    related = Product.query.filter(
    Product.id != product.id,
    Product.price.between(product.price - 500, product.price + 500)
    ).limit(3).all()

    return render_template("product_detail.html", product=product, related=related)


# ------------------
# ADD PRODUCT (ADMIN)
# ------------------
@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        return "Unauthorized", 403

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]      # <-- IMPORTANT
        image = request.files["image"]

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        product = Product(
            name=name,
            price=price,
            description=description,                    # <-- SAVE DESCRIPTION
            image=filename
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for("products"))

    return render_template("add_products.html")

@app.route("/add-to-cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        return abort(404)

    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart

    return redirect(url_for("products"))

@app.route("/cart")
@login_required
def cart():
    cart_ids = session.get("cart", [])
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total = sum([p.price for p in products])
    return render_template("cart.html", products=products, total=total)

@app.route("/checkout")
@login_required
def checkout():
    cart_ids = session.get("cart", [])
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total = sum([p.price for p in products])

    # Clear cart after checkout
    session["cart"] = []

    return render_template("checkout.html", products=products, total=total)

    # clear cart after checkout
    session["cart"] = []

    return render_template("checkout.html", products=products, total=total)


@app.route("/delete-product/<int:product_id>")
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        return "Unauthorized", 403

    product = Product.query.get(product_id)
    if not product:
        return abort(404)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("products"))

# ------------------
# MAIN
# ------------------
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        db.create_all()

        # create admin if not exists
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                password="admin",
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
