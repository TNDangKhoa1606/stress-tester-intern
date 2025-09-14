from locust import LoadTestShape

class StepStress(LoadTestShape):
    """
    Increase load stepwise to find a breakpoint.
    Each stage runs for duration seconds at a target user count.
    """
    stages = [
        {"duration": 60,  "users": 10,  "spawn_rate": 5},
        {"duration": 120, "users": 30,  "spawn_rate": 10},
        {"duration": 180, "users": 60,  "spawn_rate": 20},
        {"duration": 240, "users": 100, "spawn_rate": 25},
        {"duration": 300, "users": 150, "spawn_rate": 30},
    ]

    def tick(self):
        run_time = self.get_run_time()
        cumulative_duration = 0
        for stage in self.stages:
            cumulative_duration += stage["duration"]
            if run_time < cumulative_duration:
                return (stage["users"], stage["spawn_rate"])
        return None
