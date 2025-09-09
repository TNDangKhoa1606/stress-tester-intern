# Bảng Thiết Kế Test Case Hiệu Năng

Tài liệu này chi tiết hóa các kịch bản kiểm thử hiệu năng sẽ được thực thi, theo cấu trúc bảng chi tiết.

---

**Pre-condition:** Hệ thống demo API đã được khởi chạy qua Docker và có thể truy cập tại `http://localhost:8000`.

| ID | Description (Mô tả) | Number of virtual users (Số người dùng ảo) | Running time (Thời gian chạy) | Steps (Các bước thực hiện) | Expected Result (Kết quả mong đợi) | Actual Result | Notes (Ghi chú) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **STRESS_RAMP_01** | **Ramp-up Test (Khởi động):** "Làm nóng" hệ thống và kiểm tra hiệu năng cơ bản ở tải thấp. | Tăng dần từ 0 đến 60 VU (Virtual Users). Spawn rate: 12 VU/phút. | 10 phút (5 phút ramp + 5 phút ổn định). | 1. Chạy Locust UI: `locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py --config locust/locust.conf`<br>2. Thiết lập ramp-up từ 0 đến 60 VU trong 5 phút.<br>3. Giám sát biểu đồ thời gian thực trên UI (RPS, p95, error rate). | - **Pass:** p95 ≤ 800ms, error rate <1%, RPS ≥50 ở cuối ramp.<br>- **Fail:** p95 >800ms hoặc error rate ≥1% trước 60 VU.<br>- Hệ thống hoạt động ổn định, không có lỗi bất thường. | (Để trống) | - Dữ liệu: Sử dụng public_read.py và auth_flows.py với users alice/bob/charlie.<br>- Think time: between(0.2, 1.5)s.<br>- Thu thập: Screenshot UI + export CSV từ Locust. |
| **STRESS_STEP_02** | **Step-Stress Test (Tìm điểm gãy):** Xác định breakpoint của hệ thống bằng cách tăng tải theo từng bậc. | Các bậc: Bậc 1: 20 VU (5p), Bậc 2: 50 VU (5p), Bậc 3: 100 VU (5p), Bậc 4: 150 VU (5p), Bậc 5: 200 VU (5p). Spawn rate: 10 VU/phút giữa bậc. | 25 phút (5 phút mỗi bậc). | 1. Sử dụng custom shape: locust/shapes/stress_shape.py.<br>2. Chạy headless: `locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py --host http://localhost:8000 --headless --run-time 25m --step-load-shape stress_shape.StepStress --html locust/reports/stress.html --csv locust/reports/stress`<br>3. Theo dõi p95 và error rate ở cuối mỗi bậc. | - **Pass:** Mỗi bậc p95 ≤800ms, error rate <1%, RPS tăng ≥150 ở bậc 3+.<br>- **Fail:** Bậc nào p95 >800ms hoặc error rate ≥1% (breakpoint tại VU/RPS bậc đó). Dừng nếu error ≥5% trong 2 phút.<br>- Xác định chính xác breakpoint. | (Để trống) | - Dữ liệu: GET /products (3 tasks), auth flow (login + cart/add + checkout). Sử dụng data.csv với 5 users.<br>- Think time: between(0.3, 1.2)s.<br>- Thu thập: Bảng "Bậc → p95/error/RPS" từ CSV/HTML. |
| **STRESS_SPIKE_03** | **Spike Test (Kiểm tra phục hồi):** Đánh giá khả năng chịu sốc tải và phục hồi của hệ thống. | - GĐ1: 0 → 200 VU (30s).<br>- GĐ2: Giữ 200 VU (60s).<br>- GĐ3: Giảm về 20 VU (5p). Spawn rate: 400 VU/phút spike, -360 VU/phút recovery. | 7 phút. | 1. Tạo custom shape cho spike hoặc dùng UI để điều chỉnh thủ công.<br>2. Chạy headless: `locust -f locust/tasks/auth_flows.py --host http://localhost:8000 --headless -u 20 -r 400 -t 7m --html locust/reports/spike.html --csv locust/reports/spike`<br>3. Quan sát p95 trong/sau spike. | - **Pass:** Spike: p95 ≤1200ms, error <3%; Sau 2 phút: p95 ≤800ms, error <1%, RPS ≥100.<br>- **Fail:** Không phục hồi sau 3 phút (p95 >800ms) hoặc error ≥5% kéo dài.<br>- Thời gian phục hồi <60s. | (Để trống) | - Dữ liệu: Auth flow đầy đủ (login → add_to_cart → checkout) với 5 users, product_id ngẫu nhiên (1-5).<br>- Think time: between(0.2, 1.0)s.<br>- Thu thập: p95 spike, thời gian phục hồi từ chart timeline CSV/HTML. |

**Ghi chú chung cho tất cả test cases:**
- **Validation:** Đã thêm validation vào Locust scripts với catch_response=True, kiểm tra status_code 200 và JSON fields bắt buộc. Ví dụ snippets code:
  - GET /products: `if resp.status_code != 200 or "items" not in resp.text: resp.failure(...)`
  - GET / (index): `if resp.status_code != 200 or "ok" not in resp.json(): resp.failure(...)`
  - GET /auth/users/me: `if resp.status_code != 200 or "username" not in resp.json(): resp.failure(...)`
  - POST /cart/add: `if resp.status_code != 200 or "added" not in resp.json(): resp.failure(...)`
  - POST /checkout: `if resp.status_code != 200 or "status" not in resp.json(): resp.failure(...)`
  - POST /auth/token/login (on_start): `if r.status_code == 200 and "auth_token" in r.json(): ... else: events.request_failure.fire(...)`
- **Rủi ro:** Chỉ chạy local. Dừng khẩn cấp nếu error rate ≥5% trong 2 phút.
- **Công cụ:** Locust UI cho debug, headless cho báo cáo tự động.
- **KPI từ test_plan.md:** p95 ≤800ms, error <1%, RPS ≥150.
