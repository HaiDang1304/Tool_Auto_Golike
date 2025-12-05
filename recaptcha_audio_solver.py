"""
reCAPTCHA Audio Solver - MIỄN PHÍ
Chuyển challenge hình ảnh sang audio và dùng Google Speech Recognition
"""

import time
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr
from pydub import AudioSegment


def solve_recaptcha_audio(driver):
    """
    Giải reCAPTCHA bằng audio challenge (MIỄN PHÍ)
    """
    try:
        print("\n[*] Đang thử giải bằng audio challenge...")
        
        # Tìm iframe challenge
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        challenge_iframe = None
        
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            if "recaptcha/api2/bframe" in src or "recaptcha challenge" in iframe.get_attribute("title").lower():
                challenge_iframe = iframe
                break
        
        if not challenge_iframe:
            print("[!] Không tìm thấy iframe challenge")
            return False
        
        # Chuyển vào iframe challenge
        driver.switch_to.frame(challenge_iframe)
        time.sleep(1)
        
        # Click nút audio (headphone icon)
        try:
            audio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
            )
            print("[*] Đã tìm thấy nút audio")
            audio_button.click()
            print("[*] Đã click nút audio")
            time.sleep(2)
        except:
            print("[!] Không tìm thấy nút audio (có thể bị block)")
            driver.switch_to.default_content()
            return False
        
        # Lấy URL file audio
        try:
            audio_source = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "audio-source"))
            )
            audio_url = audio_source.get_attribute("src")
            print(f"[*] Đã lấy URL audio: {audio_url[:50]}...")
        except:
            print("[!] Không tìm thấy audio source")
            driver.switch_to.default_content()
            return False
        
        # Tải file audio
        print("[*] Đang tải file audio...")
        response = requests.get(audio_url, timeout=30)
        
        # Lưu file MP3
        with open("recaptcha_audio.mp3", "wb") as f:
            f.write(response.content)
        print("[*] Đã tải xong audio")
        
        # Chuyển đổi MP3 sang WAV (cần cho speech recognition)
        try:
            audio = AudioSegment.from_mp3("recaptcha_audio.mp3")
            audio.export("recaptcha_audio.wav", format="wav")
            print("[*] Đã chuyển đổi sang WAV")
        except:
            # Nếu không có pydub, dùng trực tiếp MP3
            print("[*] Dùng trực tiếp file MP3")
            os.rename("recaptcha_audio.mp3", "recaptcha_audio.wav")
        
        # Nhận dạng giọng nói
        print("[*] Đang nhận dạng giọng nói...")
        recognizer = sr.Recognizer()
        
        with sr.AudioFile("recaptcha_audio.wav") as source:
            audio_data = recognizer.record(source)
            
            try:
                # Thử với Google Speech Recognition (MIỄN PHÍ)
                text = recognizer.recognize_google(audio_data, language="en-US")
                print(f"[*] Nhận dạng được: '{text}'")
            except sr.UnknownValueError:
                print("[!] Không nhận dạng được giọng nói")
                driver.switch_to.default_content()
                return False
            except sr.RequestError as e:
                print(f"[!] Lỗi API: {e}")
                driver.switch_to.default_content()
                return False
        
        # Nhập kết quả vào ô text
        try:
            response_input = driver.find_element(By.ID, "audio-response")
            response_input.clear()
            response_input.send_keys(text.lower())
            print("[*] Đã nhập kết quả")
            time.sleep(1)
        except:
            print("[!] Không tìm thấy ô nhập liệu")
            driver.switch_to.default_content()
            return False
        
        # Click nút Verify
        try:
            verify_button = driver.find_element(By.ID, "recaptcha-verify-button")
            verify_button.click()
            print("[*] Đã click Verify")
            time.sleep(3)
        except:
            print("[!] Không tìm thấy nút Verify")
            driver.switch_to.default_content()
            return False
        
        # Quay lại frame chính
        driver.switch_to.default_content()
        
        # Xóa file tạm
        try:
            os.remove("recaptcha_audio.mp3")
            os.remove("recaptcha_audio.wav")
        except:
            pass
        
        print("[OK] Đã giải audio challenge thành công!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Lỗi giải audio: {e}")
        driver.switch_to.default_content()
        return False


def solve_recaptcha_with_retry(driver, max_audio_attempts=3):
    """
    Giải reCAPTCHA với nhiều lần thử audio
    """
    print("\n[*] Bắt đầu giải reCAPTCHA...")
    
    # Thử audio challenge nhiều lần
    for attempt in range(max_audio_attempts):
        print(f"\n--- Lần thử {attempt + 1}/{max_audio_attempts} ---")
        
        if solve_recaptcha_audio(driver):
            print("[OK] Giải thành công!")
            return True
        
        if attempt < max_audio_attempts - 1:
            print("[*] Thử lại...")
            time.sleep(2)
    
    print("\n[!] Không thể giải bằng audio sau nhiều lần thử")
    return False
