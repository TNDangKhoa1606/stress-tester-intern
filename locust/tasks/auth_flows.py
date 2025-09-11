from locust import FastHttpUser, task, between, events
import os, random, csv, itertools

# Build an absolute path to the data.csv file to ensure the script runs correctly from any location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "common", "data.csv")

try:
    with open(DATA_FILE, "r") as f:
        # Create a cycling iterator from the CSV data, so we don't run out of users
        user_credentials = itertools.cycle(list(csv.DictReader(f)))
except FileNotFoundError:
    print(f"CRITICAL: Data file not found at '{DATA_FILE}'. Auth flow will fail.")
    user_credentials = itertools.cycle([{"username": "error", "password": "error"}])

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class PrivateUser(FastHttpUser):
    wait_time = between(0.3, 1.2)

    def on_start(self):
        # Get the next credentials from the iterator for this virtual user instance
        credentials = next(user_credentials)
        self.username = credentials["username"]
        self.password = credentials["password"]

        # Initialize instance-specific attributes
        self.token = None
        self.headers = {"Content-Type": "application/json"}

        with self.client.post(
            f"{BASE_URL}/auth/token/login",
            json={"username": self.username, "password": self.password},
            name="POST /auth/token/login",
            timeout=5,
            catch_response=True,
        ) as resp:
            if resp.status_code == 200 and "auth_token" in resp.json():
                self.token = resp.json()["auth_token"]
                self.headers["Authorization"] = f"Token {self.token}"
            else:
                resp.failure(f"Login failed for user '{self.username}' with status {resp.status_code} - {resp.text}")
                # Dừng user ảo này lại vì không có token thì các task sau cũng sẽ lỗi
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
                resp.failure(f"Unexpected response {resp.status_code} or missing username field")

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
                resp.failure(f"Unexpected response {resp.status_code} or missing added field")

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
                resp.failure(f"Unexpected response {resp.status_code} or missing status field")