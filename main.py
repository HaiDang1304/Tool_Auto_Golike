import json
import re
import random
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from recaptcha_solver import auto_solve_recaptcha, check_recaptcha_exists
from smart_captcha_detector import smart_detect_all_captchas, is_captcha_required, get_solvable_captcha
from tiktok_handler import auto_tiktok_job
from youtube_handler import auto_youtube_job
from login_checker import ensure_platform_login, check_platform_login
from account_manager import AccountManager
from auto_login import auto_login_platform

def random_sleep(min_sec=1, max_sec=3):
    """Sleep thoi gian ngau nhien de tranh bi phat hien bot"""
    sleep(random.uniform(min_sec, max_sec))

def human_like_typing(element, text, min_delay=0.1, max_delay=0.3):
    """Nhap text nhu nguoi that - cham va tu nhien"""
    element.clear()
    sleep(random.uniform(0.3, 0.7))  # Doi sau khi clear
    
    for char in text:
        element.send_keys(char)
        # Ngau nhien co nhung ky tu go nhanh, co ky tu go cham
        if random.random() < 0.1:  # 10% go cham hon
            sleep(random.uniform(max_delay, max_delay * 2))
        else:
            sleep(random.uniform(min_delay, max_delay))
    
    # Doi mot chut sau khi go xong (nhu nguoi that suy nghi)
    sleep(random.uniform(0.3, 0.8))

def human_like_click(driver, element):
    """Click nhu nguoi that - co di chuyen chuot"""
    try:
        from selenium.webdriver.common.action_chains import ActionChains
        
        # Di chuyen den element (nhu nguoi that)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.2, 0.5))  # Dung mot chut
        actions.click()
        actions.perform()
        
        # Doi sau khi click
        sleep(random.uniform(0.3, 0.7))
    except Exception as e:
        # Fallback: Click thong thuong
        element.click()
        sleep(random.uniform(0.3, 0.7))

def scroll_randomly(driver):
    """Cuon trang ngau nhien mot chut (hanh vi tu nhien)"""
    try:
        scroll_amount = random.randint(100, 300)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        sleep(random.uniform(0.5, 1.0))
    except:
        pass

# ========== CAU HINH ==========
ACCOUNTS_FILE = "accounts.json"
LOGIN_URL = "https://app.golike.net/login"

CHANNEL_URLS = {
    "tiktok": "https://app.golike.net/jobs/tiktok",
    "shopee": "https://app.golike.net/jobs/shopee",
    "twitter": "https://app.golike.net/jobs/twitter",
    "youtube": "https://app.golike.net/jobs/youtube",
    "instagram": "https://app.golike.net/jobs/instagram",
    "traffic": "https://app.golike.net/jobs/traffic"
}

CHANNEL_NAMES = {
    "tiktok": "TikTok",
    "shopee": "Shopee",
    "twitter": "Twitter",
    "youtube": "Youtube",
    "instagram": "Instagram",
    "traffic": "Tang traffic"
}


def load_accounts():
    """Load tai khoan tu file JSON"""
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def show_menu():
    """Hien thi menu chon kenh"""
    print("\n" + "="*60)
    print("GOLIKE AUTO TOOL - CHON KENH NHIEM VU")
    print("="*60)
    print("\nCac kenh co san:")
    print("1. TikTok")
    print("2. Shopee")
    print("3. Twitter")
    print("4. Youtube")
    print("5. Instagram")
    print("6. Tang traffic")
    print("0. Thoat")
    print("="*60)
    
    while True:
        try:
            choice = input("\nChon kenh (1-6, 0 de thoat): ").strip()
            
            if choice == "0":
                return None
            elif choice == "1":
                return "tiktok"
            elif choice == "2":
                return "shopee"
            elif choice == "3":
                return "twitter"
            elif choice == "4":
                return "youtube"
            elif choice == "5":
                return "instagram"
            elif choice == "6":
                return "traffic"
            else:
                print("Lua chon khong hop le! Vui long chon lai.")
        except:
            print("Loi nhap lieu! Vui long chon lai.")


def check_and_solve_captcha(driver, auto_mode=True, max_retries=3):
    """Kiem tra THONG MINH va tu dong giai captcha NEU CAN"""
    try:
        print("\n[*] Dang quet trang web tim captcha...")
        
        # Buoc 1: Phat hien tat ca captcha
        captchas = smart_detect_all_captchas(driver, verbose=True)
        
        if not captchas:
            print("[OK] Khong co captcha - Bo qua")
            return False  # Khong co captcha = khong can giai
        
        # Buoc 2: Kiem tra xem co CAN giai khong
        print("\n[*] Kiem tra xem captcha co can giai khong...")
        
        if not is_captcha_required(driver, wait_time=1):
            print("[OK] Captcha da duoc xu ly hoac khong can giai")
            return False
        
        # Buoc 3: Lay captcha co the giai duoc
        solvable = get_solvable_captcha(driver)
        
        if not solvable:
            print("[!] Khong tim thay captcha co the giai (co the la reCAPTCHA v3)")
            return False
        
        # Buoc 4: Bat dau giai captcha
        captcha_type = solvable.get("type")
        print("\n" + "="*60)
        print(f"PHAT HIEN {captcha_type.upper()} - BAT DAU GIAI!")
        print("="*60)
        
        if auto_mode:
            # Thu giai tu dong nhieu lan
            for attempt in range(max_retries):
                print(f"\n[*] Lan thu {attempt + 1}/{max_retries}...")
                
                # Chon phuong phap giai phu hop
                if captcha_type == "recaptcha_v2":
                    success = auto_solve_recaptcha(driver, method="smart")
                elif captcha_type == "hcaptcha":
                    # Import hcaptcha solver neu can
                    try:
                        from hcaptcha_solver import auto_solve_hcaptcha
                        success = auto_solve_hcaptcha(driver, method="auto")
                    except ImportError:
                        print("[!] Khong tim thay hcaptcha_solver.py")
                        success = False
                else:
                    success = False
                
                if success:
                    print("[OK] Da giai captcha thanh cong!")
                    sleep(2)
                    
                    # Kiem tra lai xem captcha co con khong
                    if not is_captcha_required(driver, wait_time=1):
                        print("[OK] Xac nhan captcha da bien mat!")
                        return True
                    else:
                        print("[!] Captcha van con, thu lai...")
                        continue
                
                if attempt < max_retries - 1:
                    print(f"[!] That bai! Cho 3s truoc khi thu lai...")
                    sleep(3)
            
            print(f"\n[!] Da thu het {max_retries} lan nhung van khong giai duoc")
            print("[*] Chuyen sang che do thu cong...")
            return auto_solve_recaptcha(driver, method="manual")
        else:
            # Giai thu cong
            success = auto_solve_recaptcha(driver, method="manual")
            return success
        
    except Exception as e:
        print(f"[ERROR] Loi kiem tra captcha: {e}")
        import traceback
        traceback.print_exc()
        return False


def login_golike(driver, username, password):
    """Dang nhap GoLike - MO PHONG NGUOI THAT"""
    try:
        print("\n[*] Dang truy cap trang dang nhap GoLike...")
        driver.get(LOGIN_URL)
        
        # Doi lau hon de trang load hoan toan
        print("[*] Doi trang load...")
        sleep(random.uniform(4, 6))  # 4-6 giay (nguoi that thuong doi)
        
        # Cuon trang mot chut (hanh vi tu nhien)
        scroll_randomly(driver)
        sleep(random.uniform(1, 2))
        
        # Tim va click vao o username (nhu nguoi that)
        print("[*] Click vao o username...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @name='username']"))
        )
        
        # Di chuot den o username va click
        human_like_click(driver, username_input)
        sleep(random.uniform(0.5, 1.0))
        
        # Nhap username CHAM va TU NHIEN
        print("[*] Dang nhap username...")
        human_like_typing(username_input, username, min_delay=0.1, max_delay=0.3)
        
        # Doi mot chut truoc khi chuyen sang password (nhu nguoi that suy nghi)
        sleep(random.uniform(0.8, 1.5))
        
        # Tim va click vao o password
        print("[*] Click vao o password...")
        password_input = driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
        human_like_click(driver, password_input)
        sleep(random.uniform(0.5, 1.0))
        
        # Nhap password CHAM va TU NHIEN
        print("[*] Dang nhap password...")
        human_like_typing(password_input, password, min_delay=0.1, max_delay=0.25)
        
        # Doi lau truoc khi click nut dang nhap (nguoi that thuong kiem tra lai)
        sleep(random.uniform(1.0, 2.0))
        
        # Tim va click nut dang nhap
        print("[*] Click nut dang nhap...")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        human_like_click(driver, login_btn)
        
        print("[*] Dang doi server xu ly...")
        sleep(random.uniform(5, 7))  # Doi lau hon de server xu ly
        
        # QUAN TRONG: Kiem tra va giai captcha SAU KHI click login (neu co)
        print("[*] Kiem tra xem co captcha khong...")
        captcha_detected = check_and_solve_captcha(driver)
        
        if captcha_detected:
            print("[*] Da xu ly captcha, doi ket qua dang nhap...")
            sleep(3)
        else:
            print("[*] Khong co captcha hoac da duoc xu ly tu dong")
        
        # Kiem tra dang nhap thanh cong
        print("[*] Kiem tra ket qua dang nhap...")
        sleep(2)
        current_url = driver.current_url.lower()
        
        if "login" not in current_url:
            print("[OK] Dang nhap thanh cong!")
            return True
        else:
            # Van o trang login
            print("[!] Van o trang login")
            print("[*] Co the do:")
            print("    - Username/password sai")
            print("    - Captcha chua duoc giai")
            print("    - Can giai captcha thu cong")
            
            # Cho user mot co hoi nua
            print("\n[*] Neu ban thay captcha, hay giai roi nhan Enter...")
            print("[*] Hoac nhan Ctrl+C de thoat")
            try:
                input(">>> ")
                sleep(2)
                
                # Kiem tra lai URL
                if "login" not in driver.current_url.lower():
                    print("[OK] Dang nhap thanh cong!")
                    return True
                else:
                    print("[FAIL] Dang nhap that bai!")
                    return False
            except KeyboardInterrupt:
                return False
            
    except Exception as e:
        print(f"[ERROR] Loi dang nhap: {e}")
        return False


def do_one_job(driver, channel):
    """Lam 1 nhiem vu"""
    try:
        # Buoc 1: Doi trang load va tim nut "Nhan Job ngay"
        print("  [*] Doi trang load...")
        
        # Dung WebDriverWait de doi button xuat hien
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            print("  [OK] Trang da load xong")
        except:
            print("  [!] Trang load cham, doi them...")
        
        sleep(3)
        
        # Scroll xuong de load het cac job
        print("  [*] Scroll trang de load het cac job...")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            sleep(1)
        
        print("  [*] Tim nut 'Nhan Job ngay'...")
        
        # Thu nhieu cach tim nut "Nhan Job ngay" - dua tren screenshot thuc te
        job_buttons = []
        
        # Cach 1: Tim div chua button "Nhận Job ngay" (theo HTML structure thuc te)
        try:
            job_buttons = driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'btn') and contains(@class, 'btn-outline-light')]")
            if job_buttons:
                print(f"  [DEBUG] Tim thay {len(job_buttons)} nut qua class 'btn-outline-light'")
        except:
            pass
        
        if not job_buttons:
            # Cach 2: Tim button hoac div co text "Nhận Job ngay" chinh xac
            try:
                job_buttons = driver.find_elements(By.XPATH, 
                    "//*[contains(normalize-space(.), 'Nhận Job ngay')]")
                if job_buttons:
                    print(f"  [DEBUG] Tim thay {len(job_buttons)} nut qua text 'Nhận Job ngay'")
            except:
                pass
        
        if not job_buttons:
            # Cach 3: Tim theo text "Nhận Job" (co the thieu chu "ngay")
            try:
                job_buttons = driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Nhận Job') or contains(text(), 'Nhan Job')]")
                if job_buttons:
                    print(f"  [DEBUG] Tim thay {len(job_buttons)} nut qua text 'Nhận Job'")
            except:
                pass
        
        if not job_buttons:
            # Cach 4: Tim button co class btn-outline
            try:
                job_buttons = driver.find_elements(By.XPATH, 
                    "//button[contains(@class, 'btn-outline')] | //div[contains(@class, 'btn-outline')]")
                # Loc chi lay nhung nut co text lien quan
                job_buttons = [btn for btn in job_buttons if btn.is_displayed() and ('nhận' in btn.text.lower() or 'job' in btn.text.lower())]
                if job_buttons:
                    print(f"  [DEBUG] Tim thay {len(job_buttons)} nut qua class 'btn-outline'")
            except:
                pass
        
        if not job_buttons:
            # Cach 5: Tim theo icon fa-arrow (nhu trong screenshot)
            try:
                job_buttons = driver.find_elements(By.XPATH, 
                    "//*[.//i[contains(@class, 'fa-arrow-right')]]")
                if job_buttons:
                    # Loc chi lay nhung nut co text "Nhận Job"
                    job_buttons = [btn for btn in job_buttons if 'nhận' in btn.text.lower() and 'job' in btn.text.lower()]
                    if job_buttons:
                        print(f"  [DEBUG] Tim thay {len(job_buttons)} nut qua icon arrow")
            except:
                pass
        
        if not job_buttons:
            # Cach 6: Tim tat ca element clickable co text "Nhận Job ngay"
            try:
                all_clickable = driver.find_elements(By.XPATH, 
                    "//button | //div[@class[contains(., 'btn')]] | //a")
                for elem in all_clickable:
                    if elem.is_displayed():
                        text = elem.text.strip().lower()
                        if 'nhận job' in text and 'ngay' in text:
                            job_buttons = [elem]
                            print(f"  [DEBUG] Tim thay nut qua scan toan bo: '{elem.text.strip()}'")
                            break
            except:
                pass
        
        if not job_buttons:
            print("  [!] Khong tim thay nut nhan job lan 1!")
            print("  [DEBUG] Dang o URL:", driver.current_url)
            
            # Retry: Reload trang va thu lai
            print("  [*] Thu reload trang va tim lai...")
            driver.refresh()
            sleep(5)
            
            # Scroll lai
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                driver.execute_script("window.scrollTo(0, 0);")
                sleep(1)
            
            # Tim lai tat ca cach
            try:
                job_buttons = driver.find_elements(By.XPATH, "//button")
                job_buttons = [btn for btn in job_buttons if btn.is_displayed() and ('nhận' in btn.text.lower() or 'job' in btn.text.lower())]
            except:
                pass
            
            if not job_buttons:
                # Debug: In ra tat ca button
                print("  [DEBUG] Danh sach tat ca cac button:")
                try:
                    all_btns = driver.find_elements(By.TAG_NAME, "button")
                    for i, btn in enumerate(all_btns[:15]):  # In 15 button dau
                        try:
                            text = btn.text.strip()
                            classes = btn.get_attribute("class")
                            visible = btn.is_displayed()
                            print(f"    Button {i+1}: text='{text}', class='{classes}', visible={visible}")
                        except:
                            pass
                except:
                    pass
                
                # Luu screenshot
                try:
                    driver.save_screenshot("debug_no_job_button.png")
                    print("  [DEBUG] Da luu screenshot: debug_no_job_button.png")
                except:
                    pass
                
                print("  [!] Van khong tim thay nut nhan job! Dung lai nhiem vu nay.")
                return False, 0
        
        print(f"  [*] Tim thay {len(job_buttons)} nut job")
        
        # Loc lay button visible dau tien
        visible_btn = None
        for btn in job_buttons:
            try:
                if btn.is_displayed():
                    # Kiem tra xem co phai la button hoac div clickable khong
                    tag_name = btn.tag_name.lower()
                    if tag_name in ['button', 'div', 'a']:
                        visible_btn = btn
                        break
            except:
                continue
        
        if not visible_btn and job_buttons:
            # Lay phan tu dau tien neu khong tim thay visible
            visible_btn = job_buttons[0]
        
        if not visible_btn:
            print("  [!] Khong co nut nao co the click!")
            return False, 0
        
        # Debug: Hien thi thong tin nut se click
        try:
            btn_text = visible_btn.text.strip()
            btn_class = visible_btn.get_attribute("class")
            btn_tag = visible_btn.tag_name
            print(f"  [DEBUG] Se click element: tag='{btn_tag}', text='{btn_text}', class='{btn_class}'")
        except:
            pass
        
        # Scroll den nut va click
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", visible_btn)
            sleep(1)
            
            # Highlight button truoc khi click (de ban thay)
            driver.execute_script("arguments[0].style.border='3px solid red'", visible_btn)
            sleep(0.5)
            
            # Thu click bang JavaScript (nhanh hon va it loi hon)
            driver.execute_script("arguments[0].click();", visible_btn)
            print("  [OK] Da click 'Nhan Job ngay'")
            sleep(5)
        except Exception as e:
            print(f"  [!] Loi khi click nut: {e}")
            # Thu click truc tiep
            try:
                visible_btn.click()
                print("  [OK] Da click 'Nhan Job ngay' (cach 2)")
                sleep(5)
            except:
                print("  [!] Khong the click nut!")
                return False, 0
        
        # Buoc 2: Trang chi tiet job hien thi (Hinh 1) - Tim nut Shopee/TikTok/etc
        print("  [*] Doi trang chi tiet job load...")
        sleep(3)
        
        # Chi kiem tra captcha neu co dau hieu (optional - chi khi can)
        # if check_and_solve_captcha(driver, auto_mode=True):
        #     print("  [OK] Da xu ly captcha")
        #     sleep(3)
        
        print("  [*] Tim nut kenh (Shopee/TikTok/Youtube...)...")
        
        # Tim nut kenh - co the la button hoac link (nhu trong Hinh 1)
        channel_buttons = []
        
        # Cach 1: Tim button co icon + text kenh (theo hinh 1 - nut Shopee mau cam/trang)
        if channel == "shopee":
            # Tim button/div co chua text "Shopee"
            channel_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(normalize-space(.), 'Shopee')] | //div[@role='button' and contains(., 'Shopee')]")
            
            if not channel_buttons:
                # Tim theo icon Shopee (SVG)
                channel_buttons = driver.find_elements(By.XPATH,
                    "//*[local-name()='svg' and contains(@class, 'shopee')]/ancestor::button")
            
            if not channel_buttons:
                # Tim button co background gradient cam (mau Shopee)
                all_btns = driver.find_elements(By.TAG_NAME, "button")
                for btn in all_btns:
                    if btn.is_displayed():
                        style = btn.get_attribute("style") or ""
                        class_name = btn.get_attribute("class") or ""
                        if "gradient" in style.lower() or "gradient" in class_name.lower():
                            if "shopee" in btn.text.lower() or btn.text.strip() == "":
                                channel_buttons = [btn]
                                break
        
        elif channel == "tiktok":
            channel_buttons = driver.find_elements(By.XPATH,
                "//button[contains(., 'TikTok') or contains(., 'Tiktok')] | //div[@role='button' and contains(., 'TikTok')]")
        
        elif channel == "youtube":
            channel_buttons = driver.find_elements(By.XPATH,
                "//button[contains(., 'Youtube') or contains(., 'YouTube')] | //div[@role='button' and contains(., 'Youtube')]")
        
        # Cach 2: Tim link chua domain kenh
        if not channel_buttons:
            channel_buttons = driver.find_elements(By.XPATH, 
                f"//a[contains(@href, '{channel}.')]")
        
        # Cach 3: Tim trong container chi tiet job
        if not channel_buttons:
            # Tim tat ca button visible
            all_btns = driver.find_elements(By.XPATH, "//button | //div[@role='button'] | //a[@href]")
            for btn in all_btns:
                try:
                    if btn.is_displayed():
                        text = btn.text.strip().lower()
                        href = btn.get_attribute("href") or ""
                        if channel.lower() in text or channel.lower() in href:
                            channel_buttons = [btn]
                            break
                except:
                    continue
        
        if not channel_buttons:
            print("  [!] Khong tim thay nut kenh!")
            print("  [DEBUG] Dang o URL:", driver.current_url)
            
            # Debug: In ra cac button co san
            print("  [DEBUG] Cac button/link co san:")
            try:
                all_elements = driver.find_elements(By.XPATH, "//button | //a[@href]")
                for i, elem in enumerate(all_elements[:10]):
                    if elem.is_displayed():
                        text = elem.text.strip()
                        href = elem.get_attribute("href") or ""
                        tag = elem.tag_name
                        print(f"    {i+1}. {tag}: text='{text}', href='{href[:50]}'")
            except:
                pass
            
            # Luu screenshot
            try:
                driver.save_screenshot("debug_no_channel_button.png")
                print("  [DEBUG] Da luu screenshot: debug_no_channel_button.png")
            except:
                pass
            return False, 0
        
        print(f"  [*] Tim thay {len(channel_buttons)} nut kenh")
        
        # Debug: Hien thi thong tin nut se click
        try:
            btn_text = channel_buttons[0].text.strip()
            btn_href = channel_buttons[0].get_attribute("href") or "N/A"
            print(f"  [DEBUG] Se click: text='{btn_text}', href='{btn_href[:50]}'")
        except:
            pass
        
        # Luu tab hien tai (GoLike - Hinh 1)
        original_window = driver.current_window_handle
        
        # Click vao nut kenh de mo trang Shopee/TikTok (sang Hinh 2 hoac 4)
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", channel_buttons[0])
            sleep(1)
            
            # Highlight truoc khi click
            driver.execute_script("arguments[0].style.border='3px solid blue'", channel_buttons[0])
            sleep(0.5)
            
            driver.execute_script("arguments[0].click();", channel_buttons[0])
            print(f"  [OK] Da click vao nut {channel.upper()}")
            sleep(5)
        except Exception as e:
            print(f"  [!] Loi khi click nut kenh: {e}")
            # Thu click truc tiep
            try:
                channel_buttons[0].click()
                print(f"  [OK] Da click vao nut {channel.upper()} (cach 2)")
                sleep(5)
            except:
                print("  [!] Khong the click nut kenh!")
                return False, 0
        
        # Buoc 3: Chuyen sang tab moi (Shopee/TikTok - Hinh 2, 4)
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            # Chuyen sang tab moi
            new_window = [w for w in all_windows if w != original_window][0]
            driver.switch_to.window(new_window)
            print(f"  [*] Dang o trang {channel.upper()}...")
            
            # Doi load trang
            sleep(5)
            
            # QUAN TRONG: Kiem tra dang nhap truoc khi lam job
            print("\n[*] Kiem tra trang thai dang nhap...")
            is_logged_in = ensure_platform_login(driver, channel, auto_prompt=True)
            
            if not is_logged_in:
                print("\n[!] KHONG THE LAM JOB - Chua dang nhap!")
                print("[!] Job nay se KHONG DUOC TINH va KHONG TRA TIEN")
                print("[*] Bam Enter de bao loi va bo qua job nay...")
                input(">>> ")
                
                # Dong tab va quay lai
                driver.close()
                driver.switch_to.window(original_window)
                
                # Bao loi job
                print("  [*] Bao loi job (chua dang nhap)...")
                return False
            
            # Thuc hien hanh dong tuy theo kenh
            action_success = False
            
            try:
                if channel == "shopee":
                    # Shopee: Tim nut "Yeu thich" (icon trai tim) hoac "Theo doi" (+ Theo Doi)
                    print("  [*] Tim nut Yeu thich hoac Theo doi...")
                    
                    # Cach 1: Tim nut "Da thich" hoac icon trai tim
                    like_btns = driver.find_elements(By.XPATH,
                        "//button[contains(@class, 'shopee-button-') and (@aria-label[contains(., 'thích')] or contains(., 'Thích'))]")
                    
                    if not like_btns:
                        # Cach 2: Tim button co text "Đã thích"
                        like_btns = driver.find_elements(By.XPATH,
                            "//button[contains(., 'Đã thích') or contains(., 'Thích')]")
                    
                    if not like_btns:
                        # Cach 3: Tim icon trai tim (svg heart)
                        like_btns = driver.find_elements(By.XPATH,
                            "//*[name()='svg' and contains(@class, 'heart')]/ancestor::button")
                    
                    if not like_btns:
                        # Cach 4: Tim nut "Theo Dõi" (+ Theo Doi)
                        like_btns = driver.find_elements(By.XPATH,
                            "//button[contains(., 'Theo Dõi') or contains(., '+ Theo Dõi')]")
                    
                    if not like_btns:
                        # Cach 5: Tim theo class button-solid (nut Theo Doi)
                        like_btns = driver.find_elements(By.XPATH,
                            "//button[contains(@class, 'button-solid')]")
                    
                    if like_btns:
                        # Scroll den nut
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_btns[0])
                        sleep(1)
                        
                        # Click
                        driver.execute_script("arguments[0].click();", like_btns[0])
                        print("  [OK] Da click Yeu thich/Theo doi!")
                        action_success = True
                        sleep(3)
                    else:
                        print("  [!] Khong tim thay nut Yeu thich/Theo doi")
                        # Luu screenshot
                        try:
                            driver.save_screenshot("debug_shopee_no_like.png")
                            print("  [DEBUG] Da luu screenshot: debug_shopee_no_like.png")
                        except:
                            pass
                
                elif channel == "tiktok":
                    # TikTok: Sử dụng handler chuyên dụng
                    print("  [*] Xử lý TikTok job...")
                    
                    # Phát hiện loại job (follow, like, comment, share)
                    job_type = "follow"  # Mặc định là follow
                    
                    # Kiểm tra URL để xác định loại job
                    try:
                        current_url = driver.current_url.lower()
                        if "/@" in current_url and "/video/" not in current_url:
                            job_type = "follow"  # Profile page -> Follow
                        elif "/video/" in current_url:
                            # Video page -> có thể là like hoặc comment
                            job_type = "like"  # Mặc định like video
                    except:
                        job_type = "follow"
                    
                    action_success = auto_tiktok_job(driver, job_type)
                    
                    if action_success:
                        print(f"  [OK] Đã hoàn thành TikTok {job_type}!")
                    else:
                        print(f"  [!] Không thể thực hiện TikTok {job_type}")
                    
                    sleep(2)
                
                elif channel == "youtube":
                    # YouTube: Sử dụng handler chuyên dụng
                    print("  [*] Xử lý YouTube job...")
                    
                    # Phát hiện loại job
                    job_type = "subscribe"  # Mặc định là subscribe
                    
                    # Kiểm tra URL
                    current_url = driver.current_url.lower()
                    if "/watch?v=" in current_url:
                        # Video page -> like hoặc comment
                        job_type = "like"  # Mặc định like
                    elif "/@" in current_url or "/channel/" in current_url or "/c/" in current_url:
                        job_type = "subscribe"  # Channel page -> Subscribe
                    
                    action_success = auto_youtube_job(driver, job_type)
                    
                    if action_success:
                        print(f"  [OK] Đã hoàn thành YouTube {job_type}!")
                    else:
                        print(f"  [!] Không thể thực hiện YouTube {job_type}")
                    
                    sleep(2)
                
                elif channel in ["instagram", "twitter"]:
                    # Instagram/Twitter: Tim nut Follow
                    follow_btns = driver.find_elements(By.XPATH,
                        "//button[contains(text(), 'Follow')]")
                    if follow_btns:
                        driver.execute_script("arguments[0].click();", follow_btns[0])
                        print(f"  [OK] Da follow {channel.upper()}!")
                        action_success = True
                        sleep(2)
                
                if not action_success:
                    print("  [*] Khong tim thay nut action, doi them...")
                    sleep(5)
                    
            except Exception as e:
                print(f"  [!] Loi khi thuc hien action: {e}")
                sleep(3)
            
            # Dong tab Shopee/TikTok va quay lai tab GoLike (Hinh 1)
            driver.close()
            driver.switch_to.window(original_window)
            print("  [OK] Da dong tab va quay lai GoLike")
            sleep(3)
        
        # Buoc 4: Click nut "Hoan thanh" (Hinh 1 - nut mau xanh)
        print("  [*] Tim nut 'Hoan thanh'...")
        sleep(2)
        
        # Scroll de thay nut
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        
        # Tim nut Hoan thanh
        complete_buttons = []
        
        # Cach 1: Tim button co text "Hoàn thành"
        complete_buttons = driver.find_elements(By.XPATH,
            "//button[contains(., 'Hoàn thành') or contains(., 'hoàn thành') or contains(., 'HOÀN THÀNH')]")
        
        if not complete_buttons:
            # Cach 2: Tim div hoac element co text "Hoàn thành"
            complete_buttons = driver.find_elements(By.XPATH,
                "//*[contains(text(), 'Hoàn thành')]")
        
        if not complete_buttons:
            # Cach 3: Tim theo class (nut mau xanh - success/primary)
            complete_buttons = driver.find_elements(By.XPATH,
                "//button[contains(@class, 'success') or contains(@class, 'primary')]")
            # Loc lai
            complete_buttons = [btn for btn in complete_buttons if 'hoàn' in btn.text.lower() or 'thành' in btn.text.lower()]
        
        if complete_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", complete_buttons[0])
                sleep(1)
                driver.execute_script("arguments[0].click();", complete_buttons[0])
                print("  [OK] Da bam 'Hoan thanh'!")
                sleep(3)
            except Exception as e:
                print(f"  [!] Loi khi click Hoan thanh: {e}")
        else:
            print("  [!] Khong tim thay nut 'Hoan thanh'")
            print("  [*] Co the nhiem vu tu dong hoan thanh")
        
        # Buoc 5: Xu ly popup "Thanh cong" (Hinh 3) - Click OK
        print("  [*] Kiem tra popup thanh cong...")
        sleep(3)
        
        popup_clicked = False
        try:
            # Cach 1: Tim nut OK chinh xac (trong popup)
            ok_buttons = driver.find_elements(By.XPATH,
                "//button[normalize-space(.)='OK' or normalize-space(.)='Ok']")
            
            if not ok_buttons:
                # Cach 2: Tim button trong modal/swal
                ok_buttons = driver.find_elements(By.XPATH,
                    "//div[contains(@class, 'swal') or contains(@class, 'modal') or contains(@class, 'popup')]//button[contains(., 'OK')]")
            
            if not ok_buttons:
                # Cach 3: Tim tat ca button visible co text OK
                all_btns = driver.find_elements(By.TAG_NAME, "button")
                for btn in all_btns:
                    try:
                        if btn.is_displayed() and btn.text.strip().upper() == 'OK':
                            ok_buttons = [btn]
                            break
                    except:
                        continue
            
            # Click nut OK
            if ok_buttons:
                for btn in ok_buttons:
                    try:
                        if btn.is_displayed():
                            # Highlight truoc khi click
                            driver.execute_script("arguments[0].style.border='3px solid green'", btn)
                            sleep(0.5)
                            
                            driver.execute_script("arguments[0].click();", btn)
                            print("  [OK] Da click OK tren popup Thanh cong!")
                            popup_clicked = True
                            sleep(2)
                            break
                    except Exception as e:
                        print(f"  [DEBUG] Thu click nut OK khac: {e}")
                        continue
            
            if not popup_clicked:
                print("  [*] Khong tim thay nut OK hoac popup da tu dong dong")
                # Cho them 2s phong truong hop popup tu dong dong
                sleep(2)
                
        except Exception as e:
            print(f"  [DEBUG] Loi xu ly popup: {e}")
        
        # Buoc 6: Quay lai trang jobs de tiep tuc vong lap
        print("  [*] Quay lai trang jobs...")
        try:
            # Kiem tra xem co dang o trang chi tiet job khong
            current_url = driver.current_url
            
            # Neu dang o trang chi tiet job, quay lai trang list jobs
            if 'job' not in current_url or '/jobs/' not in current_url:
                # Quay lai trang jobs
                channel_url = CHANNEL_URLS.get(channel)
                if channel_url:
                    driver.get(channel_url)
                    print(f"  [OK] Da quay lai trang {channel.upper()} jobs")
                    sleep(3)
            else:
                # Da o trang jobs roi, chi can reload
                driver.refresh()
                print("  [OK] Da refresh trang jobs")
                sleep(3)
                
        except Exception as e:
            print(f"  [!] Loi khi quay lai trang jobs: {e}")
        
        # Lay so tien thuong
        coin = 0
        try:
            coin_elements = driver.find_elements(By.XPATH,
                "//*[contains(text(), 'kiếm được') or contains(text(), 'đ')]")
            for elem in coin_elements:
                text = elem.text
                if 'đ' in text or 'kiem' in text.lower():
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        coin = int(numbers[0])
                        break
        except:
            coin = 0
        
        return True, coin
        
    except Exception as e:
        print(f"  [ERROR] Loi: {e}")
        return False, 0


def do_jobs_for_channel(driver, channel, max_jobs, account_data=None):
    """Lam nhiem vu cho 1 kenh"""
    channel_url = CHANNEL_URLS.get(channel)
    if not channel_url:
        print(f"[ERROR] Kenh {channel} khong hop le!")
        return 0, 0
    
    print(f"\n{'='*60}")
    print(f"KENH: {CHANNEL_NAMES.get(channel, channel.upper())}")
    print(f"{'='*60}")
    
    # BUOC 1: Auto login vao platform neu co credentials
    if account_data and channel in ['shopee', 'tiktok', 'youtube', 'instagram', 'twitter']:
        platform_creds = account_data.get('platforms', {}).get(channel, {})
        
        if platform_creds and platform_creds.get('username') and platform_creds.get('password'):
            print(f"\n[*] Phat hien thong tin dang nhap {channel.upper()}...")
            
            # Kiem tra xem da login chua
            if not check_platform_login(driver, channel):
                print(f"[*] Chua dang nhap {channel.upper()}, bat dau auto login...")
                
                # Lay cookies file path
                cookie_file = None
                if account_data.get('settings', {}).get('save_cookies', True):
                    acc_manager = AccountManager()
                    cookie_file = acc_manager.get_cookie_path(account_data.get('name', 'default'), channel)
                
                # Auto login
                success = auto_login_platform(driver, channel, platform_creds, cookie_file)
                
                if success:
                    print(f"[OK] Da dang nhap {channel.upper()} thanh cong!")
                else:
                    print(f"[!] Khong the auto login {channel.upper()}")
                    print(f"[*] Ban co the dang nhap thu cong sau khi mo job...")
            else:
                print(f"[OK] Da dang nhap {channel.upper()} roi!")
    
    # BUOC 2: Vao trang kenh GoLike
    print(f"\n[*] Dang vao kenh {channel.upper()} tren GoLike...")
    print(f"[*] URL: {channel_url}")
    driver.get(channel_url)
    sleep(5)
    
    # Kiem tra da vao dung trang chua
    current_url = driver.current_url
    print(f"[*] Da vao trang: {current_url}")
    
    if "login" in current_url.lower():
        print("[ERROR] Bi quay lai trang login! Co the phien dang nhap het han.")
        return 0, 0
    
    # Pause de ban xem trang (chi dung khi debug)
    # print("[DEBUG] Da vao trang kenh. Nhan Enter de tiep tuc...")
    # input()
    
    completed = 0
    total_coins = 0
    
    # Lam nhiem vu lien tuc
    for i in range(max_jobs):
        print(f"\nNHIEM VU #{i+1}:")
        
        success, coin = do_one_job(driver, channel)
        
        if not success:
            print(f"  [!] Khong the lam nhiem vu. Dung lai.")
            break
        
        completed += 1
        total_coins += coin
        
        if coin > 0:
            print(f"  => Nhan duoc: {coin} xu")
        
        print(f"  => TONG: {completed} nhiem vu | {total_coins} xu")
        
        # Doi truoc khi lam nhiem vu tiep theo
        sleep(3)
    
    return completed, total_coins


def run_bot(channel, max_jobs=50, account_data=None):
    """Chay bot cho 1 kenh"""
    
    # Load accounts neu chua co
    if account_data is None:
        try:
            acc_manager = AccountManager()
            accounts = acc_manager.get_enabled_accounts()
            
            if not accounts:
                print("\n[ERROR] Khong tim thay tai khoan nao duoc bat!")
                print("Vui long bat tai khoan trong file accounts_full.json")
                return
            
            # Chon tai khoan tu menu
            from account_manager import show_account_menu
            account_data = show_account_menu(acc_manager)
            if account_data is None:
                print("\n[*] Da huy chon tai khoan")
                return
        except FileNotFoundError:
            # Fallback: Dung file accounts.json cu
            print("\n[!] Khong tim thay accounts_full.json, dung accounts.json...")
            accounts = load_accounts()
            account = None
            for acc in accounts:
                if acc.get('enabled', False):
                    account = acc
                    break
            
            if not account:
                print("\n[ERROR] Khong tim thay tai khoan nao duoc bat!")
                return
            
            account_data = {
                'name': account.get('name', 'Unknown'),
                'golike': {
                    'username': account.get('username', ''),
                    'password': account.get('password', '')
                }
            }
    
    username = account_data.get('golike', {}).get('username', '')
    password = account_data.get('golike', {}).get('password', '')
    account_name = account_data.get('name', 'Unknown')
    
    print(f"\n{'='*60}")
    print(f"TAI KHOAN: {account_name}")
    print(f"{'='*60}")
    
    # Khoi tao trinh duyet (undetected-chromedriver + stealth)
    print("\n[*] Dang khoi dong Chrome (Anti-Detection Mode)...")
    
    try:
        # Cau hinh options don gian cho undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Khoi tao driver (undetected-chromedriver tu dong xu ly anti-detection)
        driver = uc.Chrome(
            options=options,
            use_subprocess=False,
            version_main=142,
            driver_executable_path=None
        )
        
        # Ap dung selenium-stealth de tang cuong anti-detection
        try:
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            print("[OK] Da ap dung Selenium Stealth")
        except Exception as e:
            print(f"[!] Khong the ap dung stealth (van co the hoat dong): {e}")
        
        print("[OK] Da khoi dong Chrome voi che do Anti-Detection")
        
    except Exception as e:
        print(f"[ERROR] Loi khoi tao Chrome: {e}")
        print("[*] Thu lai voi cau hinh don gian hon...")
        
        # Fallback: Khoi tao don gian nhat
        driver = uc.Chrome(use_subprocess=False)
        print("[OK] Da khoi dong Chrome (che do don gian)")
    
    try:
        # Dang nhap
        if not login_golike(driver, username, password):
            print("\n[ERROR] Khong the dang nhap! Dung lai.")
            return
        
        # Lam nhiem vu (truyen account_data de co the auto login platforms)
        completed, total_coins = do_jobs_for_channel(driver, channel, max_jobs, account_data)
        
        # Hien thi ket qua
        print(f"\n{'='*60}")
        print(f"KET QUA - {CHANNEL_NAMES.get(channel, channel.upper())}")
        print(f"{'='*60}")
        print(f"So nhiem vu hoan thanh: {completed}")
        print(f"Tong tien thuong: {total_coins} xu")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n[ERROR] Loi: {e}")
        import traceback
        traceback.print_exc()
        
        # Khong dong trinh duyet de debug
        print("\n[*] GIU TRINH DUYET MO DE DEBUG")
        print("[*] Nhan Enter de dong trinh duyet...")
        input()
    finally:
        try:
            print("\n[*] Dong trinh duyet...")
            driver.quit()
        except:
            pass


def main():
    """Chuong trinh chinh"""
    while True:
        # Hien thi menu chon kenh
        channel = show_menu()
        
        if channel is None:
            print("\n[*] Da thoat chuong trinh!")
            break
        
        # Nhap so luong nhiem vu
        try:
            max_jobs = int(input("\nNhap so luong nhiem vu (mac dinh 50): ").strip() or "50")
        except:
            max_jobs = 50
        
        print(f"\n[OK] Bat dau lam {max_jobs} nhiem vu cho kenh {CHANNEL_NAMES.get(channel, channel.upper())}...")
        
        # Chay bot
        run_bot(channel, max_jobs)
        
        # Hoi co muon tiep tuc khong
        continue_choice = input("\nBan co muon chon kenh khac? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n[*] Da thoat chuong trinh!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Da dung chuong trinh (Ctrl+C)")
    except Exception as e:
        print(f"\n[ERROR] Loi: {e}")
