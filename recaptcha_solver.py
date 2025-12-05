"""
reCAPTCHA Solver - Tu dong giai reCAPTCHA cho GoLike
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_recaptcha_exists(driver):
    """Kiem tra xem co reCAPTCHA khong"""
    try:
        # Tim iframe recaptcha
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            title = iframe.get_attribute("title") or ""
            if "recaptcha" in src.lower() or "recaptcha" in title.lower():
                print(f"    [DEBUG] Tim thay reCAPTCHA: {title}")
                return True
        return False
    except Exception as e:
        print(f"    [DEBUG] Loi kiem tra reCAPTCHA: {e}")
        return False


def solve_recaptcha_v2(driver, max_attempts=3):
    """
    Giai reCAPTCHA v2 bang cach click checkbox
    Neu bot score thap => Pass luon
    """
    
    for attempt in range(max_attempts):
        try:
            print(f"\n[*] Thu giai reCAPTCHA lan {attempt + 1}/{max_attempts}...")
            
            # Doi mot chut
            time.sleep(2)
            
            # Tim iframe recaptcha anchor (checkbox)
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            recaptcha_iframe = None
            
            for iframe in iframes:
                src = iframe.get_attribute("src") or ""
                if "recaptcha/api2/anchor" in src:
                    recaptcha_iframe = iframe
                    break
            
            if not recaptcha_iframe:
                print("[!] Khong tim thay iframe reCAPTCHA")
                return False
            
            # Chuyen vao iframe
            driver.switch_to.frame(recaptcha_iframe)
            
            # Tim va click checkbox
            try:
                # Doi checkbox xuat hien
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
                )
                
                print("[*] Da tim thay checkbox reCAPTCHA")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Click checkbox
                checkbox.click()
                print("[*] Da click checkbox")
                
                # Doi ket qua
                time.sleep(3)
                
                # Kiem tra xem da duoc tick chua
                try:
                    checked = checkbox.get_attribute("aria-checked")
                    if checked == "true":
                        print("[OK] reCAPTCHA da duoc tick (khong co challenge)!")
                        driver.switch_to.default_content()
                        return True
                except:
                    pass
                
                # Quay lai frame chinh
                driver.switch_to.default_content()
                
                # Kiem tra co challenge popup khong
                time.sleep(2)
                challenge_iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha/api2/bframe')]")
                
                if not challenge_iframes:
                    print("[OK] Giai reCAPTCHA thanh cong (khong co challenge)!")
                    return True
                else:
                    print("[!] Co challenge xuat hien (can giai thu cong)")
                    return False
                    
            except Exception as e:
                print(f"[!] Loi khi click checkbox: {e}")
                driver.switch_to.default_content()
                
        except Exception as e:
            print(f"[ERROR] Loi: {e}")
            driver.switch_to.default_content()
    
    return False


def solve_recaptcha_manual(driver, timeout=120):
    """
    Cho user giai reCAPTCHA thu cong
    """
    print("\n" + "="*60)
    print("reCAPTCHA - CAN GIAI THU CONG")
    print("="*60)
    print("HUONG DAN:")
    print("1. Nhin vao trinh duyet Chrome")
    print("2. Click vao checkbox 'I'm not a robot'")
    print("3. Neu co challenge, chon hinh theo yeu cau")
    print("4. Doi cho den khi checkbox duoc tick")
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


def auto_solve_recaptcha(driver, method="smart"):
    """
    Tu dong giai reCAPTCHA
    
    Methods:
    - "auto": Thu tu dong (checkbox + audio)
    - "manual": Luon giai thu cong
    - "smart": Thu checkbox -> audio -> manual (recommended)
    """
    
    try:
        # Kiem tra co reCAPTCHA khong
        if not check_recaptcha_exists(driver):
            print("[*] Khong phat hien reCAPTCHA")
            return True
        
        print("\n[!] PHAT HIEN reCAPTCHA!")
        
        if method == "manual":
            return solve_recaptcha_manual(driver)
        
        elif method == "auto" or method == "smart":
            # BUOC 1: Thu click checkbox truoc
            print("[*] Buoc 1: Thu click checkbox...")
            
            if solve_recaptcha_v2(driver, max_attempts=2):
                print("[OK] Pass luon sau khi click checkbox!")
                return True
            
            # BUOC 2: Neu co challenge, thu audio
            print("[*] Buoc 2: Thu giai bang audio challenge...")
            
            try:
                from recaptcha_audio_solver import solve_recaptcha_with_retry
                
                if solve_recaptcha_with_retry(driver, max_audio_attempts=2):
                    print("[OK] Giai audio thanh cong!")
                    return True
            except ImportError:
                print("[!] Chua cai thu vien audio (SpeechRecognition, pydub)")
                print("[*] Chay: pip install SpeechRecognition pydub")
            except Exception as e:
                print(f"[!] Loi audio solver: {e}")
            
            # BUOC 3: Neu audio cung khong duoc, chuyen sang thu cong
            if method == "smart":
                print("[*] Buoc 3: Chuyen sang che do thu cong...")
                return solve_recaptcha_manual(driver, timeout=120)
            else:
                return False
        
        return False
        
    except Exception as e:
        print(f"[ERROR] Loi giai reCAPTCHA: {e}")
        return False


def wait_for_recaptcha_solve(driver, timeout=60):
    """
    Doi cho den khi reCAPTCHA duoc giai
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if not check_recaptcha_exists(driver):
            print("[OK] reCAPTCHA da duoc giai!")
            return True
        time.sleep(1)
    
    print("[!] Timeout - reCAPTCHA van chua duoc giai")
    return False
