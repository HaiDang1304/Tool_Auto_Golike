"""
AUTO LOGIN MODULE
Tự động đăng nhập vào các sàn: Shopee, TikTok, YouTube, Instagram, Twitter
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import pickle
import os


def human_type(element, text, min_delay=0.1, max_delay=0.3):
    """Gõ text như người thật"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


def auto_login_shopee(driver, username, password):
    """
    Tự động đăng nhập Shopee
    
    Args:
        driver: Selenium WebDriver
        username: Số điện thoại hoặc email
        password: Mật khẩu
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    try:
        print("\n[SHOPEE] Đang đăng nhập...")
        
        # Mở trang login
        driver.get("https://shopee.vn/buyer/login")
        time.sleep(3)
        
        # Tìm và nhập username
        username_selectors = [
            "//input[@name='loginKey']",
            "//input[@placeholder='Email/Số điện thoại/Tên đăng nhập']",
            "//input[@type='text']",
        ]
        
        username_input = None
        for selector in username_selectors:
            try:
                username_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not username_input:
            print("[!] Không tìm thấy ô nhập username")
            return False
        
        print("[*] Nhập username...")
        username_input.click()
        time.sleep(0.5)
        human_type(username_input, username)
        time.sleep(1)
        
        # Tìm và nhập password
        password_selectors = [
            "//input[@name='password']",
            "//input[@type='password']",
            "//input[@placeholder='Mật khẩu']",
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                password_input = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not password_input:
            print("[!] Không tìm thấy ô nhập password")
            return False
        
        print("[*] Nhập password...")
        password_input.click()
        time.sleep(0.5)
        human_type(password_input, password)
        time.sleep(1)
        
        # Click nút đăng nhập
        login_btn_selectors = [
            "//button[@type='submit']",
            "//button[contains(., 'Đăng nhập')]",
            "//button[contains(@class, 'btn-solid-primary')]",
        ]
        
        login_btn = None
        for selector in login_btn_selectors:
            try:
                login_btn = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not login_btn:
            print("[!] Không tìm thấy nút đăng nhập")
            return False
        
        print("[*] Click đăng nhập...")
        login_btn.click()
        time.sleep(5)
        
        # Kiểm tra có captcha/OTP không
        current_url = driver.current_url.lower()
        if "otp" in current_url or "verify" in current_url:
            print("[!] Cần nhập OTP/Captcha thủ công!")
            input(">>> Nhập OTP rồi nhấn Enter...")
            time.sleep(3)
        
        # Kiểm tra đăng nhập thành công
        time.sleep(3)
        if "login" not in driver.current_url.lower():
            print("[OK] Đăng nhập Shopee thành công!")
            return True
        else:
            print("[!] Đăng nhập Shopee thất bại!")
            return False
            
    except Exception as e:
        print(f"[ERROR] Lỗi đăng nhập Shopee: {e}")
        return False


def auto_login_tiktok(driver, username, password, login_method="email"):
    """
    Tự động đăng nhập TikTok
    
    Args:
        driver: Selenium WebDriver
        username: Email hoặc username
        password: Mật khẩu
        login_method: "email" hoặc "phone"
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    try:
        print("\n[TIKTOK] Đang đăng nhập...")
        
        # Mở trang login
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(3)
        
        # Tìm ô nhập email/username
        input_selectors = [
            "//input[@name='username']",
            "//input[@placeholder='Email or username']",
            "//input[@type='text']",
        ]
        
        username_input = None
        for selector in input_selectors:
            try:
                username_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not username_input:
            print("[!] Không tìm thấy ô nhập username")
            return False
        
        print("[*] Nhập email/username...")
        username_input.click()
        time.sleep(0.5)
        human_type(username_input, username)
        time.sleep(1)
        
        # Tìm ô nhập password
        password_input = None
        try:
            password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        except:
            print("[!] Không tìm thấy ô nhập password")
            return False
        
        print("[*] Nhập password...")
        password_input.click()
        time.sleep(0.5)
        human_type(password_input, password)
        time.sleep(1)
        
        # Click nút đăng nhập
        login_btn_selectors = [
            "//button[@type='submit']",
            "//button[contains(., 'Log in')]",
            "//button[contains(., 'Đăng nhập')]",
        ]
        
        login_btn = None
        for selector in login_btn_selectors:
            try:
                login_btn = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if login_btn:
            print("[*] Click đăng nhập...")
            login_btn.click()
            time.sleep(5)
        else:
            # Thử Enter
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)
        
        # Kiểm tra captcha
        if "captcha" in driver.page_source.lower():
            print("[!] Cần giải captcha thủ công!")
            input(">>> Giải captcha rồi nhấn Enter...")
            time.sleep(3)
        
        # Kiểm tra đăng nhập thành công
        time.sleep(3)
        if "/login" not in driver.current_url:
            print("[OK] Đăng nhập TikTok thành công!")
            return True
        else:
            print("[!] Đăng nhập TikTok thất bại!")
            return False
            
    except Exception as e:
        print(f"[ERROR] Lỗi đăng nhập TikTok: {e}")
        return False


def auto_login_youtube(driver, email, password):
    """
    Tự động đăng nhập YouTube/Google
    
    Args:
        driver: Selenium WebDriver
        email: Email Google
        password: Mật khẩu Google
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    try:
        print("\n[YOUTUBE] Đang đăng nhập Google...")
        
        # Mở trang login Google
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # Nhập email
        email_selectors = [
            "//input[@type='email']",
            "//input[@id='identifierId']",
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                email_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not email_input:
            print("[!] Không tìm thấy ô nhập email")
            return False
        
        print("[*] Nhập email...")
        email_input.click()
        time.sleep(0.5)
        human_type(email_input, email)
        time.sleep(1)
        
        # Click Next
        next_btn = None
        try:
            next_btn = driver.find_element(By.XPATH, "//button[@id='identifierNext'] | //button[contains(., 'Next')]")
            next_btn.click()
        except:
            email_input.send_keys(Keys.RETURN)
        
        time.sleep(3)
        
        # Nhập password
        password_selectors = [
            "//input[@type='password']",
            "//input[@name='password']",
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not password_input:
            print("[!] Không tìm thấy ô nhập password")
            return False
        
        print("[*] Nhập password...")
        password_input.click()
        time.sleep(0.5)
        human_type(password_input, password)
        time.sleep(1)
        
        # Click Next
        try:
            next_btn = driver.find_element(By.XPATH, "//button[@id='passwordNext'] | //button[contains(., 'Next')]")
            next_btn.click()
        except:
            password_input.send_keys(Keys.RETURN)
        
        time.sleep(5)
        
        # Kiểm tra 2FA
        if "challenge" in driver.current_url or "verify" in driver.current_url:
            print("[!] Cần xác thực 2 bước!")
            input(">>> Xác thực trên điện thoại rồi nhấn Enter...")
            time.sleep(5)
        
        # Mở YouTube để test
        driver.get("https://www.youtube.com")
        time.sleep(3)
        
        # Kiểm tra đăng nhập
        try:
            avatar = driver.find_element(By.XPATH, "//button[@id='avatar-btn']")
            if avatar:
                print("[OK] Đăng nhập YouTube thành công!")
                return True
        except:
            pass
        
        print("[!] Đăng nhập YouTube thất bại!")
        return False
        
    except Exception as e:
        print(f"[ERROR] Lỗi đăng nhập YouTube: {e}")
        return False


def save_cookies(driver, filepath):
    """Lưu cookies vào file"""
    try:
        cookies = driver.get_cookies()
        with open(filepath, 'wb') as f:
            pickle.dump(cookies, f)
        print(f"[OK] Đã lưu cookies: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi lưu cookies: {e}")
        return False


def load_cookies(driver, filepath):
    """Load cookies từ file"""
    try:
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'rb') as f:
            cookies = pickle.load(f)
        
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass
        
        print(f"[OK] Đã load cookies: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi load cookies: {e}")
        return False


def auto_login_platform(driver, platform, credentials, cookie_file=None):
    """
    Tự động đăng nhập vào platform
    
    Args:
        driver: Selenium WebDriver
        platform: Tên platform (shopee, tiktok, youtube, etc.)
        credentials: Dict chứa username/email và password
        cookie_file: File cookies để lưu/load
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    
    platform = platform.lower()
    
    # Thử load cookies trước
    if cookie_file and os.path.exists(cookie_file):
        print(f"[*] Thử load cookies từ {cookie_file}...")
        
        # Mở trang trước khi load cookies
        if platform == "shopee":
            driver.get("https://shopee.vn")
        elif platform == "tiktok":
            driver.get("https://www.tiktok.com")
        elif platform == "youtube":
            driver.get("https://www.youtube.com")
        
        time.sleep(2)
        
        if load_cookies(driver, cookie_file):
            driver.refresh()
            time.sleep(3)
            
            # Kiểm tra đã login chưa
            from login_checker import check_platform_login
            if check_platform_login(driver, platform):
                print(f"[OK] Đã đăng nhập {platform.upper()} bằng cookies!")
                return True
            else:
                print("[!] Cookies hết hạn, đăng nhập lại...")
    
    # Đăng nhập bình thường
    success = False
    
    if platform == "shopee":
        username = credentials.get("username", "")
        password = credentials.get("password", "")
        success = auto_login_shopee(driver, username, password)
    
    elif platform == "tiktok":
        username = credentials.get("username", "")
        password = credentials.get("password", "")
        login_method = credentials.get("login_method", "email")
        success = auto_login_tiktok(driver, username, password, login_method)
    
    elif platform == "youtube":
        email = credentials.get("email", "")
        password = credentials.get("password", "")
        success = auto_login_youtube(driver, email, password)
    
    else:
        print(f"[!] Platform {platform} chưa được hỗ trợ auto login!")
        return False
    
    # Lưu cookies nếu thành công
    if success and cookie_file:
        time.sleep(2)
        save_cookies(driver, cookie_file)
    
    return success
