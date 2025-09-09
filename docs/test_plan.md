# Kế Hoạch Kiểm Thử Hiệu Năng (Test Plan)

**Tài liệu này mô tả kế hoạch thực hiện stress test cho ứng dụng demo E-commerce.**


## 1. Mục Tiêu (Objectives)

*   **Tìm điểm gãy (Breakpoint):** Xác định số lượng người dùng đồng thời (Concurrent Users) và/hoặc số yêu cầu mỗi giây (RPS) tối đa mà endpoint `GET /products` có thể chịu được trước khi hiệu năng suy giảm đáng kể (vượt ngưỡng SLO).
*   **Đánh giá khả năng phục hồi (Resilience):** Kiểm tra khả năng hệ thống phục hồi về trạng thái ổn định sau khi một lượng lớn người dùng truy cập đột ngột (spike) vào luồng `Đăng nhập -> Thêm vào giỏ hàng -> Thanh toán`.


## 2. Phạm Vi (Scope)

### Các luồng nghiệp vụ chính được kiểm thử:

1.  **Luồng đọc công khai:**
    *   `GET /products`
2.  **Luồng mua hàng (Authenticated Flow):**
    *   `POST /auth/token/login`
    *   `POST /cart/add`
    *   `POST /checkout`

**Ghi chú:** Endpoint `GET /auth/users/me` không được liệt kê riêng vì đã được bao hàm ngầm định trong luồng authenticated flow thông qua việc sử dụng auth token.

### Ngoài phạm vi:

*   Các endpoint khác không được liệt kê.
*   Kiểm thử giao diện người dùng (UI testing).
*   Kiểm thử bảo mật (Security testing).


## 3. KPI và Ngưỡng Chấp Nhận (SLO)

### 3.1. Luồng Đọc Công Khai (`GET /products`)

| Chỉ số (KPI) | Ngưỡng Chấp Nhận (Threshold) | Ghi chú |
| :--- | :--- | :--- |
| **p95 Response Time** | `≤ 800ms` | 95% yêu cầu phải có thời gian phản hồi dưới 800ms. |
| **p99 Response Time** | `≤ 1200ms` | 99% yêu cầu phải có thời gian phản hồi dưới 1200ms. |
| **Tỷ lệ lỗi (Error Rate)** | `< 0.5%` | Tỷ lệ lỗi (HTTP 5xx, network errors) phải dưới 0.5%. |
| **RPS mục tiêu** | `≥ 120 RPS` | Hệ thống cần đạt được ít nhất 120-180 RPS từ luồng này. |

### 3.2. Luồng Mua Hàng (Authenticated Flow)

Bao gồm chuỗi `login` -> `add_to_cart` -> `checkout`.

| Chỉ số (KPI) | Ngưỡng Chấp Nhận (Threshold) | Ghi chú |
| :--- | :--- | :--- |
| **p95 Response Time** | `≤ 1000ms` | Áp dụng cho từng request trong chuỗi. |
| **p99 Response Time** | `≤ 1800ms` | Áp dụng cho từng request trong chuỗi. |
| **Tỷ lệ lỗi (Error Rate)** | `< 1%` | Tỷ lệ lỗi trên toàn luồng. |


## 4. Mô Hình Tải & Kịch Bản (Load Profile & Scenarios)

### 4.1. Phân Bổ Tải (Traffic Mix) & Pacing

*   **Traffic Mix:** Tải sẽ được phân bổ theo tỷ lệ để mô phỏng hành vi người dùng thực tế:
    *   **80%** traffic cho luồng đọc công khai (`GET /products`).
    *   **20%** traffic cho luồng mua hàng (`Authenticated Flow`).
*   **Pacing (Think Time):** Mỗi người dùng ảo sẽ có thời gian chờ ngẫu nhiên từ `0.5` đến `2.0` giây giữa các request để mô phỏng thời gian người dùng suy nghĩ. Sẽ có kịch bản chạy không có think time để đo giới hạn tuyệt đối của hệ thống.

### 4.2. Các Kịch Bản Test

*   **Ramp-up Test (Khởi động):** Tăng dần từ 0 đến 60 người dùng ảo (VU) trong 5 phút để "làm nóng" hệ thống và kiểm tra hiệu năng ở tải cơ bản.
*   **Step-Stress Test (Tìm điểm gãy):** Tăng tải theo từng bậc để xác định chính xác breakpoint. Sẽ thực hiện 2 biến thể:
    *   **Theo Virtual User (VU):** Tăng bậc 60 -> 90 -> 120 VU, mỗi bậc giữ trong 8 phút.
    *   **Theo Arrival Rate (CAR):** Tăng bậc 50 -> 100 -> 150 -> 180 -> 210 RPS (requests per second), mỗi bậc giữ trong 8 phút.
*   **Spike Test (Kiểm tra phục hồi):** Tăng đột ngột từ 0 lên 200 VU trong 30 giây, giữ tải trong 2 phút, sau đó giảm về 20 VU và theo dõi thời gian hệ thống phục hồi về trạng thái ổn định (p95 < 800ms).
*   **Soak Test (Kiểm tra độ bền - khuyến nghị):** Chạy tải ổn định ở mức ~80% breakpoint (ví dụ: 120-150 RPS) trong 30-60 phút để phát hiện các vấn đề về rò rỉ bộ nhớ, connection pool, hoặc suy giảm hiệu năng theo thời gian.


## 5. Dữ Liệu & Môi Trường Test (Data & Environment)

*   **Dữ liệu (Data Seeding):**
    *   Cơ sở dữ liệu cần được seed với một số lượng sản phẩm đủ lớn và nhất quán (ví dụ: 5,000 sản phẩm) để kết quả test có thể lặp lại.
    *   Payload request và response cần được chuẩn hóa.
*   **Xác thực (Authentication):**
    *   Sử dụng nhiều tài khoản người dùng riêng biệt để tránh xung đột phiên (token conflict).
    *   Cân nhắc cơ chế tái sử dụng token trong một phiên của người dùng ảo để giảm tải cho endpoint login.
*   **Trạng thái hệ thống (System State):**
    *   Thực hiện test trên cả 2 kịch bản: **cache-warm** (hệ thống đã chạy và cache đã có dữ liệu) và **cache-cold** (sau khi xóa cache) để đánh giá tác động của bộ nhớ đệm.
    *   Các thao tác ghi (giỏ hàng, thanh toán) cần sử dụng mock và có cơ chế dọn dẹp để không làm thay đổi trạng thái hệ thống giữa các lần chạy.


## 6. Quan Sát & Đo Lường (Observability)

*   **Client-side (Locust):**
    *   Thu thập các chỉ số: RPS, response time (p50, p95, p99), error rate.
    *   Lưu lại báo cáo HTML, CSV, và các file log.
*   **Server-side:**
    *   Thu thập các chỉ số hệ thống: CPU, Memory, I/O, Network.
    *   Thu thập các chỉ số ứng dụng (APM): latency của từng thành phần, DB queries (qps, slow queries), cache hit ratio, tình trạng connection/thread pool.
*   **Gắn nhãn (Tagging):** Mỗi lần chạy test cần được gắn nhãn với thông tin ngữ cảnh (ví dụ: git commit hash, build ID, cấu hình test) để dễ dàng so sánh và truy vết.


## 7. Rủi Ro & Biện Pháp An Toàn (Risks & Mitigation)

*   **Rủi ro:** Treo hệ thống cục bộ do quá tải.
*   **Biện pháp:**
    *   Tất cả các bài test chỉ được thực hiện trên môi trường local (`localhost`).
    *   **Điều kiện dừng khẩn cấp:** Tự động dừng bài test nếu tỷ lệ lỗi (`error rate`) vượt quá `5%` trong một cửa sổ thời gian trượt (sliding window) là 120 giây.


## 8. Tiêu Chí Phân Tích & Pass/Fail (Analysis & Pass/Fail Criteria)

### 8.1. Định Nghĩa

*   **Breakpoint:** Được xác định là bậc tải đầu tiên mà tại đó một trong các điều kiện sau xảy ra:
    *   `p95 response time` vượt ngưỡng SLO trong 3 phút liên tiếp.
    *   `Error rate` vượt ngưỡng SLO trong 1 phút liên tiếp.
*   **Thời gian phục hồi (Recovery Time):** Thời gian (tính bằng giây) để hệ thống quay trở lại ngưỡng SLO sau khi kết thúc một spike.

### 8.2. Tiêu Chí Pass/Fail Chung

*   **Pass:** Hệ thống đạt được RPS mục tiêu (`≥ 150 RPS` tổng thể) một cách ổn định trong ít nhất 10 phút mà không vi phạm bất kỳ SLO nào (p95, p99, error rate).
*   **Fail:** Không đạt được RPS mục tiêu hoặc vi phạm bất kỳ SLO nào trước khi đạt đến tải mục tiêu. Báo cáo cần ghi rõ breakpoint đã được xác định.