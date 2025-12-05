# 🚀 HƯỚNG DẪN NHANH - GOLIKE AUTO TOOL

## Bước 1: Cấu hình tài khoản

Mở file `accounts.json` và sửa:

```json
{
  "name": "TenTaiKhoan",
  "enabled": true,
  "username": "golike_username",    // ← Username GoLike của bạn
  "password": "golike_password",    // ← Password GoLike của bạn
  "channels": ["facebook", "tiktok"],  // ← Chọn kênh muốn làm
  "max_tasks_per_round": 10
}
```

## Bước 2: Chọn kênh nhiệm vụ

**Có 7 kênh:**
- `facebook` - Like, Follow, Share
- `tiktok` - Follow, Like
- `shopee` - Follow shop
- `twitter` - Follow, Like, Retweet  
- `youtube` - Subscribe, Like
- `instagram` - Follow, Like
- `traffic` - View website

**Ví dụ:**
```json
"channels": ["facebook"]                          // Chỉ làm Facebook
"channels": ["facebook", "tiktok", "youtube"]     // Làm 3 kênh
"channels": ["traffic"]                           // Chỉ tăng traffic
```

## Bước 3: Chạy chương trình

```powershell
D:/React/Tool/.venv/Scripts/python.exe main.py
```

**Hoặc** (nếu đã activate venv):
```powershell
python main.py
```

## 📊 Kết quả

- Tool sẽ tự động đăng nhập → làm nhiệm vụ → ghi log
- Logs được lưu trong `logs.csv`
- Chương trình chạy tự động liên tục

## ⚙️ Tùy chỉnh nhanh

### Tắt/Bật tài khoản
```json
"enabled": true   // BẬT
"enabled": false  // TẮT
```

### Thay đổi số nhiệm vụ mỗi kênh
```json
"max_tasks_per_round": 20  // Làm 20 nhiệm vụ/kênh
```

### Chạy ẩn trình duyệt (headless)
Mở `main.py`, tìm và bỏ comment dòng:
```python
# options.add_argument('--headless')
```
Thành:
```python
options.add_argument('--headless')
```

---

## ❓ FAQ

**Q: Tool báo lỗi import?**
A: Đã cài đặt rồi, lỗi này từ Pylance, không ảnh hưởng.

**Q: Không tìm thấy nhiệm vụ?**
A: Kiểm tra tài khoản GoLike đã liên kết kênh chưa (Facebook, TikTok...)

**Q: Muốn dừng chương trình?**
A: Nhấn `Ctrl + C` trong terminal

**Q: Làm sao biết đang chạy kênh nào?**
A: Xem terminal, có log `[TÊN_TÀI_KHOẢN][KÊNH] ...`

---

**🎯 Mẹo:** Bắt đầu với 1 tài khoản, 1 kênh, 5 nhiệm vụ để test!
