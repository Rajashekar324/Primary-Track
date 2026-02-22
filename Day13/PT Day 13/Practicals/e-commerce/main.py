from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
import uuid

app = FastAPI(title="E-Commerce Web + REST API")

# ✅ REQUIRED so login session works
app.add_middleware(SessionMiddleware, secret_key="SOME_RANDOM_SECRET_123")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# In-memory DB
# -----------------------------
users_db: Dict[str, Dict[str, str]] = {}
items_db: Dict[int, Dict[str, Any]] = {}
orders_db: Dict[str, Dict[str, Any]] = {}
cart_db: Dict[str, Dict[int, int]] = {}
next_item_id = 1


# -----------------------------
# Models for /items endpoints
# -----------------------------
class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)


# -----------------------------
# Helpers
# -----------------------------
def get_user(request: Request) -> Optional[str]:
    return request.session.get("username")


def require_login(request: Request) -> Optional[str]:
    u = get_user(request)
    return u


def get_item_or_404(item_id: int) -> Dict[str, Any]:
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def compute_cart(username: str) -> Dict[str, Any]:
    user_cart = cart_db.get(username, {})
    out_items = []
    subtotal = 0.0

    for item_id, qty in user_cart.items():
        item = items_db.get(item_id)
        if not item:
            continue
        line_total = float(item["price"]) * qty
        subtotal += line_total
        out_items.append(
            {
                "item_id": item_id,
                "title": item["title"],
                "price": float(item["price"]),
                "quantity": qty,
                "line_total": line_total,
            }
        )

    return {"items": out_items, "subtotal": subtotal}


# -----------------------------
# Landing
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if get_user(request):
        return RedirectResponse("/home", status_code=302)
    return RedirectResponse("/login", status_code=302)


# -----------------------------
# AUTH
# -----------------------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    username = username.strip()
    password = password.strip()

    user = users_db.get(username)
    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
            status_code=400,
        )

    request.session["username"] = username
    cart_db.setdefault(username, {})

    # ✅ IMPORTANT: 303 after POST
    return RedirectResponse("/home", status_code=303)


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    username = username.strip()
    password = password.strip()

    if len(username) < 3:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username must be at least 3 characters"}, status_code=400)
    if len(password) < 3:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Password must be at least 3 characters"}, status_code=400)
    if username in users_db:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"}, status_code=400)

    users_db[username] = {"password": password}
    cart_db.setdefault(username, {})

    return RedirectResponse("/login", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


# -----------------------------
# HOME (Protected)
# -----------------------------
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    username = require_login(request)
    if not username:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse(
        "home_auth.html",
        {
            "request": request,
            "username": username,
            "items": list(items_db.values()),
            "cart": compute_cart(username),
            "last_order_id": request.session.get("last_order_id"),
            "last_order_amount": request.session.get("last_order_amount"),
        },
    )


# -----------------------------
# Upload (Protected)
# -----------------------------
@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("upload.html", {"request": request, "error": None})


@app.post("/upload", response_class=HTMLResponse)
async def upload_post(request: Request, title: str = Form(...), file: UploadFile = File(...)):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)

    title = title.strip()
    if not title:
        return templates.TemplateResponse("upload.html", {"request": request, "error": "Title is required"}, status_code=400)
    if not file or not file.filename:
        return templates.TemplateResponse("upload.html", {"request": request, "error": "Please choose a file"}, status_code=400)

    content = await file.read()
    safe_name = f"{uuid.uuid4().hex}_{os.path.basename(file.filename)}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(save_path, "wb") as f:
        f.write(content)

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "title": title, "filename": file.filename, "saved_as": safe_name, "size": len(content)},
    )


# ============================================================
# REST API: /items (for Postman + your tests)
# ============================================================
@app.get("/items")
def get_items():
    return list(items_db.values())


@app.post("/items", status_code=201)
def create_item(payload: ItemCreate):
    global next_item_id
    item_id = next_item_id
    next_item_id += 1

    item = {
        "id": item_id,
        "title": payload.title,
        "description": payload.description,
        "price": float(payload.price),
        "stock": int(payload.stock),
    }
    items_db[item_id] = item
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, payload: ItemUpdate):
    item = get_item_or_404(item_id)
    data = payload.model_dump(exclude_unset=True)

    for k, v in data.items():
        item[k] = v

    items_db[item_id] = item
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    get_item_or_404(item_id)
    items_db.pop(item_id, None)

    # remove from all carts
    for u in cart_db:
        cart_db[u].pop(item_id, None)

    return {"message": "Item deleted"}


# ============================================================
# UI Actions from Home page (forms)
# ============================================================
@app.post("/ui/add-item")
def ui_add_item(request: Request, title: str = Form(...), price: float = Form(...), stock: int = Form(...), description: str = Form("")):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)

    create_item(ItemCreate(title=title.strip(), description=description.strip() or None, price=price, stock=stock))
    return RedirectResponse("/home", status_code=303)


@app.post("/ui/update-item")
def ui_update_item(request: Request, item_id: int = Form(...), title: str = Form(""), price: str = Form(""), stock: str = Form(""), description: str = Form("")):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)

    data: Dict[str, Any] = {}
    if title.strip():
        data["title"] = title.strip()
    if description.strip():
        data["description"] = description.strip()
    if price.strip():
        data["price"] = float(price)
    if stock.strip():
        data["stock"] = int(stock)

    update_item(item_id, ItemUpdate(**data))
    return RedirectResponse("/home", status_code=303)


@app.post("/ui/delete-item")
def ui_delete_item(request: Request, item_id: int = Form(...)):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)
    delete_item(item_id)
    return RedirectResponse("/home", status_code=303)


@app.post("/ui/add-to-cart")
def ui_add_to_cart(request: Request, item_id: int = Form(...), quantity: int = Form(...)):
    username = require_login(request)
    if not username:
        return RedirectResponse("/login", status_code=302)

    item = get_item_or_404(item_id)
    if item["stock"] <= 0:
        return RedirectResponse("/home", status_code=303)

    user_cart = cart_db.setdefault(username, {})
    new_qty = user_cart.get(item_id, 0) + int(quantity)
    if new_qty > item["stock"]:
        new_qty = item["stock"]
    user_cart[item_id] = new_qty

    return RedirectResponse("/home", status_code=303)


@app.post("/ui/remove-from-cart")
def ui_remove_from_cart(request: Request, item_id: int = Form(...), quantity: int = Form(1)):
    username = require_login(request)
    if not username:
        return RedirectResponse("/login", status_code=302)

    user_cart = cart_db.setdefault(username, {})
    if item_id in user_cart:
        user_cart[item_id] -= int(quantity)
        if user_cart[item_id] <= 0:
            user_cart.pop(item_id, None)

    return RedirectResponse("/home", status_code=303)


@app.post("/ui/checkout")
def ui_checkout(request: Request, name: str = Form(...), address: str = Form(...), payment_method: str = Form(...)):
    username = require_login(request)
    if not username:
        return RedirectResponse("/login", status_code=302)

    cart = compute_cart(username)
    if not cart["items"]:
        return RedirectResponse("/home", status_code=303)

    # reduce stock
    for ci in cart["items"]:
        item = get_item_or_404(ci["item_id"])
        if ci["quantity"] > item["stock"]:
            return RedirectResponse("/home", status_code=303)
        item["stock"] -= ci["quantity"]
        items_db[ci["item_id"]] = item

    order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"
    orders_db[order_id] = {
        "order_id": order_id,
        "username": username,
        "customer": {"name": name.strip(), "address": address.strip()},
        "payment_method": payment_method,
        "subtotal": cart["subtotal"],
        "status": "PENDING_PAYMENT" if payment_method in ("CARD", "UPI") else "CONFIRMED",
        "items": cart["items"],
    }

    cart_db[username] = {}
    request.session["last_order_id"] = order_id
    request.session["last_order_amount"] = cart["subtotal"]

    return RedirectResponse("/home", status_code=303)


@app.post("/ui/payment")
def ui_payment(request: Request, order_id: str = Form(...), method: str = Form(...), amount: float = Form(...)):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)

    order = orders_db.get(order_id)
    if not order:
        return RedirectResponse("/home", status_code=303)

    if float(amount) != float(order["subtotal"]):
        return RedirectResponse("/home", status_code=303)

    order["status"] = "CONFIRMED"
    order["paid_via"] = method
    orders_db[order_id] = order

    return RedirectResponse("/home", status_code=303)
