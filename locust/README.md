# Stress Tester Intern – Starter Pack (Locust + Docker demo app)

This repo gives your intern everything to run safe, local stress tests:
- A **Flask demo API** in Docker (`demo_app`) with endpoints for login/products/cart/checkout.
- **Locust scripts** (`locust/`) with public and auth flows, plus a step-stress LoadTestShape.
- A ready **workshop plan** and commands to run locally.

## Quick Start

### 1) Prereqs
- Docker + Docker Compose
- Python 3.10+

### 2) Start the demo API
```bash
docker compose up --build -d
# API will be available at http://localhost:8000

# Verify that the API is running
curl http://localhost:8000
# Expected output: {"ok":true}
```

### 3) Create a virtualenv and install Locust
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r locust/requirements.txt
```

### 4) (Optional) Configure environment
Create `.env` (or export env vars) if you want to override defaults:
```
BASE_URL=http://localhost:8000
USER_NAME=alice
USER_PASS=alice123
```

## How to Run Tests (Runbook)

This section provides detailed instructions for running different test scenarios.

### 1. Run with Web UI (UI Mode) 

Use this command to start Locust and open the web interface at `http://localhost:8089`.

```bash
# Run basic flows
locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py --config locust/locust.conf
```

**From the UI, you can customize:**

*   **Number of users**: Total concurrent users (VUs).
*   **Spawn rate**: Number of VUs to start per second.
*   **Host**: The target system's URL (e.g., `http://localhost:8000`).

### 2. Run without Web UI (Headless Mode)

This mode is ideal for automation (CI/CD) or long-duration tests. Reports will be saved to the `locust/reports/` directory.

```bash
# Example: Run a test for 10 minutes with 100 users
locust -f locust/locustfile.py --config locust/locust.conf --headless \
  --users 100 --spawn-rate 10 --run-time 10m \
  --html locust/reports/headless_report.html \
  --csv locust/reports/headless_report
```

### 3. Run Custom Load Shapes

Complex load patterns like Step-Stress or Spike tests are defined in the `locust/shapes` directory. To run them, you need to specify the corresponding `shape-class`.

```bash
# Run the Step-Stress shape
locust -f locust/locustfile.py --config locust/locust.conf --headless --shape-class StepStressShape \
  --html locust/reports/step_stress.html
```

```bash
# Run the Spike Test shape
locust -f locust/locustfile.py --config locust/locust.conf --headless --shape-class SpikeTestShape \
  --html locust/reports/spike_test.html
```

### 4. Override Parameters via Command Line

You can override values from `locust.conf` or the UI by passing command-line arguments.

```bash
# Override host, user count, and run time
locust -f locust/locustfile.py --headless \
  --host http://custom-host:8080 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 5m
```

> **Ethics & safety:** Do not stress public websites without permission. This pack is meant for local/demo testing.

## Endpoints (demo app)

- `POST /auth/token/login` → `{ "auth_token": "..." }` for valid users.
- `GET /auth/users/me` → current user profile.
- `GET /products` → product catalog (with random latency).
- `POST /cart/add` → add item to cart (random latency).
- `POST /checkout` → simulate payment (may randomly fail 1–3%).

## Default test users

- `alice` / `alice123`
- `bob` / `bob123`
- `charlie` / `charlie123`  
- `logan` / `logan123`
- `stark` / `stark123`
- `tobey` / `tobey123`


## Workshop outline

- Load vs Stress vs Spike vs Soak (SLO/SLA, p50/p95/p99, error rate).
- Design journeys: public browse vs auth flow.
- Demo Locust UI (ramp → step stress → spike).
- Report & interpret: breakpoint, recovery, recommendations.