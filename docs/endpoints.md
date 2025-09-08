# Bảng Tóm Tắt Endpoint

| Phương thức | Endpoint | Payload Mẫu (Request Body) | Ràng buộc | Mã trả về (Thành công) | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- | 
| `GET` | `/products` | (Không có) | Không cần xác thực | `200 OK` | Trả về danh sách tất cả sản phẩm. |
| `POST` | `/auth/token/login` | `{"username": "alice", "password": "alice123"}` | Không cần xác thực | `200 OK` | Trả về `auth_token` để sử dụng cho các request cần xác thực. |
| `GET` | `/auth/users/me` | (Không có) | Dùng `auth_token` trong header `Authorization: Bearer token` | `200 OK` | Trả về thông tin của user hiện tại. |
| `POST` | `/cart/add` | `{"product_id": 1, "quantity": 1}` | Cần `auth_token` trong header `Authorization: Bearer <token>` | `200 OK` | Thêm sản phẩm vào giỏ hàng của user hiện tại. |
| `POST` | `/checkout` | `{"payment_method": "visa"}` | Cần `auth_token` trong header `Authorization: Bearer <token>` | `200 OK` | Thanh toán giỏ hàng. Có thể trả về `502` ngẫu nhiên. |
