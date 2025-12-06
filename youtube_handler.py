"""
YOUTUBE JOB HANDLER
Xử lý nhiệm vụ Youtube tự động: Subscribe, Like, Comment, Share
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random


def wait_for_youtube_load(driver, timeout=15):
    """Đợi YouTube load xong"""
    try:
        # Đợi player xuất hiện
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        time.sleep(2)
        return True
    except:
        # Nếu không có player (channel page), đợi page load
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


def handle_youtube_subscribe(driver):
    """
    Xử lý nhiệm vụ Subscribe kênh YouTube
    """
    try:
        print("  [YOUTUBE] Đang tìm nút Subscribe...")
        
        # Đợi trang load
        wait_for_youtube_load(driver)
        
        # Scroll lên top để thấy nút Subscribe
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Các selector cho nút Subscribe
        subscribe_selectors = [
            # Button Subscribe chính
            "//button[@aria-label[contains(., 'Subscribe')]]",
            "//button[contains(@aria-label, 'Subscribe to')]",
            
            # Button có text Subscribe
            "//yt-button-shape//button[contains(., 'Subscribe')]",
            "//button[contains(., 'Subscribe') and not(contains(., 'Subscribed'))]",
            
            # Button Subscribe (tiếng Việt)
            "//button[contains(., 'Đăng ký') and not(contains(., 'Đã đăng ký'))]",
            
            # Subscribe button trong channel header
            "//ytd-subscribe-button-renderer//button",
            "//ytd-button-renderer//button[contains(@aria-label, 'Subscribe')]",
        ]
        
        subscribe_btn = None
        
        for selector in subscribe_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for btn in buttons:
                    if btn.is_displayed():
                        text = btn.text.upper()
                        aria_label = btn.get_attribute("aria-label") or ""
                        
                        # Không click nếu đã subscribe
                        if "SUBSCRIBED" not in text and "ĐÃ ĐĂNG KÝ" not in text.upper():
                            if "SUBSCRIBE" in text or "ĐĂNG KÝ" in text or "Subscribe" in aria_label:
                                subscribe_btn = btn
                                print(f"  [DEBUG] Tìm thấy nút: {btn.text or aria_label}")
                                break
                
                if subscribe_btn:
                    break
            except Exception as e:
                continue
        
        if not subscribe_btn:
            print("  [!] Không tìm thấy nút Subscribe (có thể đã subscribe)")
            return False
        
        # Scroll đến nút
        scroll_to_element(driver, subscribe_btn)
        
        # Click Subscribe
        try:
            subscribe_btn.click()
        except:
            driver.execute_script("arguments[0].click();", subscribe_btn)
        
        print("  [OK] Đã click Subscribe!")
        time.sleep(random.uniform(2, 3))
        
        # Xử lý popup xác nhận (nếu có)
        try:
            confirm_btns = driver.find_elements(By.XPATH, 
                "//button[contains(., 'Subscribe') or contains(., 'Đăng ký')]")
            if confirm_btns:
                for btn in confirm_btns:
                    if btn.is_displayed():
                        btn.click()
                        print("  [OK] Đã xác nhận Subscribe!")
                        break
        except:
            pass
        
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi subscribe YouTube: {e}")
        return False


def handle_youtube_like(driver):
    """
    Xử lý nhiệm vụ Like video YouTube
    """
    try:
        print("  [YOUTUBE] Đang tìm nút Like...")
        
        wait_for_youtube_load(driver)
        
        # Scroll xuống để thấy like button
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
        
        # Các selector cho nút Like
        like_selectors = [
            # Like button chính (YouTube mới)
            "//yt-button-shape[@id='top-level-buttons-computed']//button[@aria-label[contains(., 'like')]]",
            "//button[@aria-label[contains(., 'like this video')]]",
            
            # Like button (cấu trúc cũ)
            "//button[contains(@aria-label, 'Like')]",
            "//button[@title='I like this' or @title='Like this video']",
            
            # Like button tiếng Việt
            "//button[contains(@aria-label, 'Thích') or contains(@title, 'Thích')]",
            
            # Segmented like button
            "//ytd-toggle-button-renderer[@id='like-button']//button",
            "//yt-icon-button[@id='button-shape']//button[contains(@aria-label, 'like')]",
        ]
        
        like_btn = None
        
        for selector in like_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for btn in buttons:
                    if btn.is_displayed():
                        aria_pressed = btn.get_attribute("aria-pressed")
                        # Chỉ click nếu chưa like
                        if aria_pressed == "false" or not aria_pressed:
                            like_btn = btn
                            aria_label = btn.get_attribute("aria-label") or btn.get_attribute("title") or "Like"
                            print(f"  [DEBUG] Tìm thấy nút: {aria_label}")
                            break
                
                if like_btn:
                    break
            except:
                continue
        
        if not like_btn:
            print("  [!] Không tìm thấy nút Like (có thể đã like)")
            return False
        
        # Scroll đến nút
        scroll_to_element(driver, like_btn)
        
        # Click Like
        try:
            like_btn.click()
        except:
            driver.execute_script("arguments[0].click();", like_btn)
        
        print("  [OK] Đã like video!")
        time.sleep(random.uniform(1.5, 2.5))
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi like YouTube: {e}")
        return False


def handle_youtube_comment(driver, comment_text="Great video! 👍"):
    """
    Xử lý nhiệm vụ Comment YouTube
    """
    try:
        print("  [YOUTUBE] Đang tìm ô comment...")
        
        wait_for_youtube_load(driver)
        
        # Scroll xuống phần comment
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.5)
        
        time.sleep(2)
        
        # Tìm ô comment
        comment_box_selectors = [
            # Comment box chính
            "//ytd-comment-simplebox-renderer//div[@id='placeholder-area']",
            "//div[@id='simple-box']//div[@id='placeholder-area']",
            
            # Contenteditable
            "//div[@id='contenteditable-root'][@contenteditable='true']",
            "//ytd-commentbox//div[@contenteditable='true']",
        ]
        
        comment_box = None
        
        for selector in comment_box_selectors:
            try:
                boxes = driver.find_elements(By.XPATH, selector)
                if boxes and boxes[0].is_displayed():
                    comment_box = boxes[0]
                    break
            except:
                continue
        
        if not comment_box:
            print("  [!] Không tìm thấy ô comment")
            return False
        
        # Click vào ô comment để focus
        scroll_to_element(driver, comment_box)
        comment_box.click()
        time.sleep(1)
        
        # Tìm textarea thực sự để nhập
        try:
            textarea = driver.find_element(By.XPATH, 
                "//ytd-commentbox//div[@id='contenteditable-root'][@contenteditable='true']")
            
            if textarea:
                # Nhập comment
                textarea.click()
                time.sleep(0.5)
                textarea.send_keys(comment_text)
                time.sleep(1)
                
                print(f"  [OK] Đã nhập comment: {comment_text}")
                
                # Tìm nút Comment/Bình luận
                submit_selectors = [
                    "//ytd-commentbox//button[@aria-label='Comment' or @aria-label='Bình luận']",
                    "//ytd-commentbox//button[contains(., 'Comment')]",
                    "//ytd-commentbox//button[@id='submit-button']",
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btns = driver.find_elements(By.XPATH, selector)
                        if submit_btns and submit_btns[0].is_displayed():
                            time.sleep(1)
                            submit_btns[0].click()
                            print("  [OK] Đã gửi comment!")
                            time.sleep(2)
                            return True
                    except:
                        continue
                
                print("  [!] Không tìm thấy nút Comment")
                return False
        
        except Exception as e:
            print(f"  [!] Lỗi nhập comment: {e}")
            return False
        
    except Exception as e:
        print(f"  [ERROR] Lỗi comment YouTube: {e}")
        return False


def handle_youtube_share(driver):
    """
    Xử lý nhiệm vụ Share video YouTube
    """
    try:
        print("  [YOUTUBE] Đang tìm nút Share...")
        
        wait_for_youtube_load(driver)
        
        # Scroll xuống một chút
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
        
        # Tìm nút Share
        share_selectors = [
            # Share button chính
            "//button[@aria-label='Share']",
            "//button[@aria-label='Chia sẻ']",
            "//button[contains(@aria-label, 'Share')]",
            
            # Share button trong action buttons
            "//ytd-menu-renderer//button[contains(@aria-label, 'Share')]",
            "//yt-button-shape//button[contains(@aria-label, 'Share')]",
        ]
        
        share_btn = None
        
        for selector in share_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                if buttons and buttons[0].is_displayed():
                    share_btn = buttons[0]
                    break
            except:
                continue
        
        if not share_btn:
            print("  [!] Không tìm thấy nút Share")
            return False
        
        # Click Share
        scroll_to_element(driver, share_btn)
        try:
            share_btn.click()
        except:
            driver.execute_script("arguments[0].click();", share_btn)
        
        time.sleep(1.5)
        
        # Tìm nút Copy (trong popup)
        copy_selectors = [
            "//button[contains(@aria-label, 'Copy')]",
            "//button[contains(., 'Copy')]",
            "//button[contains(., 'Sao chép')]",
            "//yt-button-renderer[contains(., 'Copy')]//button",
        ]
        
        for selector in copy_selectors:
            try:
                copy_btns = driver.find_elements(By.XPATH, selector)
                if copy_btns and copy_btns[0].is_displayed():
                    copy_btns[0].click()
                    print("  [OK] Đã share (copy link)!")
                    time.sleep(1)
                    
                    # Đóng popup (ESC)
                    try:
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                    except:
                        pass
                    
                    return True
            except:
                continue
        
        print("  [!] Không tìm thấy Copy, nhưng đã click Share")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Lỗi share YouTube: {e}")
        return False


def auto_youtube_job(driver, job_type="subscribe"):
    """
    Hàm chính xử lý nhiệm vụ YouTube
    
    Args:
        driver: Selenium WebDriver
        job_type: Loại nhiệm vụ (subscribe, like, comment, share)
    
    Returns:
        True nếu thành công, False nếu thất bại
    """
    
    print(f"\n  [YOUTUBE] Bắt đầu nhiệm vụ: {job_type.upper()}")
    
    try:
        # Đợi YouTube load
        time.sleep(3)
        
        # Thực hiện nhiệm vụ theo loại
        if job_type == "subscribe":
            return handle_youtube_subscribe(driver)
        
        elif job_type == "like":
            return handle_youtube_like(driver)
        
        elif job_type == "comment":
            # Comment ngẫu nhiên
            comments = [
                "Great video! 👍",
                "Amazing content! ❤️",
                "Very helpful, thanks! 🙏",
                "Love this! 😍",
                "Awesome! 🔥",
                "Keep it up! 💪",
            ]
            comment = random.choice(comments)
            return handle_youtube_comment(driver, comment)
        
        elif job_type == "share":
            return handle_youtube_share(driver)
        
        else:
            print(f"  [!] Loại job không hỗ trợ: {job_type}")
            return False
    
    except Exception as e:
        print(f"  [ERROR] Lỗi xử lý YouTube job: {e}")
        return False
