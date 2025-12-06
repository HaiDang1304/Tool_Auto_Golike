"""
SMART CAPTCHA DETECTOR - Phát hiện captcha thông minh
Kiểm tra nhiều loại captcha: reCAPTCHA v2, reCAPTCHA v3, hCaptcha
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def detect_recaptcha_v2(driver):
    """
    Phát hiện reCAPTCHA v2 (có checkbox)
    Returns: dict với thông tin chi tiết hoặc None
    """
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            try:
                src = iframe.get_attribute("src") or ""
                title = iframe.get_attribute("title") or ""
                
                # reCAPTCHA v2 anchor (checkbox)
                if "recaptcha/api2/anchor" in src or "recaptcha anchor" in title.lower():
                    if iframe.is_displayed() and iframe.size['width'] > 0 and iframe.size['height'] > 0:
                        return {
                            "type": "recaptcha_v2",
                            "subtype": "checkbox",
                            "iframe": iframe,
                            "visible": True,
                            "src": src[:80]
                        }
                
                # reCAPTCHA v2 challenge (image/audio)
                if "recaptcha/api2/bframe" in src or "recaptcha challenge" in title.lower():
                    if iframe.is_displayed() and iframe.size['width'] > 0:
                        return {
                            "type": "recaptcha_v2",
                            "subtype": "challenge",
                            "iframe": iframe,
                            "visible": True,
                            "src": src[:80]
                        }
                        
            except Exception:
                continue
        
        return None
        
    except Exception as e:
        print(f"    [DEBUG] Lỗi detect reCAPTCHA v2: {e}")
        return None


def detect_recaptcha_v3(driver):
    """
    Phát hiện reCAPTCHA v3 (không có UI, chạy ngầm)
    Returns: dict hoặc None
    """
    try:
        # reCAPTCHA v3 thường không có iframe visible
        # Kiểm tra script tag
        scripts = driver.find_elements(By.TAG_NAME, "script")
        
        for script in scripts:
            src = script.get_attribute("src") or ""
            if "recaptcha/api.js" in src or "recaptcha/enterprise.js" in src:
                # Kiểm tra xem có badge không
                try:
                    badge = driver.find_element(By.CLASS_NAME, "grecaptcha-badge")
                    if badge.is_displayed():
                        return {
                            "type": "recaptcha_v3",
                            "subtype": "invisible",
                            "visible": True,
                            "note": "reCAPTCHA v3 - Không thể giải tự động"
                        }
                except:
                    pass
                
                return {
                    "type": "recaptcha_v3",
                    "subtype": "invisible",
                    "visible": False,
                    "note": "reCAPTCHA v3 có thể đang chạy ngầm"
                }
        
        return None
        
    except Exception as e:
        print(f"    [DEBUG] Lỗi detect reCAPTCHA v3: {e}")
        return None


def detect_hcaptcha(driver):
    """
    Phát hiện hCaptcha
    Returns: dict hoặc None
    """
    try:
        # Cách 1: Tìm iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            try:
                src = iframe.get_attribute("src") or ""
                title = iframe.get_attribute("title") or ""
                
                if "hcaptcha" in src.lower() or "hcaptcha" in title.lower():
                    if iframe.is_displayed() and iframe.size['width'] > 0:
                        return {
                            "type": "hcaptcha",
                            "subtype": "checkbox" if "checkbox" in src else "challenge",
                            "iframe": iframe,
                            "visible": True,
                            "src": src[:80]
                        }
            except:
                continue
        
        # Cách 2: Tìm div container
        try:
            containers = driver.find_elements(By.CSS_SELECTOR, "div.h-captcha, div[data-hcaptcha-response]")
            for container in containers:
                if container.is_displayed():
                    return {
                        "type": "hcaptcha",
                        "subtype": "widget",
                        "visible": True,
                        "note": "Tìm thấy hCaptcha container"
                    }
        except:
            pass
        
        return None
        
    except Exception as e:
        print(f"    [DEBUG] Lỗi detect hCaptcha: {e}")
        return None


def detect_cloudflare_turnstile(driver):
    """
    Phát hiện Cloudflare Turnstile
    Returns: dict hoặc None
    """
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            try:
                src = iframe.get_attribute("src") or ""
                if "challenges.cloudflare.com" in src or "turnstile" in src:
                    if iframe.is_displayed():
                        return {
                            "type": "cloudflare_turnstile",
                            "visible": True,
                            "src": src[:80]
                        }
            except:
                continue
        
        return None
        
    except Exception as e:
        print(f"    [DEBUG] Lỗi detect Cloudflare: {e}")
        return None


def smart_detect_all_captchas(driver, verbose=True):
    """
    PHÁT HIỆN TẤT CẢ CÁC LOẠI CAPTCHA
    
    Args:
        driver: Selenium WebDriver
        verbose: In log chi tiết (default: True)
    
    Returns:
        list: Danh sách captcha phát hiện được
              Mỗi item là dict chứa thông tin captcha
    """
    
    if verbose:
        print("\n[*] Đang quét trang web để tìm captcha...")
    
    detected_captchas = []
    
    # 1. Kiểm tra reCAPTCHA v2
    recaptcha_v2 = detect_recaptcha_v2(driver)
    if recaptcha_v2:
        detected_captchas.append(recaptcha_v2)
        if verbose:
            print(f"    ✓ Phát hiện reCAPTCHA v2 ({recaptcha_v2['subtype']})")
    
    # 2. Kiểm tra reCAPTCHA v3
    recaptcha_v3 = detect_recaptcha_v3(driver)
    if recaptcha_v3 and not recaptcha_v2:  # Chỉ báo v3 nếu không có v2
        detected_captchas.append(recaptcha_v3)
        if verbose:
            print(f"    ⚠ Phát hiện reCAPTCHA v3 (invisible)")
    
    # 3. Kiểm tra hCaptcha
    hcaptcha = detect_hcaptcha(driver)
    if hcaptcha:
        detected_captchas.append(hcaptcha)
        if verbose:
            print(f"    ✓ Phát hiện hCaptcha ({hcaptcha.get('subtype', 'unknown')})")
    
    # 4. Kiểm tra Cloudflare Turnstile
    turnstile = detect_cloudflare_turnstile(driver)
    if turnstile:
        detected_captchas.append(turnstile)
        if verbose:
            print(f"    ✓ Phát hiện Cloudflare Turnstile")
    
    if verbose:
        if not detected_captchas:
            print("    ✓ Không phát hiện captcha nào")
        else:
            print(f"    → Tổng cộng: {len(detected_captchas)} captcha")
    
    return detected_captchas


def is_captcha_required(driver, wait_time=2):
    """
    Kiểm tra xem có CẦN giải captcha không
    
    Trả về:
        True: Có captcha và CẦN giải
        False: Không có captcha HOẶC đã được giải
    """
    try:
        # Đợi một chút để captcha load
        time.sleep(wait_time)
        
        # Quét tất cả captcha
        captchas = smart_detect_all_captchas(driver, verbose=False)
        
        if not captchas:
            return False
        
        # Kiểm tra từng captcha xem có cần giải không
        for captcha in captchas:
            captcha_type = captcha.get("type")
            
            # reCAPTCHA v2
            if captcha_type == "recaptcha_v2":
                # Nếu là checkbox, kiểm tra xem đã tick chưa
                if captcha.get("subtype") == "checkbox":
                    try:
                        iframe = captcha.get("iframe")
                        if iframe:
                            driver.switch_to.frame(iframe)
                            checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                            checked = checkbox.get_attribute("aria-checked")
                            driver.switch_to.default_content()
                            
                            if checked == "true":
                                print("    [*] reCAPTCHA đã được tick - Không cần giải")
                                return False
                            else:
                                print("    [!] reCAPTCHA chưa được tick - CẦN giải")
                                return True
                    except:
                        driver.switch_to.default_content()
                        return True
                
                # Nếu là challenge, chắc chắn cần giải
                if captcha.get("subtype") == "challenge":
                    print("    [!] reCAPTCHA challenge xuất hiện - CẦN giải")
                    return True
            
            # hCaptcha
            elif captcha_type == "hcaptcha":
                if captcha.get("visible"):
                    print("    [!] hCaptcha xuất hiện - CẦN giải")
                    return True
            
            # reCAPTCHA v3
            elif captcha_type == "recaptcha_v3":
                # v3 không cần giải thủ công
                print("    [*] reCAPTCHA v3 - Không thể giải, chạy ngầm")
                return False
            
            # Cloudflare
            elif captcha_type == "cloudflare_turnstile":
                print("    [!] Cloudflare Turnstile - CẦN giải")
                return True
        
        return False
        
    except Exception as e:
        print(f"    [DEBUG] Lỗi kiểm tra captcha: {e}")
        return False


def get_solvable_captcha(driver):
    """
    Lấy captcha CÓ THỂ giải được
    
    Returns:
        dict: Thông tin captcha hoặc None
    """
    captchas = smart_detect_all_captchas(driver, verbose=False)
    
    for captcha in captchas:
        captcha_type = captcha.get("type")
        
        # Chỉ trả về captcha có thể giải
        if captcha_type in ["recaptcha_v2", "hcaptcha"]:
            if captcha.get("visible"):
                return captcha
    
    return None


def wait_for_captcha_appear(driver, timeout=10, check_interval=0.5):
    """
    Đợi captcha xuất hiện (nếu có)
    
    Returns:
        True: Captcha xuất hiện
        False: Timeout mà không có captcha
    """
    start_time = time.time()
    
    print(f"[*] Đợi captcha xuất hiện (timeout: {timeout}s)...")
    
    while time.time() - start_time < timeout:
        if is_captcha_required(driver, wait_time=0):
            print("[!] Captcha đã xuất hiện!")
            return True
        
        time.sleep(check_interval)
    
    print("[*] Không có captcha xuất hiện")
    return False


def continuous_captcha_monitor(driver, duration=30, callback=None):
    """
    Giám sát liên tục sự xuất hiện của captcha
    
    Args:
        duration: Thời gian giám sát (giây)
        callback: Hàm gọi khi phát hiện captcha
    """
    start_time = time.time()
    last_check = 0
    
    print(f"\n[*] Bắt đầu giám sát captcha trong {duration}s...")
    
    while time.time() - start_time < duration:
        current_time = time.time()
        
        # Kiểm tra mỗi 2 giây
        if current_time - last_check >= 2:
            if is_captcha_required(driver, wait_time=0):
                print("\n[ALERT] Phát hiện captcha mới!")
                
                if callback:
                    callback(driver)
                
                break
            
            last_check = current_time
        
        time.sleep(0.5)
    
    print("[*] Kết thúc giám sát")
