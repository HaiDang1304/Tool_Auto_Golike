# 🤖 GoLike Auto Tool - Bot tự động làm nhiệm vụ

## ✨ Tính năng chính

### 🎯 Tự động hoàn toàn
- ✅ **Auto login GoLike** - Đăng nhập tự động bằng username/password
- ✅ **Auto login Platforms** - Tự động đăng nhập vào Shopee, TikTok, YouTube
- ✅ **Cookie Persistence** - Lưu cookies để không phải đăng nhập lại mỗi lần
- ✅ **Smart Captcha Solver** - Tự động giải captcha (audio + checkbox)
- ✅ **Anti-Detection** - Chống phát hiện bot (human-like behavior)

### 🌐 Hỗ trợ nhiều kênh
- 🛒 **Shopee** - Follow shop
- 🎵 **TikTok** - Follow, Like, Comment, Share
- 📺 **YouTube** - Subscribe, Like, Comment, Share
- 📸 **Instagram** - Follow, Like, Comment
- 🐦 **Twitter** - Follow, Like, Retweet
- 🌍 **Traffic** - Tăng lượt xem website

### 🔐 Quản lý tài khoản
- ✅ Hỗ trợ nhiều tài khoản GoLike
- ✅ Quản lý thông tin login các platform (Shopee, TikTok, YouTube...)
- ✅ Bật/tắt từng tài khoản dễ dàng
- ✅ Bảo mật thông tin (gitignore credentials)

## 📋 Yêu cầu hệ thống
- **Python 3.7+** (khuyến nghị Python 3.11+)
- **Google Chrome** (phiên bản mới nhất)
- **Internet ổn định**

## 🚀 Cài đặt nhanh

### Bước 1: Clone repository
```bash
git clone https://github.com/HaiDang1304/Tool_Auto_Golike.git
cd Tool_Auto_Golike
```

### Bước 2: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình tài khoản
Đổi tên file `accounts_full.example.json` thành `accounts_full.json` và điền thông tin:

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

**Giải thích:**
- ✅ `enabled: true` - Bật tài khoản
- ✅ `golike` - Thông tin đăng nhập GoLike (bắt buộc)
- ✅ `platforms` - Thông tin login các sàn (chỉ cần điền sàn bạn muốn làm)
- ✅ `auto_login: true` - Tự động đăng nhập vào platforms
- ✅ `save_cookies: true` - Lưu cookies để không phải login lại

### Bước 4: Chạy chương trình
```bash
python main.py
```

Chương trình sẽ hiển thị menu để bạn chọn kênh và nhập số lượng nhiệm vụ.

## 📖 Hướng dẫn chi tiết

Xem file [AUTO_LOGIN_GUIDE.md](AUTO_LOGIN_GUIDE.md) để biết thêm chi tiết về:
- Cách cấu hình tài khoản
- Quản lý cookies
- Xử lý lỗi thường gặp
- Tips & tricks

## 🔄 Workflow tự động

```
1. Chạy python main.py
2. Chọn tài khoản (nếu có nhiều account)
3. Đăng nhập GoLike tự động
4. Chọn kênh (Shopee/TikTok/YouTube...)
5. Bot tự động:
   ├─ Kiểm tra login platform
   ├─ Auto login platform (nếu cần)
   ├─ Lưu cookies
   ├─ Nhận job
   ├─ Mở link job
   ├─ Thực hiện tương tác (Follow/Like/Comment...)
   ├─ Click hoàn thành
   └─ Lặp lại cho job tiếp theo
```

## ⚙️ Tính năng nâng cao

### 1. Anti-Detection
- ✅ Undetected ChromeDriver (bypass bot detection)
- ✅ Selenium Stealth (ẩn automation indicators)
- ✅ Human-like typing (0.1-0.3s mỗi ký tự)
- ✅ Human-like click (di chuyển chuột trước khi click)
- ✅ Random delays (4-6s page load, 1-2s giữa các actions)
- ✅ Random scrolling (cuộn trang như người thật)

### 2. Smart Captcha Solver
- ✅ Tự động phát hiện captcha (reCAPTCHA v2/v3, hCaptcha, Turnstile)
- ✅ Giải audio captcha bằng Google Speech Recognition
- ✅ Fallback methods (checkbox → audio → manual)
- ✅ Chỉ giải khi thực sự cần thiết (smart detection)

### 3. Cookie Management
- ✅ Lưu cookies sau khi login thành công
- ✅ Tự động load cookies lần chạy sau
- ✅ Kiểm tra cookies còn hạn không
- ✅ File cookies: `cookies/{AccountName}_{Platform}.pkl`

## ⚠️ Lưu ý quan trọng

### Bảo mật
- 🔒 **KHÔNG** share file `accounts_full.json` (chứa mật khẩu)
- 🔒 **KHÔNG** push file này lên GitHub (đã có .gitignore)
- 🔒 Nên backup file này ở nơi an toàn

### Chạy bot
- ⏱️ Bot có delays để tránh bị phát hiện (4-6s mỗi page)
- 🤖 Đừng lo lắng nếu bot chạy chậm - đó là tính năng anti-detection
- 🔄 Nếu gặp captcha, bot sẽ tự động giải (hoặc yêu cầu manual)
- 📱 Nếu gặp OTP, nhập OTP rồi nhấn Enter

### Xử lý lỗi
- ❌ "Không tìm thấy ô nhập username" → Platform thay đổi giao diện, cần cập nhật selector
- ❌ "Đăng nhập thất bại" → Kiểm tra username/password trong `accounts_full.json`
- ❌ "Cookies hết hạn" → Bot sẽ tự động đăng nhập lại
- ❌ "CODE 429" → Đang bị rate limit, tăng delays hoặc nghỉ 1 lúc

## 📁 Cấu trúc project

```
Tool_Auto_Golike/
├── main.py                      # File chính
├── account_manager.py           # Quản lý tài khoản
├── auto_login.py                # Auto login platforms
├── login_checker.py             # Kiểm tra login status
├── smart_captcha_detector.py    # Phát hiện captcha
├── recaptcha_solver.py          # Giải reCAPTCHA
├── hcaptcha_solver.py           # Giải hCaptcha
├── recaptcha_audio_solver.py    # Giải audio captcha
├── tiktok_handler.py            # Handler TikTok jobs
├── youtube_handler.py           # Handler YouTube jobs
├── accounts_full.json           # Config tài khoản (BẠN TẠO)
├── accounts_full.example.json   # File mẫu
├── cookies/                     # Thư mục lưu cookies
├── requirements.txt             # Danh sách thư viện
└── README.md                    # File này
```

## 🤝 Đóng góp

Nếu bạn phát hiện bug hoặc muốn thêm tính năng:
1. Fork repository này
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📞 Liên hệ

- GitHub: [@HaiDang1304](https://github.com/HaiDang1304)
- Repository: [Tool_Auto_Golike](https://github.com/HaiDang1304/Tool_Auto_Golike)

## ⚖️ License

Dự án này chỉ dùng cho mục đích học tập và nghiên cứu. Vui lòng tuân thủ Terms of Service của GoLike.

---

**⭐ Nếu tool hữu ích, đừng quên star repo nhé!**
```

### Chạy chế độ không hiện trình duyệt (headless)
Bỏ comment dòng này trong `main.py`:
```python
# options.add_argument('--headless')
```

### Thêm delay giữa các nhiệm vụ
Tìm và chỉnh:
```python
sleep(5)  # Nghỉ giữa các nhiệm vụ → Có thể tăng lên 10
```

## 🐛 Xử lý lỗi

Nếu gặp lỗi:
1. Kiểm tra username/password có đúng không
2. Kiểm tra kết nối Internet
3. Xem log trong terminal và file `logs.csv`
4. Đảm bảo Chrome đã được cài đặt

## 📞 Hỗ trợ

Nếu tool không hoạt động:
- Kiểm tra GoLike có thay đổi giao diện không
- Cập nhật Selenium: `pip install --upgrade selenium`
- Xóa cache ChromeDriver: `.wdm` folder

---

**Chúc bạn kiếm tiền thành công! 💰**
