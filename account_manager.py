"""
ACCOUNT MANAGER
Quản lý tài khoản GoLike và các sàn (Shopee, TikTok, YouTube, etc.)
"""

import json
import os
from typing import Dict, List, Optional


class AccountManager:
    """Quản lý tài khoản từ file JSON"""
    
    def __init__(self, accounts_file="accounts_full.json"):
        self.accounts_file = accounts_file
        self.accounts = []
        self.global_settings = {}
        self.load_accounts()
    
    def load_accounts(self):
        """Load tài khoản từ file JSON"""
        try:
            if not os.path.exists(self.accounts_file):
                print(f"[!] File {self.accounts_file} không tồn tại!")
                print(f"[*] Sử dụng file mẫu: accounts_full.example.json")
                
                # Copy file example
                if os.path.exists("accounts_full.example.json"):
                    import shutil
                    shutil.copy("accounts_full.example.json", self.accounts_file)
                    print(f"[OK] Đã tạo {self.accounts_file}")
                    print("[*] Vui lòng chỉnh sửa file này với thông tin tài khoản của bạn!")
                else:
                    print("[ERROR] Không tìm thấy file example!")
                    return
            
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Hỗ trợ 2 format: array hoặc object
                if isinstance(data, list):
                    # Format: [{account1}, {account2}, ...]
                    self.accounts = data
                    self.global_settings = {}
                else:
                    # Format: {"accounts": [...], "global_settings": {...}}
                    self.accounts = data.get("accounts", [])
                    self.global_settings = data.get("global_settings", {})
            
            print(f"[OK] Đã load {len(self.accounts)} tài khoản từ {self.accounts_file}")
            
        except Exception as e:
            print(f"[ERROR] Lỗi load accounts: {e}")
            self.accounts = []
    
    def get_enabled_accounts(self) -> List[Dict]:
        """Lấy danh sách tài khoản đã bật"""
        return [acc for acc in self.accounts if acc.get("enabled", False)]
    
    def get_account_by_id(self, account_id: int) -> Optional[Dict]:
        """Lấy tài khoản theo ID"""
        for acc in self.accounts:
            if acc.get("id") == account_id:
                return acc
        return None
    
    def get_account_by_name(self, name: str) -> Optional[Dict]:
        """Lấy tài khoản theo tên"""
        for acc in self.accounts:
            if acc.get("name") == name:
                return acc
        return None
    
    def get_golike_credentials(self, account: Dict) -> tuple:
        """Lấy username và password GoLike"""
        golike = account.get("golike", {})
        return golike.get("username", ""), golike.get("password", "")
    
    def get_platform_credentials(self, account: Dict, platform: str) -> Optional[Dict]:
        """
        Lấy thông tin đăng nhập của 1 platform
        
        Returns:
            Dict với keys: username/email, password, login_method
        """
        platforms = account.get("platforms", {})
        platform_data = platforms.get(platform.lower(), {})
        
        # Kiểm tra có username/email và password không
        if not platform_data:
            return None
        
        has_username = platform_data.get("username") or platform_data.get("email")
        has_password = platform_data.get("password")
        
        if not (has_username and has_password):
            return None
        
        return platform_data
    
    def is_platform_enabled(self, account: Dict, platform: str) -> bool:
        """Kiểm tra xem platform có thông tin đăng nhập không"""
        creds = self.get_platform_credentials(account, platform)
        return creds is not None
    
    def get_account_settings(self, account: Dict) -> Dict:
        """Lấy settings của account"""
        return account.get("settings", {})
    
    def get_max_jobs(self, account: Dict) -> int:
        """Lấy số job tối đa cho account"""
        settings = self.get_account_settings(account)
        return settings.get("max_jobs_per_channel", 10)
    
    def should_auto_login(self, account: Dict) -> bool:
        """Kiểm tra có nên tự động login không"""
        settings = self.get_account_settings(account)
        return settings.get("auto_login", True)
    
    def should_save_cookies(self, account: Dict) -> bool:
        """Kiểm tra có nên lưu cookies không"""
        settings = self.get_account_settings(account)
        return settings.get("save_cookies", True)
    
    def get_cookies_path(self) -> str:
        """Lấy đường dẫn thư mục cookies"""
        path = self.global_settings.get("cookies_path", "./cookies")
        
        # Tạo thư mục nếu chưa có
        if not os.path.exists(path):
            os.makedirs(path)
        
        return path
    
    def get_account_cookie_file(self, account: Dict, platform: str) -> str:
        """Lấy đường dẫn file cookie cho account + platform"""
        cookies_dir = self.get_cookies_path()
        account_id = account.get("id", 1)
        filename = f"account_{account_id}_{platform}.json"
        return os.path.join(cookies_dir, filename)
    
    def get_cookie_path(self, account_name: str, platform: str) -> str:
        """Lấy đường dẫn file cookie theo tên account + platform"""
        cookies_dir = self.get_cookies_path()
        # Sanitize account name (remove special characters)
        safe_name = "".join(c if c.isalnum() else "_" for c in account_name)
        filename = f"{safe_name}_{platform}.pkl"
        return os.path.join(cookies_dir, filename)
    
    def list_accounts(self):
        """In ra danh sách tài khoản"""
        print("\n" + "="*70)
        print("DANH SÁCH TÀI KHOẢN")
        print("="*70)
        
        if not self.accounts:
            print("[!] Chưa có tài khoản nào!")
            return
        
        for acc in self.accounts:
            status = "✅ BẬT" if acc.get("enabled") else "❌ TẮT"
            account_id = acc.get("id", "?")
            name = acc.get("name", "Unknown")
            note = acc.get("note", "")
            
            print(f"\n[{account_id}] {name} - {status}")
            print(f"    Note: {note}")
            
            # GoLike
            golike = acc.get("golike", {})
            golike_user = golike.get("username", "N/A")
            print(f"    GoLike: {golike_user}")
            
            # Platforms
            platforms = acc.get("platforms", {})
            available_platforms = []
            
            for platform, data in platforms.items():
                if data:
                    # Check có credentials không
                    has_creds = False
                    if platform == "youtube":
                        has_creds = data.get("email") and data.get("password")
                    else:
                        has_creds = data.get("username") and data.get("password")
                    
                    if has_creds:
                        available_platforms.append(platform.upper())
            
            if available_platforms:
                print(f"    Platforms: {', '.join(available_platforms)}")
            else:
                print("    Platforms: Không có")
            
            # Settings
            settings = acc.get("settings", {})
            max_jobs = settings.get("max_jobs_per_channel", 10)
            print(f"    Max jobs: {max_jobs}/kênh")
        
        print("\n" + "="*70)
    
    def validate_account(self, account: Dict) -> tuple:
        """
        Kiểm tra tài khoản có hợp lệ không
        
        Returns:
            (is_valid: bool, errors: list)
        """
        errors = []
        
        # Kiểm tra GoLike
        golike = account.get("golike", {})
        if not golike.get("username") or not golike.get("password"):
            errors.append("Thiếu thông tin GoLike (username/password)")
        
        # Kiểm tra ít nhất 1 platform có credentials
        platforms = account.get("platforms", {})
        has_platform_creds = False
        
        for platform, data in platforms.items():
            if data:
                # Kiểm tra có username/email và password
                if platform == "youtube":
                    if data.get("email") and data.get("password"):
                        has_platform_creds = True
                else:
                    if data.get("username") and data.get("password"):
                        has_platform_creds = True
        
        if not has_platform_creds:
            errors.append("Không có platform nào có thông tin đăng nhập")
        
        is_valid = len(errors) == 0
        return is_valid, errors


def show_account_menu(manager: AccountManager) -> Optional[Dict]:
    """
    Hiển thị menu chọn tài khoản
    
    Returns:
        Account dict hoặc None nếu user hủy
    """
    enabled_accounts = manager.get_enabled_accounts()
    
    if not enabled_accounts:
        print("\n[!] Không có tài khoản nào được bật!")
        print("[*] Vui lòng chỉnh sửa file accounts_full.json")
        return None
    
    print("\n" + "="*70)
    print("CHỌN TÀI KHOẢN ĐỂ CHẠY")
    print("="*70)
    
    for i, acc in enumerate(enabled_accounts, 1):
        name = acc.get("name", "Unknown")
        note = acc.get("note", "")
        
        # Đếm platforms enabled
        platforms = acc.get("platforms", {})
        enabled_count = sum(1 for p in platforms.values() if p.get("enabled", False))
        
        print(f"{i}. {name}")
        print(f"   {note}")
        print(f"   Platforms: {enabled_count} kênh")
    
    print("0. Thoát")
    print("="*70)
    
    while True:
        try:
            choice = input("\nChọn tài khoản (1-{}, 0 để thoát): ".format(len(enabled_accounts))).strip()
            
            if choice == "0":
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(enabled_accounts):
                selected = enabled_accounts[index]
                
                # Validate
                if manager.validate_account(selected):
                    print(f"\n[OK] Đã chọn: {selected.get('name')}")
                    return selected
                else:
                    print("[!] Tài khoản không hợp lệ! Chọn tài khoản khác.")
            else:
                print("Lựa chọn không hợp lệ!")
                
        except ValueError:
            print("Vui lòng nhập số!")
        except KeyboardInterrupt:
            return None


# Test
if __name__ == "__main__":
    manager = AccountManager()
    manager.list_accounts()
    
    # Test chọn account
    account = show_account_menu(manager)
    if account:
        print(f"\nĐã chọn: {account.get('name')}")
        
        # Test lấy credentials
        golike_user, golike_pass = manager.get_golike_credentials(account)
        print(f"GoLike: {golike_user}")
        
        # Test platform
        shopee_creds = manager.get_platform_credentials(account, "shopee")
        if shopee_creds:
            print(f"Shopee enabled: {shopee_creds.get('username')}")
