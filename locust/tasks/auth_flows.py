from locust import task, SequentialTaskSet, FastHttpUser, between
from locust.exception import StopUser
import random

# Import the config parser listener so it gets registered
from common import config

class AuthFlows(SequentialTaskSet):
    """
    Simulates a user journey that requires authentication:
    1. Login to get a token.
    2. Add a product to the cart.
    3. Checkout.
    """
    def on_start(self):
        """Called when a virtual user starts this TaskSet. Performs login."""
        self.token = None
        self.login()

    def login(self):
        """
        Logs in a user using credentials from the configuration
        (locust.conf, env var, or command line).
        """
        # Access the parsed options from the environment
        username = self.user.environment.parsed_options.username
        password = self.user.environment.parsed_options.password

        with self.client.post(
            "/auth/token/login",
            json={"username": username, "password": password},
            name="/auth/token/login",
            catch_response=True
        ) as resp:
            if resp.status_code == 200 and "auth_token" in resp.json():
                self.token = resp.json()["auth_token"]
                resp.success()
            else:
                resp.failure(f"Login failed for user '{username}' with status {resp.status_code}")
                # Stop the entire User, not just the task sequence.
                raise StopUser("Login failed, stopping user.")

    @task
    def view_profile(self):
        if not self.token:
            return
        with self.client.get(
            "/auth/users/me",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/auth/users/me",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"View profile failed with status {resp.status_code}")
                # Interrupt and restart the sequence from the beginning
                self.interrupt()

    @task
    def add_to_cart(self):
        if not self.token:
            return
        # choose random product id 1..5
        pid = random.randint(1, 5)
        with self.client.post(
            "/cart/add",
            json={"product_id": pid, "quantity": 1},
            headers={"Authorization": f"Bearer {self.token}"},
            name="/cart/add",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Add to cart failed with status {resp.status_code}")
                self.interrupt()

    @task
    def checkout(self):
        if not self.token:
            return
        with self.client.post(
            "/checkout",
            json={"payment_method": "visa"},
            headers={"Authorization": f"Bearer {self.token}"},
            name="/checkout",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Checkout failed with status {resp.status_code}")
        # After checkout, the sequence ends and will start over.

class PrivateUser(FastHttpUser):
    """
    A user that executes the authenticated flow sequentially.
    This user's behavior is defined by the AuthFlows TaskSet.
    """
    wait_time = between(0.3, 1.2)
    # host is configured in locust.conf or via --host
    tasks = [AuthFlows]
