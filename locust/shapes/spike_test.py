from locust import LoadTestShape

class SpikeTest(LoadTestShape):
    """
    A shape to simulate a spike test to check system resilience and recovery.
    This shape corresponds to test case TC_SPIKE_05.

    - Spikes to 200 users in 30s.
    - Holds the load for 2 minutes.
    - Drops to a recovery load of 20 users and holds for 5 minutes.
    """
    stages = [
        # 1. Ramp up to 200 users in 30 seconds
        {"duration": 30, "users": 200, "spawn_rate": 200},
        # 2. Hold 200 users for 2 minutes (120 seconds)
        {"duration": 30 + 120, "users": 200, "spawn_rate": 200},
        # 3. Drop to 20 users and hold for 5 minutes to observe recovery
        {"duration": 30 + 120 + 300, "users": 20, "spawn_rate": 20},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None
