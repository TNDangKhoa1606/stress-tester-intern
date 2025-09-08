# Bảng Thiết Kế Test Case Hiệu Năng

Tài liệu này chi tiết hóa các kịch bản kiểm thử hiệu năng sẽ được thực thi, theo cấu trúc bảng chi tiết.

---

**Pre-condition:** Hệ thống demo API đã được khởi chạy qua Docker và có thể truy cập tại `http://localhost:8000`.

| ID | Description (Mô tả) | Number of virtual users (Số người dùng ảo) | Running time (Thời gian chạy) | Steps (Các bước thực hiện) | Expected Result (Kết quả mong đợi) | Actual Result | Notes (Ghi chú) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **STRESS_RAMP_01** | **Ramp-up Test (Khởi động):** "Làm nóng" hệ thống và kiểm tra hiệu năng cơ bản ở tải thấp. | Tăng dần từ 0 đến 60 users. | 5 phút. | 1. Chạy Locust với cấu hình Ramp-up.<br>2. Giám sát biểu đồ thời gian thực trên UI. | - `p95 Response Time ≤ 800ms`.<br>- `Tỷ lệ lỗi < 1%`.<br>- Hệ thống hoạt động ổn định, không có lỗi bất thường. | (Để trống) | Locust |
| **STRESS_STEP_02** | **Step-Stress Test (Tìm điểm gãy):** Xác định breakpoint của hệ thống bằng cách tăng tải theo từng bậc. | Tăng theo từng bậc, mỗi bậc +50 users (50, 100, 150,...). | 5 phút cho mỗi bậc. | 1. Chạy Locust với kịch bản `LoadTestShape`.<br>2. Theo dõi `p95` và `Tỷ lệ lỗi` ở cuối mỗi bậc tải. | - Xác định được chính xác số Users/RPS mà tại đó `p95 > 800ms` hoặc `Tỷ lệ lỗi ≥ 1%`. Đây chính là breakpoint. | (Để trống) | Locust |
| **STRESS_SPIKE_03** | **Spike Test (Kiểm tra phục hồi):** Đánh giá khả năng chịu sốc tải và phục hồi của hệ thống. | - GĐ1: Tăng đột ngột 0 → 200 users (trong 30s).<br>- GĐ2: Giữ 200 users (trong 60s).<br>- GĐ3: Giảm về 20 users. | ~7 phút. | 1. Chạy Locust với kịch bản Spike.<br>2. Quan sát biểu đồ `p95` trong và sau giai đoạn spike. | - Hệ thống không sập (tỷ lệ lỗi < 50%) trong lúc spike.<br>- Thời gian phục hồi (p95 quay về < 800ms) phải dưới 60 giây sau khi tải giảm. | (Để trống) | Locust |