from locust import FastHttpUser, task, between, events
import os, random, csv, itertools

try:
    with open("locust/common/data.csv", "r") as f:
        user_credentials = itertools.cycle(list(csv.DictReader(f)))
except FileNotFoundError:
    print("QUAN TRỌNG: Không tìm thấy file data.csv. Luồng xác thực sẽ thất bại.")
    user_credentials = itertools.cycle([{"username": "error", "password": "error"}])

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class PrivateUser(FastHttpUser):
    wait_time = between(0.3, 1.2)

    def on_start(self):
        # Lấy tài khoản tiếp theo từ iterator cho người dùng ảo này
        credentials = next(user_credentials)
        self.username = credentials["username"]
        self.password = credentials["password"]

        # Khởi tạo các thuộc tính riêng cho instance này
        self.token = None
        self.headers = {"Content-Type": "application/json"}

        r = self.client.post(
            f"{BASE_URL}/auth/token/login",
            json={"username": self.username, "password": self.password},
            name="POST /auth/token/login",
            timeout=5,
        )
        if r.status_code == 200 and "auth_token" in r.json():
            self.token = r.json()["auth_token"]
            self.headers["Authorization"] = f"Token {self.token}"
        else:
            # events.request_failure.fire(
            #     request_type="POST", name="login_failed", response_time=0, response=r
            # )

            # Nếu đăng nhập thất bại, dừng người dùng ảo này lại vì các task sau cũng sẽ lỗi
            self.stop()

    @task(2)
    def view_profile(self):
        if not self.token:
            return
        with self.client.get(
            f"{BASE_URL}/auth/users/me",
            headers=self.headers,
            name="GET /auth/users/me",
            timeout=5,
            catch_response=True,
        ) as resp:
            if resp.status_code != 200 or "username" not in resp.json():
                resp.failure(
                    f"Unexpected response {resp.status_code} or missing username field"
                )

    @task(2)
    def add_to_cart(self):
        # choose random product id 1..5
        pid = random.randint(1, 5)
        with self.client.post(
            f"{BASE_URL}/cart/add",
            json={"product_id": pid, "qty": 1},
            headers=self.headers if self.token else None,
            name="POST /cart/add",
            timeout=5,
            catch_response=True,
        ) as resp:
            if resp.status_code != 200 or "added" not in resp.json():
                resp.failure(
                    f"Unexpected response {resp.status_code} or missing added field"
                )

    @task(1)
    def checkout(self):
        with self.client.post(
            f"{BASE_URL}/checkout",
            json={"payment_method": "visa"},
            headers=self.headers if self.token else None,
            name="POST /checkout",
            timeout=8,
            catch_response=True,
        ) as resp:
            if resp.status_code != 200 or "status" not in resp.json():
                resp.failure(
                    f"Unexpected response {resp.status_code} or missing status field"
                )
