from locust import FastHttpUser, task, between
import os, random

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

class PublicReader(FastHttpUser):
    wait_time = between(0.2, 1.5)

    @task(3)
    def list_products(self):
        with self.client.get(f"{BASE_URL}/products", name="GET /products", timeout=5, catch_response=True) as resp:
            if resp.status_code != 200 or "items" not in resp.text:
                resp.failure(f"Unexpected response {resp.status_code}")

    @task(1)
    def index(self):
        with self.client.get(f"{BASE_URL}/", name="GET /", timeout=3, catch_response=True) as resp:
            if resp.status_code != 200 or "ok" not in resp.json():
                resp.failure(f"Unexpected response {resp.status_code} or missing ok field")
