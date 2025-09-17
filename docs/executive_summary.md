# Báo Cáo Tóm Tắt Hiệu Năng (Executive Summary)

**Ngày:** 24/05/2024

---

## Tình Trạng Tổng Quan (Overall Status)

**TÌNH TRẠNG: <font color='orange'>ORANGE (MAJOR ISSUES)</font>**

**Lý do:** Hệ thống không đạt được các chỉ số hiệu năng mục tiêu (KPI) và có dấu hiệu bất ổn định (rò rỉ tài nguyên) khi chạy trong thời gian dài, mặc dù lỗi blocker ban đầu đã được khắc phục.

---

## 1. Phát hiện chính & Phân tích (Key Findings & Analysis)

Sau khi khắc phục lỗi `401 Unauthorized` ban đầu, các bài test đã hé lộ những vấn đề hiệu năng cốt lõi của hệ thống:

1.  **Điểm gãy (Breakpoint) thấp:** Hệ thống chỉ chịu được khoảng **~90 người dùng đồng thời (VU)**, tương đương **~52 RPS**, trước khi thời gian phản hồi vượt ngưỡng SLO (p95 > 800ms). Con số này thấp hơn đáng kể so với mục tiêu **120-180 RPS** đã đề ra trong kế hoạch.
2.  **Suy giảm hiệu năng theo thời gian (Latency Drift):** Bài test độ bền (Soak test) cho thấy thời gian phản hồi (p95) tăng dần theo thời gian. Đây là dấu hiệu rõ ràng của việc **rò rỉ bộ nhớ hoặc tài nguyên** phía server, có thể gây sập hệ thống nếu chạy trong thời gian dài.
3.  **Khả năng phục hồi tốt:** Điểm sáng là hệ thống có khả năng phục hồi nhanh chóng (trong **75 giây**) sau khi chịu tải đột biến, cho thấy khả năng xử lý sốc tải trong ngắn hạn là khá tốt.

---

## 2. Kết luận & Đề xuất (Conclusion & Recommendations)

### Kết luận
Mặc dù lỗi blocker ban đầu đã được khắc phục, sản phẩm vẫn **chưa đủ điều kiện** để "Go-live" do không đạt được các mục tiêu hiệu năng cốt lõi và có vấn đề nghiêm trọng về độ ổn định lâu dài.

### Rủi ro nếu không khắc phục (Risk if not fixed)
*   **Trải nghiệm người dùng:** Hiệu năng kém sẽ dẫn đến trải nghiệm người dùng chậm chạp. Vấn đề rò rỉ tài nguyên có thể gây sập server sau một thời gian hoạt động, làm gián đoạn dịch vụ.
*   **Tổn thất kinh doanh:** Mất doanh thu trực tiếp và suy giảm uy tín thương hiệu.
*   **Khả năng mở rộng:** Hệ thống không thể mở rộng (scale-out) để đáp ứng lượng người dùng tăng trong tương lai với breakpoint thấp như hiện tại.

### Đề xuất
1.  **[P0 - Bắt buộc] Điều tra và khắc phục vấn đề "Latency Drift":** Ưu tiên hàng đầu. Cần profiling bộ nhớ và CPU của ứng dụng để tìm ra nguyên nhân rò rỉ tài nguyên.
2.  **[P1] Tối ưu hóa để nâng cao Breakpoint:** Phân tích các truy vấn CSDL, cấu hình connection pool, và các thành phần khác để cải thiện thông lượng (RPS) của hệ thống.
3.  **[P2] Thực thi lại bộ test hiệu năng:** Sau khi các bản vá được áp dụng, cần chạy lại toàn bộ bộ test để xác nhận các vấn đề đã được giải quyết.

---

## 3. Bảng Tổng Hợp Kết Quả (KPI Summary)

| Kịch bản | Mô tả | RPS (TB) | p95 (ms) | Tỷ lệ lỗi (%) | Kết quả |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_RAMP_01** | Ramp-up 0 → 60 VU | 39.4 | 1200 | 2.07 | **KHÔNG ĐẠT** |
| **TC_STEP_VU_03** | Step-Stress 25 → 110 VU | ~52 (tại 90 VU) | >800 (tại 90 VU) | <1% | **KHÔNG ĐẠT** (Tìm thấy Breakpoint) |
| **TC_CONST_VU_04** | Constant Load 80 VU | ~52 | ~780 | ~0.1 | **ĐẠT** |
| **TC_SPIKE_05** | Spike 0 → 200 VU | ~65 | ~780 (sau phục hồi) | <1% | **ĐẠT** (Phục hồi trong 75s) |
| **TC_SOAK_06** | Soak Test 60 phút | ~52 | >800 (tăng dần) | ~0.1 | **KHÔNG ĐẠT** (Latency Drift) |

---

## 4. Chi tiết Defects (Defect Details)

**Defect ID-01: Lỗi kiến trúc - Token không được chia sẻ giữa các worker**
*   **Mô tả:** Hệ thống được cấu hình với 2 workers (`APP_WORKERS=2`). Token xác thực được tạo ở worker này không được công nhận ở worker kia, dẫn đến lỗi `401 Unauthorized`.
*   **Mức độ nghiêm trọng:** **Critical**.
*   **Trạng thái:** **CLOSED** (Đã khắc phục và thực thi lại test).

**Defect ID-02: Suy giảm hiệu năng theo thời gian (Latency Drift)**
*   **Mô tả:** Trong kịch bản Soak Test (TC_SOAK_06), thời gian phản hồi p95 tăng dần theo thời gian, vượt ngưỡng SLO từ phút thứ 30 trở đi. Đây là dấu hiệu của rò rỉ bộ nhớ hoặc tài nguyên phía server.
*   **Mức độ nghiêm trọng:** **Major**.
*   **Trạng thái:** **OPEN**.

---

## 5. Phụ lục: Môi trường & Phạm vi (Appendix: Environment & Scope)

### Môi trường kiểm thử
| Hạng mục | Chi tiết |
| :--- | :--- |
| **Application Server** | Gunicorn chạy trên Docker |
| **Cấu hình Server** | 2 Workers, 4 Threads (`APP_WORKERS=2`, `APP_THREADS=4`) |
| **URL Ứng dụng** | `http://localhost:8000` |
| **Công cụ tạo tải** | Locust (Python) |

### Phạm vi kiểm thử
*   **Trong phạm vi:**
    *   Luồng công khai: `GET /products`
    *   Luồng mua hàng: `POST /auth/token/login` -> `POST /cart/add` -> `POST /checkout`
*   **Ngoài phạm vi:**
    *   Kiểm thử chức năng, giao diện, bảo mật.