from locust import FastHttpUser, task, between, events
import os, random

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
USER = os.getenv("USER_NAME", "alice")
PWD = os.getenv("USER_PASS", "alice123")

class PrivateUser(FastHttpUser):
    wait_time = between(0.3, 1.2)
    token = None
    headers = {"Content-Type": "application/json"}

    def on_start(self):
        r = self.client.post(
            f"{BASE_URL}/auth/token/login",
            json={"username": USER, "password": PWD},
            name="POST /auth/token/login",
            timeout=5
        )
        if r.status_code == 200 and "auth_token" in r.json():
            self.token = r.json()["auth_token"]
            self.headers["Authorization"] = f"Token {self.token}"
        else:
            events.request_failure.fire(request_type="POST", name="login_failed", response_time=0, response=r)

    @task(2)
    def view_profile(self):
        if not self.token: return
        self.client.get(
            f"{BASE_URL}/auth/users/me",
            headers=self.headers,
            name="GET /auth/users/me",
            timeout=5
        )

    @task(2)
    def add_to_cart(self):
        # choose random product id 1..5
        pid = random.randint(1, 5)
        self.client.post(
            f"{BASE_URL}/cart/add",
            json={"product_id": pid, "qty": 1},
            headers=self.headers if self.token else None,
            name="POST /cart/add",
            timeout=5
        )

    @task(1)
    def checkout(self):
        self.client.post(
            f"{BASE_URL}/checkout",
            json={"payment_method": "visa"},
            headers=self.headers if self.token else None,
            name="POST /checkout",
            timeout=8
        )
