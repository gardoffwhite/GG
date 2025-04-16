# selenium_updater.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def update_character_with_selenium(data):
    url_login = "http://nage-warzone.com/admin/index.php"
    url_edit = "http://nage-warzone.com/admin/charedit.php"

    driver = webdriver.Chrome()  # หรือใช้ headless ได้ถ้าต้องการ
    wait = WebDriverWait(driver, 10)

    try:
        # Login
        driver.get(url_login)
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("3770")
        driver.find_element(By.NAME, "submit").click()

        # ไปหน้าแก้ไข
        driver.get(url_edit)
        wait.until(EC.presence_of_element_located((By.NAME, "charname"))).send_keys(data["charname"])
        driver.find_element(By.NAME, "searchname").click()

        wait.until(EC.presence_of_element_located((By.NAME, "lv")))  # รอให้โหลดหน้าเสร็จก่อนกรอก

        # กรอกข้อมูลที่เหลือ
        for key, value in data.items():
            try:
                input_field = driver.find_element(By.NAME, key)
                input_field.clear()
                input_field.send_keys(value)
            except:
                pass  # ข้ามถ้าไม่มีฟิลด์นั้น

        # กดอัปเดต
        driver.find_element(By.NAME, "submit").click()

        return True
    except Exception as e:
        print(f"⚠️ Selenium Error: {e}")
        return False
    finally:
        driver.quit()
