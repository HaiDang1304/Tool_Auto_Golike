"""
TIKTOK JOB HANDLER
Xử lý nhiệm vụ TikTok tự động: Follow, Like, Comment, Share
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random


def wait_for_page_load(driver, timeout=10):
    """Đợi trang TikTok load xong"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)
        return True
    except:
        return False


def scroll_to_element(driver, element):
    """Scroll đến element"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(random.uniform(0.5, 1.0))
    except:
        pass


def handle_tiktok_follow(driver):
    """
    Xử lý nhiệm vụ Follow TikTok
    Tìm và click nút Follow/Theo dõi
    """
    try:
        print("  [TIKTOK] Đang tìm nút Follow...")
        
        # Đợi trang load
        wait_for_page_load(driver)
        
        # Cách 1: Tìm nút Follow chính (profile page)
        follow_selectors = [
            # Button có text "Follow"
            "//button[contains(@data-e2e, 'follow-button')]",
            "//button[contains(text(), 'Follow') and not(contains(text(), 'Following'))]",
            "//button[contains(., 'Theo dõi') and not(contains(., 'Đang theo dõi'))]",
            
            # Button có class follow
            "//button[contains(@class, 'follow-button')]",
            "//button[contains(@class, 'tiktok-') and contains(., 'Follow')]",
            
            # Div button role
            "//div[@role='button' and contains(., 'Follow')]",
        ]
        
        follow_btn = None
        
        for selector in follow_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                # Lọc button visible và chưa follow
                for btn in buttons:
                    if btn.is_displayed():
                        text = btn.text.lower()
                        # Không click nếu đã follow
                        if "following" not in text and "đang theo dõi" not in text:
                            follow_btn = btn
                            print(f"  [DEBUG] Tìm thấy nút: {btn.text}")
                            break
                
                if follow_btn:
                    break
            except:
                continue
        
        if not follow_btn:
            print("  [!] Không tìm thấy nút Follow")
            return False
        
        # Scroll đến nút
        scroll_to_element(driver, follow_btn)
        
        # Click
        try:
            follow_btn.click()
        except:
            driver.execute_script("arguments[0].click();", follow_btn)
        
        print("  [OK] Đã click Follow!")
        time.sleep(random.uniform(2, 3))
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi follow TikTok: {e}")
        return False


def handle_tiktok_like(driver):
    """
    Xử lý nhiệm vụ Like video TikTok
    """
    try:
        print("  [TIKTOK] Đang tìm nút Like...")
        
        wait_for_page_load(driver)
        
        # Cách 1: Tìm nút like (icon trái tim)
        like_selectors = [
            # Button có data-e2e like
            "//button[contains(@data-e2e, 'like-button')]",
            "//button[contains(@data-e2e, 'browse-like')]",
            
            # Button có aria-label like
            "//button[contains(@aria-label, 'like')]",
            "//button[contains(@aria-label, 'Like')]",
            
            # Icon trái tim SVG
            "//*[name()='svg' and contains(@fill, 'currentColor')]/ancestor::button[contains(@aria-label, 'like')]",
            
            # Button chứa icon heart
            "//button[.//*[contains(@class, 'heart')]]",
        ]
        
        like_btn = None
        
        for selector in like_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for btn in buttons:
                    if btn.is_displayed():
                        # Kiểm tra xem đã like chưa
                        aria_pressed = btn.get_attribute("aria-pressed")
                        if aria_pressed == "false" or not aria_pressed:
                            like_btn = btn
                            break
                
                if like_btn:
                    break
            except:
                continue
        
        if not like_btn:
            print("  [!] Không tìm thấy nút Like")
            return False
        
        # Scroll đến nút
        scroll_to_element(driver, like_btn)
        
        # Click
        try:
            like_btn.click()
        except:
            driver.execute_script("arguments[0].click();", like_btn)
        
        print("  [OK] Đã like video!")
        time.sleep(random.uniform(1.5, 2.5))
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi like TikTok: {e}")
        return False


def handle_tiktok_comment(driver, comment_text="Nice video! 👍"):
    """
    Xử lý nhiệm vụ Comment TikTok
    """
    try:
        print("  [TIKTOK] Đang tìm ô comment...")
        
        wait_for_page_load(driver)
        
        # Tìm nút comment
        comment_btn_selectors = [
            "//button[contains(@data-e2e, 'comment-button')]",
            "//button[contains(@aria-label, 'comment')]",
            "//button[contains(@aria-label, 'Comment')]",
        ]
        
        comment_btn = None
        for selector in comment_btn_selectors:
            try:
                btns = driver.find_elements(By.XPATH, selector)
                if btns and btns[0].is_displayed():
                    comment_btn = btns[0]
                    break
            except:
                continue
        
        if comment_btn:
            # Click để mở ô comment
            scroll_to_element(driver, comment_btn)
            try:
                comment_btn.click()
            except:
                driver.execute_script("arguments[0].click();", comment_btn)
            
            time.sleep(2)
        
        # Tìm ô nhập comment
        comment_input_selectors = [
            "//div[@contenteditable='true' and contains(@data-e2e, 'comment')]",
            "//div[@contenteditable='true']",
            "//textarea[@placeholder]",
        ]
        
        comment_input = None
        for selector in comment_input_selectors:
            try:
                inputs = driver.find_elements(By.XPATH, selector)
                if inputs and inputs[0].is_displayed():
                    comment_input = inputs[0]
                    break
            except:
                continue
        
        if not comment_input:
            print("  [!] Không tìm thấy ô comment")
            return False
        
        # Nhập comment
        comment_input.click()
        time.sleep(0.5)
        comment_input.send_keys(comment_text)
        time.sleep(1)
        
        # Tìm nút Post/Đăng
        post_btn_selectors = [
            "//button[contains(text(), 'Post')]",
            "//button[contains(text(), 'Đăng')]",
            "//button[@type='submit']",
        ]
        
        post_btn = None
        for selector in post_btn_selectors:
            try:
                btns = driver.find_elements(By.XPATH, selector)
                if btns and btns[0].is_displayed():
                    post_btn = btns[0]
                    break
            except:
                continue
        
        if post_btn:
            post_btn.click()
            print(f"  [OK] Đã comment: {comment_text}")
            time.sleep(2)
            return True
        else:
            print("  [!] Không tìm thấy nút Post")
            return False
        
    except Exception as e:
        print(f"  [ERROR] Lỗi comment TikTok: {e}")
        return False


def handle_tiktok_share(driver):
    """
    Xử lý nhiệm vụ Share TikTok
    """
    try:
        print("  [TIKTOK] Đang tìm nút Share...")
        
        wait_for_page_load(driver)
        
        # Tìm nút share
        share_selectors = [
            "//button[contains(@data-e2e, 'share-button')]",
            "//button[contains(@aria-label, 'share')]",
            "//button[contains(@aria-label, 'Share')]",
        ]
        
        share_btn = None
        for selector in share_selectors:
            try:
                btns = driver.find_elements(By.XPATH, selector)
                if btns and btns[0].is_displayed():
                    share_btn = btns[0]
                    break
            except:
                continue
        
        if not share_btn:
            print("  [!] Không tìm thấy nút Share")
            return False
        
        # Click share
        scroll_to_element(driver, share_btn)
        try:
            share_btn.click()
        except:
            driver.execute_script("arguments[0].click();", share_btn)
        
        time.sleep(1)
        
        # Tìm và click "Copy link"
        copy_link_selectors = [
            "//button[contains(., 'Copy link')]",
            "//button[contains(., 'Sao chép liên kết')]",
            "//div[contains(., 'Copy link')]",
        ]
        
        for selector in copy_link_selectors:
            try:
                btns = driver.find_elements(By.XPATH, selector)
                if btns and btns[0].is_displayed():
                    btns[0].click()
                    print("  [OK] Đã share (copy link)!")
                    time.sleep(1)
                    return True
            except:
                continue
        
        print("  [!] Không tìm thấy Copy link, nhưng đã click Share")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi share TikTok: {e}")
        return False


def auto_tiktok_job(driver, job_type="follow"):
    """
    Hàm chính xử lý nhiệm vụ TikTok
    
    Args:
        driver: Selenium WebDriver
        job_type: Loại nhiệm vụ (follow, like, comment, share)
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    
    print(f"\n  [TIKTOK] Bắt đầu nhiệm vụ: {job_type.upper()}")
    
    try:
        # Đợi trang TikTok load
        time.sleep(3)
        
        # Thực hiện nhiệm vụ theo loại
        if job_type == "follow":
            return handle_tiktok_follow(driver)
        
        elif job_type == "like":
            return handle_tiktok_like(driver)
        
        elif job_type == "comment":
            # Comment ngẫu nhiên
            comments = [
                "Nice video! 👍",
                "Amazing! ❤️",
                "Great content! 🔥",
                "Love it! 😍",
                "So cool! ✨",
            ]
            comment = random.choice(comments)
            return handle_tiktok_comment(driver, comment)
        
        elif job_type == "share":
            return handle_tiktok_share(driver)
        
        else:
            print(f"  [!] Loại job không hỗ trợ: {job_type}")
            return False
    
    except Exception as e:
        print(f"  [ERROR] Lỗi xử lý TikTok job: {e}")
        return False
