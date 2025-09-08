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


## 3. KPI và Ngưỡng Chấp Nhận (SLO - Service Level Objectives)

| Chỉ số (KPI) | Ngưỡng Chấp Nhận (Threshold) | Ghi chú |
| :--- | :--- | :--- |
| **p95 Response Time** | `≤ 800ms` | 95% yêu cầu phải có thời gian phản hồi dưới 800ms. |
| **Tỷ lệ lỗi (Error Rate)** | `< 1%` | Tỷ lệ lỗi (HTTP 5xx, network errors) phải dưới 1%. |
| **RPS mục tiêu** | `≥ 150 RPS` | Hệ thống cần đạt được ít nhất 150 RPS ở tải ổn định. |


## 4. Mô Hình Tải (Load Profile)

*   **Ramp-up Test:** Tăng dần từ 0 đến 60 người dùng trong 5 phút để "làm nóng" hệ thống và tìm tải cơ bản.
*   **Step-Stress Test:** Tăng tải theo từng bậc để xác định chính xác breakpoint.
*   **Spike Test:** Tăng đột ngột từ 0 lên 200 người dùng trong 30 giây để kiểm tra khả năng phục hồi.


## 5. Rủi Ro & Biện Pháp An Toàn (Risks & Mitigation)

*   **Rủi ro:** Treo hệ thống cục bộ do quá tải.
*   **Biện pháp:**
    *   Tất cả các bài test chỉ được thực hiện trên môi trường local (`localhost`).
    *   **Điều kiện dừng khẩn cấp:** Tự động dừng bài test nếu tỷ lệ lỗi (`error rate`) vượt quá `5%` và duy trì trong `2 phút` liên tục.