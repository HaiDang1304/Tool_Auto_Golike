"""
AUTO CAPTCHA SOLVER - MIEN PHI
Su dung audio captcha va AI de giai captcha tu dong
"""

import time
import requests
import speech_recognition as sr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def solve_recaptcha_audio(driver):
    """Giai reCAPTCHA bang cach chuyen sang audio va dung speech recognition"""
    try:
        print("\n[*] Bat dau giai reCAPTCHA...")
        
        # Tim iframe recaptcha
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='recaptcha']"))
        )
        
        # Click checkbox recaptcha
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
        )
        checkbox.click()
        time.sleep(2)
        
        # Quay lai frame chinh
        driver.switch_to.default_content()
        
        # Chuyen sang iframe challenge
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title*='recaptcha challenge']"))
        )
        
        # Click nut audio
        audio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
        )
        audio_button.click()
        time.sleep(2)
        
        # Lay link file audio
        audio_source = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "audio-source"))
        )
        audio_url = audio_source.get_attribute("src")
        
        print(f"[*] Dang tai file audio: {audio_url}")
        
        # Tai file audio
        response = requests.get(audio_url)
        with open("captcha_audio.mp3", "wb") as f:
            f.write(response.content)
        
        # Chuyen doi audio sang text
        recognizer = sr.Recognizer()
        with sr.AudioFile("captcha_audio.mp3") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")
        
        print(f"[*] Nhan dang duoc: {text}")
        
        # Nhap ket qua
        input_field = driver.find_element(By.ID, "audio-response")
        input_field.send_keys(text.lower())
        
        # Click verify
        verify_button = driver.find_element(By.ID, "recaptcha-verify-button")
        verify_button.click()
        time.sleep(3)
        
        # Quay lai frame chinh
        driver.switch_to.default_content()
        
        print("[OK] Giai captcha thanh cong!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Loi giai captcha: {e}")
        driver.switch_to.default_content()
        return False


def solve_image_captcha_simple(driver):
    """Giai image captcha bang cach thu ngau nhien (khong hieu qua)"""
    try:
        print("\n[!] Image captcha kho giai tu dong!")
        print("[*] Dang thu phuong an ngau nhien...")
        
        # Tim tat ca cac o hinh
        images = driver.find_elements(By.CSS_SELECTOR, ".rc-imageselect-tile")
        
        if not images:
            return False
        
        # Click ngau nhien 3-4 o
        import random
        num_clicks = random.randint(3, 4)
        selected = random.sample(images, min(num_clicks, len(images)))
        
        for img in selected:
            img.click()
            time.sleep(0.3)
        
        # Click verify
        verify_btn = driver.find_element(By.ID, "recaptcha-verify-button")
        verify_btn.click()
        time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Loi: {e}")
        return False


def auto_solve_captcha(driver, method="audio"):
    """
    Tu dong giai captcha
    
    Methods:
    - "audio": Giai bang audio (tot nhat)
    - "random": Thu ngau nhien (kho thanh cong)
    - "manual": Cho user giai thu cong
    """
    
    if method == "audio":
        return solve_recaptcha_audio(driver)
    elif method == "random":
        return solve_image_captcha_simple(driver)
    else:
        # Manual solving
        print("\n[!] Vui long giai captcha thu cong!")
        input(">>> Nhan Enter sau khi hoan thanh...")
        return True
