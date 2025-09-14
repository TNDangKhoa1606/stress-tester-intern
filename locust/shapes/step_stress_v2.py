from locust import LoadTestShape

class StepStressV2(LoadTestShape):
    """
    A step-load shape to find the breakpoint by increasing concurrency (VUs).
    This version is designed based on expert review to align with Locust's
    closed workload model.

    - Each stage runs for 5 minutes.
    - The duration in `stages` is cumulative.
    """
    stages = [
        {"duration": 5 * 60,  "users": 25, "spawn_rate": 10},
        {"duration": 10 * 60, "users": 50, "spawn_rate": 15},
        {"duration": 15 * 60, "users": 75, "spawn_rate": 20},
        {"duration": 20 * 60, "users": 90, "spawn_rate": 25},
        {"duration": 25 * 60, "users": 110, "spawn_rate": 30},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None