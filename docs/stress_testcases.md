# Bảng Thiết Kế Test Case Hiệu Năng

Tài liệu này chi tiết hóa các kịch bản kiểm thử hiệu năng sẽ được thực thi.

---

**Pre-condition:** Hệ thống demo API đã được khởi chạy qua Docker và có thể truy cập tại `http://localhost:8000`. Tất cả các kịch bản đều đã tích hợp validation cho response.

---

| ID | Description | Number of virtual users | Running time | Step | Expected | Actual | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_BASE_00** | **Baseline Test (Sanity Check):** Thiết lập hiệu năng cơ sở. | 10 VU | 5 phút | 1. Chạy tải ổn định với 10 VU trong 5 phút. | Tất cả các endpoint đều đáp ứng ngưỡng SLO (p95/p99, error rate). | **KHÔNG ĐẠT**<br>- Ghi nhận nhiều lỗi `401 Unauthorized` ở `GET /auth/users/me`.<br>- **Phân tích:** Lỗi kiến trúc, token đăng nhập không được chia sẻ giữa các worker của server. | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_RAMP_01** | **Ramp-up Test (Khởi động):** "Làm nóng" hệ thống và kiểm tra hiệu năng ở tải cơ bản. | 0 → 60 VU | 10 phút | 1. Chạy Locust với ramp-up từ 0 đến 60 VU trong 5 phút.<br>2. Giữ tải ổn định trong 5 phút.<br>3. Giám sát biểu đồ thời gian thực. | - Luồng `/products`: p95 ≤ 800ms, error < 0.5%.<br>- Luồng `Auth`: p95 ≤ 1000ms, error < 1%. | **KHÔNG ĐẠT**<br>- RPS: 39.4<br>- p50: 440ms (Đạt)<br>- p95 (Auth): **1200ms** (Vượt SLO ≤1000ms)<br>- p99: **1300ms** (Vượt SLO ≤1200ms)<br>- Error (Checkout): **2.07%** (Vượt SLO <1%) | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_STEP_VU_02** | **Step-Stress Test (by VU):** Tìm điểm gãy (breakpoint) bằng cách tăng số người dùng ảo (VU) theo từng bậc. | 5 bậc: 10 → 30 → 60 → 100 → 150 VU | 15 phút (tổng cộng) | 1. Sử dụng `stress_shape.py` để chạy 5 bậc tải:<br>- Bậc 1: 10 VU trong 1 phút.<br>- Bậc 2: 30 VU trong 2 phút.<br>- Bậc 3: 60 VU trong 3 phút.<br>- Bậc 4: 100 VU trong 4 phút.<br>- Bậc 5: 150 VU trong 5 phút. | Xác định được **Breakpoint**: bậc tải đầu tiên mà `p95` > SLO trong 3 phút liên tiếp hoặc `error rate` > SLO trong 1 phút liên tiếp. | **ĐÃ THỰC HIỆN**<br>**Breakpoint được xác định ở 100 VU.**<br>Bảng kết quả:<br>• **10 VU:** RPS 10.0, p95 290ms, Lỗi 0.2% (Đạt)<br>• **30 VU:** RPS 31.2, p95 300ms, Lỗi 0.0% (Đạt)<br>• **60 VU:** RPS 48.1, p95 720ms, Lỗi 0.2% (Đạt)<br>• **100 VU:** RPS 50.4, p95 **1400ms** (Vượt SLO)<br>• **150 VU:** RPS 51.9, p95 **2700ms** (Vượt SLO) | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_STEP_RPS_03** | **Step-Stress Test (by Arrival Rate):** Tìm điểm gãy (breakpoint) bằng cách tăng tỷ lệ request (RPS) theo từng bậc. | N/A (Theo RPS: 50 → 210) | 40 phút (8 phút/bậc) | 1. Sử dụng custom `LoadTestShape` để điều khiển arrival-rate theo các bậc: 50 → 100 → 150 → 180 → 210 RPS.<br>2. Chạy headless và xuất báo cáo. | - **Pass:** Đạt mục tiêu ≥ 150 RPS ổn định không vi phạm SLO (p95/p99/error) trong 8 phút.<br>- **Fail:** Xác định được breakpoint trước khi đạt mục tiêu. | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |
| **TC_SPIKE_04** | **Spike Test (Kiểm tra phục hồi):** Đánh giá khả năng chịu sốc tải và phục hồi của hệ thống. | Spike: 0 → 200 VU (30s) | ~7.5 phút | 1. Tăng đột ngột lên 200 VU trong 30s.<br>2. Giữ tải trong 2 phút.<br>3. Giảm về 20 VU và theo dõi 5 phút. | Đo được **Recovery Time**. **Pass** nếu p95 < 800ms và error rate < 1% trong ≤ 120s sau khi giảm tải. | | - Mix: 100% Auth Flow<br>- Pacing: 0.2-1.0s<br>- Công cụ: Locust |
| **TC_SOAK_05** | **Soak Test (Kiểm tra độ bền):** Tìm rò rỉ bộ nhớ/tài nguyên khi chạy tải ổn định trong thời gian dài. | Tải tương đương ~80% breakpoint đo được (ví dụ 120–150 RPS hoặc VU tương ứng) | 60 phút | 1. Chạy headless với tải không đổi trong 60 phút.<br>2. Theo dõi biểu đồ p95, error rate, CPU, memory của server theo thời gian. | - **Pass:** p95, error rate, CPU, memory duy trì ổn định.<br>- **Fail:** Có hiện tượng suy giảm hiệu năng (latency drift), hoặc error rate/memory/CPU tăng dần. | | - Mix: 80% /products, 20% Auth<br>- Pacing: 0.5-2.0s<br>- Công cụ: Locust |

**Ghi chú chung:**
- **An toàn:** Các bài test sẽ tự động dừng nếu tỷ lệ lỗi vượt quá 5% trong 120 giây liên tục.
- **Tham chiếu:** Tất cả các ngưỡng SLO và định nghĩa chi tiết được tham chiếu từ file `docs/test_plan.md`.
