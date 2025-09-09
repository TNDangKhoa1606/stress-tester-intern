# Bảng Thiết Kế Test Case Hiệu Năng

Tài liệu này chi tiết hóa các kịch bản kiểm thử hiệu năng sẽ được thực thi, theo cấu trúc bảng chi tiết.

---

**Pre-condition:** Hệ thống demo API đã được khởi chạy qua Docker và có thể truy cập tại `http://localhost:8000`.

| ID | Description | Number of virtual users | Running time | Step | Expected | Actual | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_RAMP_01** | **Ramp-up Test (Khởi động):** "Làm nóng" hệ thống và kiểm tra hiệu năng ở tải cơ bản. | 0 → 60 VU | 10 phút | 1. Chạy Locust với ramp-up từ 0 đến 60 VU trong 5 phút.<br>2. Giữ tải ổn định trong 5 phút.<br>3. Giám sát biểu đồ thời gian thực. | - Luồng `/products`: p95 ≤ 800ms, error < 0.5%.<br>- Luồng `Auth`: p95 ≤ 1000ms, error < 1%. | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_STEP_VU_02** | **Step-Stress Test (by VU):** Tìm điểm gãy (breakpoint) bằng cách tăng số người dùng ảo (VU) theo từng bậc. | Bậc: 60 → 90 → 120 VU | 24 phút (8 phút/bậc) | 1. Sử dụng custom `LoadTestShape` để định nghĩa các bậc tải.<br>2. Chạy headless và xuất báo cáo.<br>3. Theo dõi p95 và error rate ở cuối mỗi bậc. | Xác định được **Breakpoint** (bậc tải đầu tiên mà `p95` hoặc `error rate` vượt SLO). | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_STEP_CAR_03** | **Step-Stress Test (by Arrival Rate):** Tìm điểm gãy (breakpoint) bằng cách tăng tỷ lệ request (RPS) theo từng bậc. | N/A (Theo RPS: 50 → 210) | 40 phút (8 phút/bậc) | 1. Sử dụng custom `LoadTestShape` để điều khiển arrival-rate theo các bậc: 50 → 100 → 150 → 180 → 210 RPS.<br>2. Chạy headless và xuất báo cáo. | - **Pass:** Đạt mục tiêu ≥ 150 RPS ổn định trong 8 phút mà không vi phạm SLO.<br>- **Fail:** Xác định được breakpoint (RPS) trước khi đạt mục tiêu. | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_SPIKE_04** | **Spike Test (Kiểm tra phục hồi):** Đánh giá khả năng chịu sốc tải và phục hồi của hệ thống. | Spike: 0 → 200 VU (30s) | ~7.5 phút | 1. Tăng đột ngột lên 200 VU trong 30s.<br>2. Giữ tải trong 2 phút.<br>3. Giảm về 20 VU và theo dõi 5 phút. | Đo được **Thời gian phục hồi** (thời gian để p95 quay về dưới 1000ms). **Pass** nếu < 120 giây. | | - Mix: 100% Auth Flow<br>- Pacing: 0.2-1.0s<br>- Công cụ: Locust |
| **TC_SOAK_05** | **Soak Test (Kiểm tra độ bền):** Tìm rò rỉ bộ nhớ/tài nguyên khi chạy tải ổn định trong thời gian dài. | ~100 VU (tương đương 120 RPS) | 60 phút | 1. Chạy headless với tải không đổi (80% breakpoint) trong 60 phút.<br>2. Theo dõi biểu đồ p95, error rate, CPU, memory của server theo thời gian. | - **Pass:** p95, error rate, CPU, memory duy trì ổn định.<br>- **Fail:** Có hiện tượng suy giảm hiệu năng (latency drift), hoặc error rate/memory/CPU tăng dần. | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |

**Ghi chú chung cho tất cả test cases:**
- **Validation:** Đã thêm validation vào Locust scripts với catch_response=True, kiểm tra status_code 200 và JSON fields bắt buộc. Ví dụ snippets code:
  - GET /products: `if resp.status_code != 200 or "items" not in resp.text: resp.failure(...)`
  - GET / (index): `if resp.status_code != 200 or "ok" not in resp.json(): resp.failure(...)`
  - GET /auth/users/me: `if resp.status_code != 200 or "username" not in resp.json(): resp.failure(...)`
  - POST /cart/add: `if resp.status_code != 200 or "added" not in resp.json(): resp.failure(...)`
  - POST /checkout: `if resp.status_code != 200 or "status" not in resp.json(): resp.failure(...)`
  - POST /auth/token/login (on_start): `if r.status_code == 200 and "auth_token" in r.json(): ... else: events.request_failure.fire(...)`
- **Rủi ro & An toàn:** Chỉ chạy local. Dừng khẩn cấp nếu error rate ≥5% trong cửa sổ trượt 120 giây.
- **Công cụ:** Locust UI cho debug, headless cho báo cáo tự động.
- **Tham chiếu:** Tất cả các ngưỡng SLO và định nghĩa chi tiết được tham chiếu từ file `docs/test_plan.md`.
