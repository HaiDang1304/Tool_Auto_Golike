# HƯỚNG DẪN SỬ DỤNG AUTO LOGIN

## Tính năng mới

### 1. Quản lý tài khoản tập trung
- File `accounts_full.json`: Lưu trữ tất cả tài khoản GoLike và các sàn (Shopee, TikTok, YouTube, Instagram, Twitter)
- Hỗ trợ nhiều tài khoản, bật/tắt từng tài khoản
- Menu chọn tài khoản tự động

### 2. Auto login tự động
- Tự động đăng nhập vào các sàn trước khi làm nhiệm vụ
- Lưu cookies để không phải đăng nhập lại mỗi lần
- Hỗ trợ 3 sàn chính:
  - **Shopee**: Đăng nhập bằng SĐT/Email + Mật khẩu
  - **TikTok**: Đăng nhập bằng Email + Mật khẩu
  - **YouTube**: Đăng nhập bằng Google (Email + Password)

### 3. Cookie persistence
- Cookies được lưu vào folder `cookies/`
- Mỗi tài khoản + platform có file cookie riêng
- Tự động load cookies nếu còn hạn, bỏ qua bước login

## Cách sử dụng

### Bước 1: Cấu hình tài khoản

Mở file `accounts_full.json` và điền thông tin:

```json
[
    {
        "name": "Account1",
        "enabled": true,
        "golike": {
            "username": "your_golike_username",
            "password": "your_golike_password"
        },
        "platforms": {
            "shopee": {
                "username": "0987654321",
                "password": "shopee_password"
            },
            "tiktok": {
                "username": "email@example.com",
                "password": "tiktok_password",
                "login_method": "email"
            },
            "youtube": {
                "email": "gmail@gmail.com",
                "password": "google_password"
            }
        },
        "settings": {
            "max_jobs_per_session": 50,
            "auto_login": true,
            "save_cookies": true
        }
    }
]
```

**Lưu ý:**
- `enabled`: `true` để bật tài khoản, `false` để tắt
- `platforms`: Chỉ cần điền thông tin platform bạn muốn làm nhiệm vụ
- `save_cookies`: `true` để lưu cookies (khuyến nghị)

### Bước 2: Chạy chương trình

```bash
python main.py
```

### Bước 3: Chọn tài khoản

Nếu có nhiều tài khoản, chương trình sẽ hiển thị menu để bạn chọn:

```
====================================
CHỌN TÀI KHOẢN
====================================
1. Account1 (GoLike: username1)
2. Account2 (GoLike: username2)
0. Hủy
====================================
Chọn tài khoản (1-2, 0 để hủy):
```

### Bước 4: Chọn kênh và làm nhiệm vụ

Chương trình sẽ:
1. **Đăng nhập GoLike** tự động
2. **Kiểm tra login platform** (Shopee/TikTok/YouTube)
3. **Auto login platform** nếu chưa đăng nhập
4. **Lưu cookies** sau khi login thành công
5. **Làm nhiệm vụ** như bình thường

## Các tính năng nâng cao

### 1. Nhiều tài khoản

Thêm nhiều tài khoản vào `accounts_full.json`:

```json
[
    {
        "name": "Account1",
        "enabled": true,
        "golike": { ... }
    },
    {
        "name": "Account2",
        "enabled": true,
        "golike": { ... }
    }
]
```

### 2. Quản lý cookies

Cookies được lưu tại:
```
cookies/
├── Account1_shopee.pkl
├── Account1_tiktok.pkl
├── Account1_youtube.pkl
├── Account2_shopee.pkl
└── ...
```

**Xóa cookies** (nếu muốn đăng nhập lại):
```bash
# Windows
del cookies\*.pkl

# Linux/Mac
rm cookies/*.pkl
```

### 3. Xử lý lỗi

#### Lỗi: "Không tìm thấy accounts_full.json"
→ Tạo file `accounts_full.json` theo mẫu ở trên

#### Lỗi: "Cần nhập OTP/Captcha thủ công"
→ Khi Shopee/TikTok yêu cầu OTP, nhập OTP rồi nhấn Enter

#### Lỗi: "Đăng nhập thất bại"
→ Kiểm tra lại username/password trong `accounts_full.json`

#### Lỗi: "Cookies hết hạn"
→ Chương trình sẽ tự động đăng nhập lại

## Lưu ý bảo mật

⚠️ **QUAN TRỌNG:**
- File `accounts_full.json` chứa mật khẩu, **KHÔNG** share cho ai
- **KHÔNG** push file này lên GitHub
- Nên backup file này ở nơi an toàn

## So sánh với phiên bản cũ

### Trước đây (`accounts.json`)
```json
[
    {
        "name": "Account1",
        "username": "golike_user",
        "password": "golike_pass",
        "enabled": true
    }
]
```
- Chỉ lưu thông tin GoLike
- **KHÔNG** có auto login platform
- Phải đăng nhập thủ công vào Shopee/TikTok/YouTube
- Nhiệm vụ **KHÔNG** được tính nếu chưa login platform

### Bây giờ (`accounts_full.json`)
```json
[
    {
        "name": "Account1",
        "golike": { ... },
        "platforms": {
            "shopee": { ... },
            "tiktok": { ... },
            "youtube": { ... }
        },
        "settings": { ... }
    }
]
```
- Lưu đầy đủ thông tin GoLike + Platforms
- **TỰ ĐỘNG** đăng nhập vào platforms
- Lưu cookies để không phải login lại
- Nhiệm vụ **ĐƯỢC TÍNH** vì đã login platform

## Tương thích ngược

Nếu bạn chưa muốn dùng `accounts_full.json`, chương trình vẫn hoạt động với `accounts.json` cũ (nhưng không có auto login).

## Roadmap

- [ ] Hỗ trợ Instagram auto login
- [ ] Hỗ trợ Twitter auto login
- [ ] Xử lý 2FA tự động (Google Authenticator)
- [ ] Web UI để quản lý tài khoản
- [ ] Scheduler để chạy tự động theo lịch

## Hỗ trợ

Nếu gặp lỗi, vui lòng:
1. Kiểm tra file `accounts_full.json` có đúng format JSON không
2. Kiểm tra username/password có đúng không
3. Xóa cookies và thử lại
4. Tắt 2FA nếu có (hoặc chuẩn bị nhập OTP)
