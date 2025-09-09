# Bảng Thiết Kế Test Case Hiệu Năng

Tài liệu này chi tiết hóa các kịch bản kiểm thử hiệu năng sẽ được thực thi, theo cấu trúc bảng chi tiết.

---

**Pre-condition:** Hệ thống demo API đã được khởi chạy qua Docker và có thể truy cập tại `http://localhost:8000`.

| ID | Test Case / Mục tiêu | Mô hình tải (Load Profile) | Phân bổ tải & Pacing | Các bước thực hiện | Tiêu chí Pass/Fail & Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_RAMP_01** | **Ramp-up Test (Khởi động):** "Làm nóng" hệ thống và kiểm tra hiệu năng ở tải cơ bản. | Tăng dần từ 0 đến 60 VU trong 5 phút, sau đó giữ tải ổn định trong 5 phút. | - **Mix:** 80% `GET /products`, 20% `Auth Flow`.<br>- **Pacing:** 0.5s - 2.0s. | 1. Chạy Locust với các task file tương ứng.<br>2. Thiết lập ramp-up từ 0 đến 60 VU trong 5 phút, thời gian chạy tổng 10 phút.<br>3. Giám sát biểu đồ thời gian thực. | - Hệ thống hoạt động ổn định.<br>- **Luồng `/products`:** p95 ≤ 800ms, error < 0.5%.<br>- **Luồng `Auth`:** p95 ≤ 1000ms, error < 1%. |
| **TC_STEP_VU_02** | **Step-Stress Test (by VU):** Tìm điểm gãy (breakpoint) bằng cách tăng số người dùng ảo (VU) theo từng bậc. | Các bậc: 60 VU → 90 VU → 120 VU. Mỗi bậc giữ trong 8 phút. | - **Mix:** 80% `GET /products`, 20% `Auth Flow`.<br>- **Pacing:** 0.5s - 2.0s. | 1. Sử dụng custom `LoadTestShape` để định nghĩa các bậc tải.<br>2. Chạy headless và xuất báo cáo.<br>3. Theo dõi p95 và error rate ở cuối mỗi bậc. | - **Kết quả:** Xác định được **Breakpoint** (bậc tải đầu tiên mà `p95` vượt SLO trong ≥3 phút hoặc `error rate` vượt SLO trong ≥1 phút).<br>- **Pass:** Hoàn thành tất cả các bậc mà không vi phạm SLO.<br>- **Fail:** Xác định được breakpoint ở một bậc cụ thể. |
| **TC_STEP_CAR_03** | **Step-Stress Test (by Arrival Rate):** Tìm điểm gãy (breakpoint) bằng cách tăng tỷ lệ request (RPS) theo từng bậc. | Các bậc: 50 → 100 → 150 → 180 → 210 RPS. Mỗi bậc giữ trong 8 phút. | - **Mix:** 80% `GET /products`, 20% `Auth Flow`.<br>- **Pacing:** 0.5s - 2.0s. | 1. Sử dụng custom `LoadTestShape` để điều khiển arrival-rate.<br>2. Chạy headless và xuất báo cáo.<br>3. Theo dõi p95 và error rate ở cuối mỗi bậc. | - **Kết quả:** Xác định được **Breakpoint (RPS)**.<br>- **Pass:** Đạt mục tiêu `≥ 150 RPS` ổn định trong 8 phút mà không vi phạm SLO.<br>- **Fail:** Xác định được breakpoint (RPS) trước khi đạt mục tiêu. |
| **TC_SPIKE_04** | **Spike Test (Kiểm tra phục hồi):** Đánh giá khả năng chịu sốc tải và phục hồi của hệ thống. | - GĐ1: 0 → 200 VU (30s).<br>- GĐ2: Giữ 200 VU (2 phút).<br>- GĐ3: Giảm về 20 VU và theo dõi 5 phút. | - **Mix:** 100% `Auth Flow` (tập trung vào luồng nhạy cảm).<br>- **Pacing:** 0.2s - 1.0s. | 1. Sử dụng custom `LoadTestShape` cho kịch bản spike.<br>2. Chạy headless và xuất báo cáo.<br>3. Quan sát p95 và error rate trong và sau spike. | - **Kết quả:** Đo **Thời gian phục hồi** (thời gian để p95 quay về dưới 1000ms).<br>- **Pass:** Thời gian phục hồi < 120 giây.<br>- **Fail:** Không phục hồi sau 3 phút hoặc hệ thống treo. |
| **TC_SOAK_05** | **Soak Test (Kiểm tra độ bền):** Tìm rò rỉ bộ nhớ/tài nguyên khi chạy tải ổn định trong thời gian dài. | Chạy ở mức 80% breakpoint (ví dụ: 120 RPS hoặc 100 VU) trong 60 phút. | - **Mix:** 80% `GET /products`, 20% `Auth Flow`.<br>- **Pacing:** 0.5s - 2.0s. | 1. Chạy headless với tải không đổi trong 60 phút.<br>2. Theo dõi biểu đồ p95, error rate, CPU, memory của server theo thời gian. | - **Pass:** p95, error rate, CPU, memory duy trì ổn định trong suốt 60 phút.<br>- **Fail:** Có hiện tượng suy giảm hiệu năng (latency drift), hoặc error rate/memory/CPU tăng dần theo thời gian. |

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
