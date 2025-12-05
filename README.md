# GoLike Auto Tool - Hướng dẫn sử dụng

## 🚀 Tính năng
- ✅ Tự động đăng nhập GoLike bằng username/password
- ✅ Hỗ trợ **7 kênh nhiệm vụ**: Facebook, TikTok, Shopee, Twitter, Youtube, Instagram, Traffic
- ✅ Tự động nhận và làm nhiệm vụ (Like, Follow, Subscribe, View...)
- ✅ Hỗ trợ nhiều tài khoản, mỗi tài khoản có thể chọn kênh riêng
- ✅ Ghi log chi tiết mỗi nhiệm vụ vào file CSV
- ✅ Chạy tự động liên tục theo vòng lặp

## 📋 Yêu cầu
- Python 3.7+
- Google Chrome đã cài đặt
- Các thư viện: selenium, webdriver-manager (đã cài đặt)

## ⚙️ Cấu hình

### 1. Sửa file `accounts.json`
Thay thế username, password và chọn kênh nhiệm vụ:

```json
[
  {
    "name": "GoLike_Account_1",
    "enabled": true,
    "username": "your_username_1",           // ← Thay username thật của bạn
    "password": "your_password_1",           // ← Thay password thật của bạn
    "channels": ["facebook", "tiktok"],      // ← Chọn kênh muốn làm
    "max_tasks_per_round": 10,
    "note": "Tài khoản chính"
  }
]
```

**Các kênh có sẵn:**
- `facebook` - Làm nhiệm vụ Facebook (Like, Follow, Share...)
- `tiktok` - Làm nhiệm vụ TikTok (Follow, Like, Comment...)
- `shopee` - Làm nhiệm vụ Shopee (Follow shop...)
- `twitter` - Làm nhiệm vụ Twitter (Follow, Like, Retweet...)
- `youtube` - Làm nhiệm vụ Youtube (Subscribe, Like, Comment...)
- `instagram` - Làm nhiệm vụ Instagram (Follow, Like...)
- `traffic` - Tăng traffic (View website)

**Lưu ý:**
- `enabled: true` - Tài khoản sẽ được sử dụng
- `enabled: false` - Tài khoản sẽ bị bỏ qua
- `channels` - Danh sách kênh muốn làm (có thể chọn nhiều kênh)
- `max_tasks_per_round` - Số nhiệm vụ tối đa mỗi kênh mỗi vòng (mặc định: 10)

### 2. Chạy chương trình

Mở PowerShell tại thư mục Tool và chạy:

```powershell
D:/React/Tool/.venv/Scripts/python.exe main.py
```

Hoặc đơn giản hơn (nếu đã activate venv):
```powershell
python main.py
```

## 📊 Logs

Tất cả hoạt động được ghi vào file `logs.csv`:
- Thời gian thực hiện
- Tên tài khoản
- ID nhiệm vụ
- Loại nhiệm vụ
- Trạng thái (success/error)

## 🔄 Cách hoạt động

1. **Đăng nhập**: Tool tự động đăng nhập GoLike với username/password
2. **Chọn kênh**: Lặp qua từng kênh trong danh sách `channels`
3. **Nhận nhiệm vụ**: Tìm và click nút "Thực hiện" trên trang nhiệm vụ của kênh
4. **Làm nhiệm vụ**: Tự động mở tab mới, thực hiện tương tác (Like/Follow/Subscribe...)
5. **Lặp lại**: Sau khi hoàn thành, chuyển sang nhiệm vụ tiếp theo
6. **Đổi kênh**: Hoàn thành hết kênh này, chuyển sang kênh khác
7. **Vòng lặp**: Sau khi xử lý hết tài khoản, nghỉ 60s rồi chạy lại

**Ví dụ luồng:**
```
Account_1 → Facebook (10 nhiệm vụ) → TikTok (10 nhiệm vụ) → Youtube (10 nhiệm vụ)
Account_2 → Shopee (15 nhiệm vụ) → Twitter (15 nhiệm vụ)
→ Nghỉ 60s → Lặp lại
```

## ⚠️ Lưu ý quan trọng

1. **Thời gian chờ**: Tool có delay giữa các thao tác để tránh bị phát hiện bot
2. **Headless mode**: Bỏ comment dòng `options.add_argument('--headless')` nếu muốn chạy ẩn
3. **Selector**: Nếu GoLike thay đổi giao diện, cần cập nhật các selector trong code
4. **Tài khoản Facebook**: Đảm bảo các tài khoản Facebook đã được liên kết với GoLike

## 🛠️ Tùy chỉnh

### Chọn kênh muốn làm
Thêm hoặc bớt kênh trong `accounts.json`:
```json
"channels": ["facebook", "tiktok", "youtube"]  // Chọn 3 kênh
"channels": ["traffic"]                        // Chỉ làm traffic
"channels": []                                 // Không làm kênh nào (bỏ qua)
```

### Thay đổi số nhiệm vụ tối đa mỗi kênh
Sửa `max_tasks_per_round` trong `accounts.json`:
```json
"max_tasks_per_round": 20  // Làm 20 nhiệm vụ/kênh
```

### Thay đổi thời gian nghỉ giữa các vòng
Tìm dòng trong `main.py`:
```python
sleep(60)  # Nghỉ 60 giây → Có thể đổi thành 300 (5 phút)
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
