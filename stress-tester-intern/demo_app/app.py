import os, time, random, string
from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "alice": "alice123",
    "bob": "bob123",
    "charlie": "charlie123",
}

TOKENS = {}
PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 39.9},
    {"id": 2, "name": "Mouse", "price": 19.5},
    {"id": 3, "name": "Headphones", "price": 59.0},
    {"id": 4, "name": "Monitor", "price": 189.0},
    {"id": 5, "name": "USB-C Cable", "price": 9.9},
]

MIN_DELAY = int(os.getenv("APP_MIN_DELAY_MS", "50"))
MAX_DELAY = int(os.getenv("APP_MAX_DELAY_MS", "300"))
SPIKE_ERROR_RATE = float(os.getenv("APP_SPIKE_ERROR_RATE", "0.02"))

def maybe_delay():
    # simulate variable processing time
    delay = random.uniform(MIN_DELAY/1000.0, MAX_DELAY/1000.0)
    time.sleep(delay)

def make_token(n=24):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def auth_user():
    header = request.headers.get("Authorization", "")
    if header.startswith("Token "):
        token = header.split(" ", 1)[1].strip()
    elif header.startswith("Bearer "):
        token = header.split(" ", 1)[1].strip()
    else:
        return None
    return TOKENS.get(token)

@app.get("/")
def index():
    return jsonify({"ok": True, "message": "Demo API up"}), 200

@app.post("/auth/token/login")
def login():
    maybe_delay()
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if USERS.get(username) == password:
        token = make_token()
        TOKENS[token] = {"username": username}
        return jsonify({"auth_token": token}), 200
    return jsonify({"detail": "invalid credentials"}), 401

@app.get("/auth/users/me")
def me():
    maybe_delay()
    user = auth_user()
    if not user:
        return jsonify({"detail": "not authorized"}), 401
    return jsonify({"username": user["username"], "role": "customer"}), 200

@app.get("/products")
def products():
    maybe_delay()
    # simulate cache hit ratio by returning quickly sometimes
    if random.random() < 0.1:
        pass
    return jsonify({"items": PRODUCTS, "count": len(PRODUCTS)}), 200

@app.post("/cart/add")
def cart_add():
    maybe_delay()
    data = request.get_json(force=True, silent=True) or {}
    product_id = data.get("product_id")
    qty = int(data.get("qty", 1))
    if not any(p["id"] == product_id for p in PRODUCTS):
        return jsonify({"detail": "product not found"}), 404
    return jsonify({"added": {"product_id": product_id, "qty": qty}}), 200

@app.post("/checkout")
def checkout():
    maybe_delay()
    # random failure to emulate payment/gateway issues
    if random.random() < SPIKE_ERROR_RATE:
        return jsonify({"detail": "payment gateway error"}), 502
    return jsonify({"status": "ok", "order_id": make_token(8)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

