"""
LOGIN CHECKER - Kiểm tra đăng nhập vào các nền tảng
Đảm bảo đã đăng nhập Shopee/TikTok/YouTube trước khi làm job
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


def check_shopee_login(driver):
    """
    Kiểm tra xem đã đăng nhập Shopee chưa
    
    Returns:
        True: Đã đăng nhập
        False: Chưa đăng nhập
    """
    try:
        # Cách 1: Kiểm tra URL
        current_url = driver.current_url.lower()
        if "login" in current_url or "buyer/login" in current_url:
            return False
        
        # Cách 2: Tìm avatar/username (dấu hiệu đã login)
        indicators = [
            # Avatar user
            "//div[contains(@class, 'navbar__username')]",
            "//div[contains(@class, 'shopee-avatar')]",
            
            # Tên user
            "//div[contains(@class, 'navbar__username')]//span",
            
            # Dropdown account
            "//div[@class='navbar__account']",
        ]
        
        for selector in indicators:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements and elements[0].is_displayed():
                    print("  [OK] Đã đăng nhập Shopee")
                    return True
            except:
                continue
        
        # Cách 3: Kiểm tra button đăng nhập (nếu có = chưa login)
        login_btns = driver.find_elements(By.XPATH, 
            "//a[contains(@href, 'login') or contains(., 'Đăng Nhập')]")
        
        if login_btns:
            for btn in login_btns:
                if btn.is_displayed():
                    print("  [!] CHƯA đăng nhập Shopee")
                    return False
        
        # Mặc định coi như đã login nếu không tìm thấy button login
        print("  [?] Không chắc chắn trạng thái đăng nhập Shopee")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi kiểm tra login Shopee: {e}")
        return False


def check_tiktok_login(driver):
    """
    Kiểm tra xem đã đăng nhập TikTok chưa
    
    Returns:
        True: Đã đăng nhập
        False: Chưa đăng nhập
    """
    try:
        # Cách 1: Kiểm tra URL
        current_url = driver.current_url.lower()
        if "/login" in current_url:
            return False
        
        # Cách 2: Tìm avatar/username
        indicators = [
            # Avatar trong header
            "//div[@id='header-avatar']",
            "//div[contains(@data-e2e, 'profile-icon')]",
            
            # Button "Upload" (chỉ có khi đã login)
            "//a[contains(@href, '/upload')]",
            "//button[contains(., 'Upload')]",
            
            # Inbox icon
            "//a[contains(@href, '/messages')]",
        ]
        
        for selector in indicators:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements and elements[0].is_displayed():
                    print("  [OK] Đã đăng nhập TikTok")
                    return True
            except:
                continue
        
        # Cách 3: Kiểm tra button "Log in"
        login_btns = driver.find_elements(By.XPATH,
            "//button[contains(., 'Log in')] | //a[contains(., 'Log in')]")
        
        if login_btns:
            for btn in login_btns:
                if btn.is_displayed():
                    print("  [!] CHƯA đăng nhập TikTok")
                    return False
        
        print("  [?] Không chắc chắn trạng thái đăng nhập TikTok")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi kiểm tra login TikTok: {e}")
        return False


def check_youtube_login(driver):
    """
    Kiểm tra xem đã đăng nhập YouTube/Google chưa
    
    Returns:
        True: Đã đăng nhập
        False: Chưa đăng nhập
    """
    try:
        # Cách 1: Kiểm tra URL
        current_url = driver.current_url.lower()
        if "accounts.google.com" in current_url:
            return False
        
        # Cách 2: Tìm avatar (dấu hiệu đã login)
        indicators = [
            # Avatar button
            "//button[@id='avatar-btn']",
            "//ytd-topbar-menu-button-renderer[@id='avatar-btn']",
            "//yt-img-shadow[@id='avatar']//img",
            
            # Account menu
            "//ytd-masthead//button[contains(@aria-label, 'Google Account')]",
            
            # Channel icon
            "//ytd-topbar-menu-button-renderer//yt-img-shadow",
        ]
        
        for selector in indicators:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    # Kiểm tra xem có src (avatar có ảnh = đã login)
                    for elem in elements:
                        if elem.is_displayed():
                            # Nếu là img, check src
                            try:
                                img = elem.find_element(By.TAG_NAME, "img")
                                src = img.get_attribute("src")
                                if src and "default" not in src:
                                    print("  [OK] Đã đăng nhập YouTube")
                                    return True
                            except:
                                # Nếu không phải img, coi như có element = login
                                print("  [OK] Đã đăng nhập YouTube")
                                return True
            except:
                continue
        
        # Cách 3: Kiểm tra button "Sign in"
        signin_btns = driver.find_elements(By.XPATH,
            "//a[contains(@aria-label, 'Sign in')] | //ytd-button-renderer//a[contains(., 'Sign in')]")
        
        if signin_btns:
            for btn in signin_btns:
                if btn.is_displayed():
                    print("  [!] CHƯA đăng nhập YouTube")
                    return False
        
        print("  [?] Không chắc chắn trạng thái đăng nhập YouTube")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi kiểm tra login YouTube: {e}")
        return False


def check_platform_login(driver, platform):
    """
    Kiểm tra đăng nhập cho bất kỳ platform nào
    
    Args:
        driver: Selenium WebDriver
        platform: Tên platform (shopee, tiktok, youtube, instagram, twitter)
    
    Returns:
        True: Đã đăng nhập
        False: Chưa đăng nhập
    """
    
    platform = platform.lower()
    
    if platform == "shopee":
        return check_shopee_login(driver)
    
    elif platform == "tiktok":
        return check_tiktok_login(driver)
    
    elif platform == "youtube":
        return check_youtube_login(driver)
    
    elif platform == "instagram":
        # Instagram: Kiểm tra có avatar không
        try:
            avatars = driver.find_elements(By.XPATH, 
                "//img[@alt[contains(., 'profile picture')]] | //a[contains(@href, '/direct/')]")
            if avatars and avatars[0].is_displayed():
                print("  [OK] Đã đăng nhập Instagram")
                return True
            else:
                print("  [!] CHƯA đăng nhập Instagram")
                return False
        except:
            return False
    
    elif platform == "twitter" or platform == "x":
        # Twitter/X: Kiểm tra có avatar không
        try:
            avatars = driver.find_elements(By.XPATH,
                "//div[@data-testid='SideNav_AccountSwitcher_Button'] | //a[@aria-label='Profile']")
            if avatars and avatars[0].is_displayed():
                print("  [OK] Đã đăng nhập Twitter")
                return True
            else:
                print("  [!] CHƯA đăng nhập Twitter")
                return False
        except:
            return False
    
    else:
        print(f"  [!] Platform không được hỗ trợ: {platform}")
        return False


def prompt_manual_login(driver, platform, timeout=300):
    """
    Yêu cầu user đăng nhập thủ công
    
    Args:
        driver: Selenium WebDriver
        platform: Tên platform
        timeout: Thời gian chờ tối đa (giây)
    
    Returns:
        True: Đã đăng nhập thành công
        False: Timeout hoặc user hủy
    """
    
    print("\n" + "="*70)
    print(f"⚠️  CẦN ĐĂNG NHẬP {platform.upper()} THỦ CÔNG")
    print("="*70)
    print(f"""
HƯỚNG DẪN:
1. Trang {platform.upper()} đã được mở trong trình duyệt
2. Vui lòng đăng nhập tài khoản {platform.upper()} của bạn
3. Sau khi đăng nhập XONG, quay lại đây và nhấn Enter
4. Nếu không muốn đăng nhập, nhấn Ctrl+C để bỏ qua

Lưu ý:
- NẾU KHÔNG ĐĂNG NHẬP, các job sẽ KHÔNG ĐƯỢC TÍNH
- GoLike sẽ KIỂM TRA và KHÔNG TRẢ TIỀN cho job giả
- Bạn có {timeout} giây để đăng nhập

Đang đợi...
    """)
    
    try:
        input(">>> Nhấn Enter sau khi đã đăng nhập xong...")
        
        # Kiểm tra lại xem đã login chưa
        time.sleep(2)
        if check_platform_login(driver, platform):
            print("\n[OK] Đã xác nhận đăng nhập thành công!")
            return True
        else:
            print("\n[!] Vẫn chưa đăng nhập. Vui lòng thử lại.")
            return False
            
    except KeyboardInterrupt:
        print("\n[!] Đã hủy đăng nhập")
        return False


def ensure_platform_login(driver, platform, auto_prompt=True):
    """
    Đảm bảo đã đăng nhập vào platform trước khi làm job
    
    Args:
        driver: Selenium WebDriver
        platform: Tên platform
        auto_prompt: Tự động nhắc đăng nhập nếu chưa login
    
    Returns:
        True: Đã đăng nhập (hoặc user chọn bỏ qua)
        False: Chưa đăng nhập và không thể tiếp tục
    """
    
    print(f"\n[*] Kiểm tra trạng thái đăng nhập {platform.upper()}...")
    
    # Đợi trang load
    time.sleep(3)
    
    # Kiểm tra đăng nhập
    is_logged_in = check_platform_login(driver, platform)
    
    if is_logged_in:
        print(f"[OK] Đã đăng nhập {platform.upper()} - Có thể làm job")
        return True
    
    # Chưa đăng nhập
    if auto_prompt:
        print(f"\n[!] CHƯA ĐĂNG NHẬP {platform.upper()}!")
        print("[*] Sẽ yêu cầu đăng nhập thủ công...")
        
        return prompt_manual_login(driver, platform)
    else:
        print(f"\n[!] CHƯA ĐĂNG NHẬP {platform.upper()}!")
        print("[!] Job này sẽ KHÔNG ĐƯỢC TÍNH nếu không đăng nhập")
        return False
