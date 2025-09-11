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

### 5) Run Locust (UI)
```bash
locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py --config locust/locust.conf
# open http://localhost:8089
```

### 6) Run headless stress (example)
```bash
locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py   --host http://localhost:8000   --headless -u 120 -r 30 -t 10m   --html locust/reports/stress.html --csv locust/reports/stress
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
