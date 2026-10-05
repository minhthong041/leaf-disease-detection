# Phát hiện và chẩn đoán bệnh trên lá cây

Đồ án môn **Xử lý ảnh**: chương trình nhận ảnh một chiếc lá, dùng các kỹ thuật xử lý ảnh cổ điển (không dùng học máy) để kết luận lá **khỏe hay bị bệnh**. Nếu lá bị bệnh, chương trình cho biết tỷ lệ diện tích bệnh, mức độ nặng nhẹ và trả về ảnh đã khoanh vùng từng vết bệnh.

## Mục tiêu

| Mục tiêu | Cách làm | Kết quả |
|---|---|---|
| Tách nền | Chuyển RGB → HSV, phân ngưỡng (Otsu / ngưỡng HSV), closing để lấp lỗ, giữ contour lá lớn nhất | Mask lá, diện tích lá |
| Nhận diện vết bệnh | Ngưỡng HSV cho vùng nâu/vàng/đen bên trong lá, opening để khử nhiễu | Mask vết bệnh |
| Tính tỷ lệ diện tích | Contours trên mask vết bệnh: diện tích, chu vi, độ tròn, tâm, bounding box | Số đốm, tỷ lệ nhiễm, chi tiết từng đốm |
| Kết luận | Phân mức theo tỷ lệ nhiễm | `healthy` / `mild` / `moderate` / `severe`, ảnh khoanh vùng |

```
Ảnh lá ─► HSV ─► Tách nền ─► Nhận diện vết bệnh ─► Contours ─► Tỷ lệ & mức độ ─► Ảnh khoanh vùng
```

## Trạng thái

| Phần | Trạng thái |
|---|---|
| Database (PostgreSQL) và model Django | Xong |
| Trang quản trị `/admin/` | Xong |
| Đăng nhập JWT, CORS cho frontend | Xong |
| Pipeline xử lý ảnh (`backend/image_processing/`) | Chưa làm |
| API tải ảnh và trả kết quả | Chưa làm |
| Giao diện frontend | Mới có khung |

## Công nghệ

- **Backend:** Python 3.12, Django 6.1, Django REST Framework, SimpleJWT, PostgreSQL (psycopg 3)
- **Xử lý ảnh:** OpenCV, NumPy, Pillow
- **Frontend:** React 19, Vite 8, MUI 9

## Cấu trúc thư mục

```
leaf-disease-detection/
├── backend/
│   ├── core/               # settings, urls của Django
│   ├── api/                # model, admin, API, lưu ảnh (images.py)
│   ├── image_processing/   # pipeline xử lý ảnh (đang làm)
│   ├── dataset/            # ảnh thử và ảnh tô tay — không đưa lên git
│   ├── media/              # ảnh người dùng tải lên (uploads/) và ảnh kết quả (results/) — không đưa lên git
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # React + Vite
└── docs/
    ├── leaf-disease-db.md  # schema xuất từ DrawSQL (nguồn chuẩn)
    └── database.md         # giải thích database cho cả nhóm
```

## Cài đặt

### Yêu cầu
- Python 3.12
- PostgreSQL đang chạy trên máy
- Node.js 20.19+ hoặc 22.12+ (yêu cầu của Vite)

### Backend

Các lệnh dưới đây chạy trong PowerShell, từ thư mục `backend/`.

```powershell
# 1. Môi trường ảo và thư viện
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Cấu hình
Copy-Item .env.example .env
```

Mở `.env` và điền:
- `DB_PASSWORD`: mật khẩu user PostgreSQL trên máy bạn.
- `DJANGO_SECRET_KEY`: tạo bằng lệnh
  ```powershell
  python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
  ```

```powershell
# 3. Tạo database (hoặc tạo bằng pgAdmin)
psql -U postgres -c "CREATE DATABASE leaf_disease_db;"

# 4. Tạo bảng và tài khoản quản trị
python manage.py migrate
python manage.py createsuperuser

# 5. Chạy server
python manage.py runserver
```

Backend chạy ở http://localhost:8000, trang quản trị ở http://localhost:8000/admin/.

### Frontend

Từ thư mục `frontend/`:

```powershell
npm install
npm run dev
```

Frontend chạy ở http://localhost:5173.

## API hiện có

| Phương thức | Đường dẫn | Gửi lên | Trả về |
|---|---|---|---|
| POST | `/api/auth/login/` | `{"email", "password"}` | `{"access", "refresh"}` |
| POST | `/api/auth/refresh/` | `{"refresh"}` | Cặp token mới (refresh cũ bị vô hiệu) |
| POST | `/api/auth/logout/` | `{"refresh"}` | Vô hiệu refresh token |

Các API khác yêu cầu header `Authorization: Bearer <access token>`. Access token hết hạn sau 30 phút, refresh token sau 7 ngày.

## Lệnh hay dùng

```powershell
python manage.py makemigrations api   # sau khi sửa models.py
python manage.py migrate
python manage.py check
python manage.py test api             # chạy test
npm run lint                          # kiểm tra code frontend
```

## Lưu ý cho thành viên

- **Database:** đọc [docs/database.md](docs/database.md) trước khi sửa model. Khi đổi schema, cập nhật cả diagram DrawSQL, `docs/leaf-disease-db.md` và `docs/database.md`.
- **Migration:** chỉ thêm migration mới, không sửa hay xóa migration đã có trên git.
- **Ảnh không đưa lên git:** nội dung `dataset/` và `media/` bị bỏ qua (chỉ giữ file `.gitkeep`). Bộ ảnh thử của nhóm được chia sẻ riêng.
- **Thêm thư viện Python:** cập nhật `requirements.txt` bằng `pip freeze | Out-File -Encoding utf8 requirements.txt`. **Đừng dùng `pip freeze > requirements.txt`** trong Windows PowerShell: lệnh đó ghi file dạng UTF-16, GitHub sẽ không xem được nội dung file.
- **OpenCV:** ảnh được đọc theo thứ tự BGR (dùng `cv2.COLOR_BGR2HSV`), và kênh H chạy 0–179 chứ không phải 0–359.
