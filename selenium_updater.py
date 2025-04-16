from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# สำหรับ headless mode (ไม่เปิดหน้าต่าง browser จริง)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

admin_url = "http://nage-warzone.com/admin/index.php"
charedit_url = "http://nage-warzone.com/admin/charedit.php"

def update_character_with_selenium(data):
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(admin_url)

        # Login
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("3770")
        driver.find_element(By.NAME, "submit").click()

        time.sleep(1)  # รอโหลดหน้า

        # ไปหน้า charedit
        driver.get(charedit_url)

        # ค้นหาชื่อตัวละคร
        driver.find_element(By.NAME, "charname").send_keys(data['charname'])
        driver.find_element(By.NAME, "searchname").click()

        time.sleep(1)  # รอโหลดข้อมูลตัวละคร

        # กรอกข้อมูลแต่ละช่อง (เฉพาะที่ส่งมา)
        for key in data:
            if key == "charname":
                continue
            try:
                input_box = driver.find_element(By.NAME, key)
                if data[key]:
                    input_box.clear()
                    input_box.send_keys(str(data[key]))
            except Exception as e:
                print(f"⚠️ ไม่เจอฟิลด์: {key} ({e})")

        # กดปุ่ม Submit เพื่ออัปเดต
        driver.find_element(By.NAME, "update").click()

        time.sleep(1)

        print("✅ อัปเดตสำเร็จ")
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False
    finally:
        driver.quit()
