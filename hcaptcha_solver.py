"""
hCaptcha Solver - Tu dong giai hCaptcha MIEN PHI
Su dung ke thuat anti-detection va image recognition
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def human_like_click(driver, element):
    """Click nhu nguoi that"""
    try:
        # Di chuyen chuot den element
        actions = ActionChains(driver)
        actions.move_to_element(element)
        time.sleep(random.uniform(0.1, 0.3))
        actions.click()
        actions.perform()
        time.sleep(random.uniform(0.2, 0.5))
    except:
        element.click()


def solve_hcaptcha_checkbox(driver, max_attempts=3):
    """
    Giai hCaptcha bang cach click checkbox va doi
    Phuong phap nay loi dung viec hCaptcha co the khong hien challenge neu:
    - Bot detection score thap
    - Hanh vi giong nguoi that
    - IP/Browser tot
    """
    
    for attempt in range(max_attempts):
        try:
            print(f"\n[*] Thu giai hCaptcha lan {attempt + 1}/{max_attempts}...")
            
            # Doi iframe hcaptcha xuat hien
            time.sleep(2)
            
            # Tim tat ca iframe
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            hcaptcha_iframe = None
            
            for iframe in iframes:
                src = iframe.get_attribute("src") or ""
                if "hcaptcha" in src.lower():
                    hcaptcha_iframe = iframe
                    break
            
            if not hcaptcha_iframe:
                print("[!] Khong tim thay iframe hCaptcha")
                return False
            
            # Chuyen vao iframe hcaptcha
            driver.switch_to.frame(hcaptcha_iframe)
            
            # Tim va click checkbox
            try:
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "checkbox"))
                )
                
                print("[*] Da tim thay checkbox hCaptcha")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Click nhu nguoi that
                human_like_click(driver, checkbox)
                print("[*] Da click checkbox")
                
                # Doi ket qua
                time.sleep(3)
                
                # Kiem tra xem co phai giai challenge khong
                driver.switch_to.default_content()
                
                # Neu khong co challenge popup => thanh cong
                time.sleep(2)
                challenge_iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'hcaptcha') and contains(@title, 'challenge')]")
                
                if not challenge_iframes:
                    print("[OK] Giai hCaptcha thanh cong (khong co challenge)!")
                    return True
                else:
                    print("[!] Co challenge xuat hien, can giai thu cong...")
                    return False
                    
            except Exception as e:
                print(f"[!] Loi khi click checkbox: {e}")
                driver.switch_to.default_content()
                
        except Exception as e:
            print(f"[ERROR] Loi: {e}")
            driver.switch_to.default_content()
    
    return False


def solve_hcaptcha_manual(driver, timeout=120):
    """
    Cho user giai hCaptcha thu cong
    """
    print("\n" + "="*60)
    print("HCAPTCHA - CAN GIAI THU CONG")
    print("="*60)
    print("HUONG DAN:")
    print("1. Nhin vao trinh duyet Chrome")
    print("2. Chon tat ca hinh co 'stairs' (cau thang)")
    print("3. Click nut 'VERIFY' mau xanh")
    print("4. Doi cho den khi captcha bien mat")
    print("5. Quay lai terminal va nhan Enter")
    print(f"\nBan co {timeout}s de giai...")
    print("="*60)
    
    try:
        input("\n>>> Nhan Enter sau khi da giai xong...")
        print("[OK] Tiep tuc...")
        time.sleep(2)
        return True
    except KeyboardInterrupt:
        print("\n[!] Da huy")
        return False


def check_hcaptcha_exists(driver):
    """Kiem tra xem co hCaptcha tren trang khong"""
    try:
        # Cach 1: Tim iframe chua "hcaptcha" trong src
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            title = iframe.get_attribute("title") or ""
            if "hcaptcha" in src.lower() or "hcaptcha" in title.lower():
                print(f"    [DEBUG] Tim thay hCaptcha iframe: {src[:50]}...")
                return True
        
        # Cach 2: Tim div chua class "h-captcha"
        divs = driver.find_elements(By.CSS_SELECTOR, "div.h-captcha, div[data-sitekey]")
        if divs:
            print(f"    [DEBUG] Tim thay {len(divs)} div h-captcha")
            return True
        
        # Cach 3: Tim bang XPath
        elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'h-captcha') or contains(@id, 'hcaptcha')]")
        if elements:
            print(f"    [DEBUG] Tim thay {len(elements)} element h-captcha")
            return True
        
        return False
    except Exception as e:
        print(f"    [DEBUG] Loi kiem tra hCaptcha: {e}")
        return False


def auto_solve_hcaptcha(driver, method="auto"):
    """
    Tu dong giai hCaptcha
    
    Methods:
    - "auto": Thu tu dong truoc, neu khong duoc thi thu cong
    - "manual": Luon giai thu cong
    - "smart": Thu nhieu phuong phap (recommended)
    """
    
    try:
        # Kiem tra co hCaptcha khong
        if not check_hcaptcha_exists(driver):
            print("[*] Khong phat hien hCaptcha")
            return True
        
        print("\n[!] PHAT HIEN HCAPTCHA!")
        
        if method == "manual":
            return solve_hcaptcha_manual(driver)
        
        elif method == "auto" or method == "smart":
            # Thu phuong phap tu dong truoc
            print("[*] Dang thu giai tu dong...")
            
            if solve_hcaptcha_checkbox(driver, max_attempts=3):
                return True
            
            # Neu khong duoc, chuyen sang thu cong
            print("[!] Khong the giai tu dong")
            print("[*] Chuyen sang che do thu cong...")
            return solve_hcaptcha_manual(driver, timeout=120)
        
        return False
        
    except Exception as e:
        print(f"[ERROR] Loi giai hCaptcha: {e}")
        return False


def wait_for_hcaptcha_solve(driver, timeout=60):
    """
    Doi cho den khi hCaptcha duoc giai (tu dong hoac thu cong)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if not check_hcaptcha_exists(driver):
            print("[OK] hCaptcha da duoc giai!")
            return True
        time.sleep(1)
    
    print("[!] Timeout - hCaptcha van chua duoc giai")
    return False


# ========== PHUONG PHAP BOI SUNG ==========

def inject_hcaptcha_bypass_script(driver):
    """
    Inject JavaScript de bypass mot so loai hCaptcha
    CANH BAO: Phuong phap nay co the khong hieu qua va vi pham TOS
    """
    try:
        script = """
        // Inject script de thay doi bot detection score
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
        });
        
        // Override cac ham phat hien automation
        window.navigator.chrome = {
            runtime: {}
        };
        
        // Fake canvas fingerprint
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {
            if (type === 'image/png' && this.width === 280 && this.height === 60) {
                return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
            }
            return originalToDataURL.apply(this, arguments);
        };
        """
        
        driver.execute_script(script)
        print("[*] Da inject bypass script")
        return True
    except Exception as e:
        print(f"[!] Khong the inject script: {e}")
        return False


def use_hcaptcha_cookie(driver, cookie_data=None):
    """
    Su dung cookie de giam ti le bi hCaptcha
    """
    try:
        if cookie_data:
            for cookie in cookie_data:
                driver.add_cookie(cookie)
            print("[*] Da them hCaptcha cookies")
            return True
    except Exception as e:
        print(f"[!] Loi khi them cookie: {e}")
    return False
