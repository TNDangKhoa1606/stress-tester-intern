from locust import HttpUser
from tasks.public_read import PublicReader
from tasks.auth_flows import PrivateUser
from shapes.step_stress_v2 import StepStressV2


class WebsiteUser(HttpUser):
    tasks = {PublicReader: 4, PrivateUser: 1}
    host = "http://localhost:8000"
