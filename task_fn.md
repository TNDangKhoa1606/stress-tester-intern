(English: **Convert the content into .md format**)

Dưới đây là phiên bản Markdown gọn gàng theo đúng cấu trúc bạn yêu cầu. Bạn cũng có thể tải file `.md` mình đã tạo tại đây: **[Download the Markdown](sandbox:/mnt/data/locust_workshop_assignment.md)**

````markdown
# Bài Tập Workshop: Stress Test với Locust

## MỤC TIÊU CHUNG
- Biết thiết kế & thực thi **stress test** bằng **Locust** trên demo API cục bộ.
- Xác định **breakpoint**, khả năng **phục hồi sau spike**, và đọc **KPI hiệu năng** (_RPS, p50/p95/p99, error rate_).
- Viết **báo cáo súc tích** và **trình bày workshop 15–20 phút**.

---

## PHẠM VI
- Ứng dụng demo (**Flask + gunicorn**) chạy local qua **Docker**  
  _Các endpoint_: `/, /products, /auth/token/login, /auth/users/me, /cart/add, /checkout`.
- Locust scripts theo repo mẫu:  
  `locust/tasks/*`, `locust/shapes/*`, `locust/locust.conf`.

---

## TASKS

### 1) Chuẩn bị môi trường & hiểu hệ thống
- Cài **Docker**, **Python 3.10+**.
- Chạy demo API:
  ```bash
  docker compose up --build -d
  # URL: http://localhost:8000
````

* Tạo `virtualenv`, cài Locust:

  ```bash
  pip install -r locust/requirements.txt
  ```
* **Đầu ra**: Ảnh chụp `docker compose up` và `/` trả về `{"ok": true}`.

### 2) Khảo sát endpoint & ghi chú

* Gọi thử thủ công (cURL/Postman) các API:

  * `GET /products`
  * `POST /auth/token/login`
  * `GET /auth/users/me`
  * `POST /cart/add`
  * `POST /checkout`
* Ghi **mã trả về**, **payload mẫu**, **ràng buộc** (auth token, field bắt buộc).
* **Đầu ra**: Bảng tóm tắt endpoint (file `docs/endpoints.md`).

### 3) Chạy Locust UI để làm quen

```bash
locust -f locust/tasks/public_read.py,locust/tasks/auth_flows.py --config locust/locust.conf
```

* Thử **5–10 VU**, **1–2 phút**, đọc UI: **RPS**, **response time**, **error**.
* **Đầu ra**: Ảnh chụp UI + ghi chú **3 chỉ số** hiểu đúng.

### 4) Viết Test Plan ngắn (≤ 2 trang)

* Mục tiêu: tìm **breakpoint** `/products` & khả năng **phục hồi sau spike** trên flow **đăng nhập → thêm giỏ → checkout**.
* KPI/SLO đề xuất (ví dụ): `p95 ≤ 800ms`, `error < 1%`, **RPS mục tiêu ≥ 150**.
* Mô hình tải: **ramp** (khởi động), **step-stress** (tăng bậc), **spike** (0→200 VU/30s).
* Rủi ro & an toàn: **chỉ chạy local**; **dừng khi error ≥ 5%** trong **2 phút** liên tục.
* **Đầu ra**: `docs/test_plan.md`.

### 5) Thiết kế Test Case stress

* Lập **bảng test case** cho 3 kiểu: **Ramp**, **Step-Stress**, **Spike**.
* Nêu rõ: **Mục tiêu**, **Dữ liệu**, **Tham số** (users, spawn\_rate, thời lượng), **Điều kiện pass/fail**, **Thu thập số liệu**.
* **Đầu ra**: `docs/stress_testcases.xlsx` (hoặc `.md`).

### 6) Chuẩn hóa dữ liệu test

* Hoàn thiện `locust/common/data.csv` (3–5 user), **tránh xung đột phiên**.
* Thêm **validation** ở task (**HTTP code**, **trường JSON** bắt buộc).
* **Đầu ra**: **CSV** + **snippet** code validation đã thêm.

### 7) Chạy Ramp (khởi động)

* **0→60 VU** trong **5 phút**, **think time 200–1500ms**.
* Xuất HTML & CSV:

  ```bash
  --html locust/reports/ramp.html --csv locust/reports/ramp
  ```
* **Đầu ra**: `ramp.html` + ghi chú KPI (**p50/p95/p99**, **error**, **RPS**).

### 8) Chạy Step-Stress (tìm breakpoint)

* Dùng `shapes/StepStress`. Theo dõi **p95** & **error** theo **từng bậc**.
* Ghi **thời điểm vượt SLO** & **VU/RPS** tương ứng.
* **Đầu ra**: `stress.html` + **bảng “bậc tải → p95/error/RPS”**.

### 9) Chạy Spike & kiểm tra phục hồi

* Tạo **spike 0→200 VU (30s)**, giữ **60s**, hạ **20 VU**.
* Quan sát **p95 khi spike** và **thời gian phục hồi** về mức **ổn định**.
* **Đầu ra**: `spike.html` + ghi chú **“thời gian phục hồi” (s)**.

### 10) Soak nhẹ (ổn định)

* **40 VU** trong **20–30 phút**. Tìm **rò rỉ** (error tăng dần, **latency drift**).
* **Đầu ra**: `soak.html` + **chart p95 theo thời gian** (trích từ CSV).

### 11) Phân tích CSV & báo cáo tóm tắt

* Đọc các CSV (`ramp/stress/spike/soak`), trích **RPS trung bình**, **p95**, **error rate**.
* Tổng hợp vào **1 trang Executive Summary**:

  * **Bảng KPI** theo kịch bản
  * **Breakpoint** (con số cụ thể)
  * **Insight** (ví dụ: `checkout` nhạy cảm với spike; `/products` ổn định)
* **Đầu ra**: `docs/executive_summary.pdf` (hoặc `.md`).

### 12) Tùy chỉnh server để tái hiện bottleneck (có kiểm soát)

* Chỉnh env demo API (ví dụ `APP_MAX_DELAY_MS=600`, `APP_SPIKE_ERROR_RATE=0.05`).
* Chạy lại **Step-Stress** để **so sánh trước/sau**.
* **Đầu ra**: **bảng so sánh trước/sau** (**p95**, **error**, **breakpoint**).

### 13) Tham số hóa & cấu hình

* Đưa `BASE_URL`, user, mật khẩu… vào **env/locust.conf**.
* Bổ sung **flag dòng lệnh** cho **số VU**, **spawn rate**, **thời lượng**.
* **Đầu ra**: Cập nhật **README.md** mục **“Runbook lệnh”**.

### 14) Headless mode & artifact

* Chạy các kịch bản ở **headless** trong **script** `shell/Makefile`.
* Lưu artifact (**HTML/CSV**) vào `locust/reports/` theo **timestamp**.
* **Đầu ra**: `scripts/run_all.sh` (hoặc **Makefile**) + **thư mục báo cáo mẫu**.

### 15) Slide Workshop (15–20 phút)

* Nội dung: **mục tiêu**, **mô hình tải**, **kết quả chính (đồ thị)**, **breakpoint**, **phục hồi**, **khuyến nghị**.
* Chèn **3–5 ảnh** chụp màn hình UI Locust + **1 chart timeline p95**.
* **Đầu ra**: `docs/workshop_slides.pptx` (hoặc Google Slides/Canva link).

### 16) Bài nộp cuối (Repo + Tài liệu)

* **Repo hoàn chỉnh** (script, shape, README, docs, reports mẫu).
* **Checklist** (bên dưới) tick đầy đủ.
* **Demo 5–10 phút** chạy một kịch bản trực tiếp.

---

## CHECKLIST “DEFINITION OF DONE”

* [x] Chạy được demo API local, **có ảnh chụp xác nhận**.
* [x] `docs/endpoints.md` đầy đủ thông tin endpoint.
* [x] `docs/test_plan.md` (**mục tiêu, KPI/SLO, mô hình tải, an toàn**).
* [x] `docs/stress_testcases.*` (**ramp, step-stress, spike – có pass/fail rõ**).
* [x] **Script Locust** có **validation hợp lệ** (**HTTP code + field**).
* [ ] Báo cáo `ramp.html`, `stress.html`, `spike.html`, `soak.html` + **CSV** tương ứng.
* [ ] `docs/executive_summary.*` **1 trang** (nêu **breakpoint** & **khuyến nghị**).
* [ ] **So sánh kết quả** trước/sau khi **chỉnh env server**.
* [ ] `README.md` cập nhật **Runbook chạy UI & headless + tham số**.
* [ ] `scripts/run_all.sh` (hoặc **Makefile**) **tạo artifact có timestamp**.
* [ ] `docs/workshop_slides.pptx` **hoàn chỉnh**.

---

## LỖI CẦN TRÁNH

* Không **validate response** → **“đỏ” không phát hiện**.
* Dùng chung **1 tài khoản cho mọi VU** → **token conflict**.
* Không có **think time/pacing** → **mô hình tải sai lệch**.
* **Nhầm lẫn** timeout **client** với **5xx server**.
* Báo cáo **không nêu con số breakpoint cụ thể**.
