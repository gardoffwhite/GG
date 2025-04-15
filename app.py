from flask import Flask, render_template, request
import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Lock  # 🔒 ใช้สำหรับล็อก

app = Flask(__name__)

session = requests.Session()

logout_url = "http://nage-warzone.com/admin/?logout=session_id()"
login_url = "http://nage-warzone.com/admin/index.php"
charedit_url = "http://nage-warzone.com/admin/charedit.php"

login_payload = {
    "username": "admin",
    "password": "3770",
    "submit": "Submit"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

timeout_time = 20

# 🔒 เพิ่มตัวแปรล็อก
processing_lock = Lock()

def get_character_data_from_admin(character_name):
    # ❗ ตรวจสอบว่าอีกคำขอหนึ่งกำลังทำงานอยู่ไหม
    if not processing_lock.acquire(blocking=False):
        return {"error": "⚠️ ระบบกำลังประมวลผลคำขอก่อนหน้า กรุณารอสักครู่แล้วลองใหม่อีกครั้ง"}

    try:
        print("➡️ กำลัง Logout...")
        logout_resp = session.get(logout_url, headers=headers, timeout=timeout_time)
        print("Logout Response:", logout_resp.text)  # Debug
        time.sleep(1)

        print("➡️ เข้าหน้า Login...")
        login_resp = session.get(login_url, headers=headers, timeout=timeout_time)
        print("Login Response:", login_resp.text)  # Debug
        time.sleep(1)

        print("➡️ กำลังกด Login...")
        login_resp = session.post(login_url, data=login_payload, headers=headers, timeout=timeout_time)
        print("Login POST Response:", login_resp.text)  # Debug
        if "Logout" not in login_resp.text:
            return {"error": "❌ Login ไม่สำเร็จ"}
        time.sleep(1)

        print("➡️ เข้าหน้า charedit.php...")
        charedit_resp = session.get(charedit_url, headers=headers, timeout=timeout_time)
        print("charedit.php Response:", charedit_resp.text)  # Debug
        time.sleep(1)

        print("➡️ ส่งชื่อค้นหา:", character_name)
        char_payload = {
            "charname": character_name,
            "searchname": "Submit"
        }
        char_resp = session.post(charedit_url, data=char_payload, headers=headers, timeout=timeout_time)
        print("Character Search Response:", char_resp.text)  # Debug
        time.sleep(1)

        soup_char = BeautifulSoup(char_resp.text, "html.parser")
        placeholders = soup_char.find_all('input', {'placeholder': True})

        data = {}
        for placeholder in placeholders:
            field_name = placeholder.get('name')
            value = placeholder.get('value', '')
            data[field_name] = value

        sorted_data = {
            "Character Name": data.get("charname", ""),
            "Level": data.get("lv", ""),
            "EXP": data.get("exp", ""),
            "ecLv": data.get("eclv", ""),
            "ecEXP": data.get("ecexp", ""),
            "STR": data.get("str", ""),
            "LvPoint": data.get("lvpoint", ""),
            "DEX": data.get("dex", ""),
            "SkPoint": data.get("skpoint", ""),
            "ESP": data.get("esp", ""),
            "LIC": data.get("lic", ""),
            "SPT": data.get("spt", ""),
            "Money": data.get("money", ""),
            "INT": data.get("int", ""),
            "Bank": data.get("bankmoney", ""),
            "Map": data.get("cmap", ""),
            "Hero": data.get("hero", ""),
            "X": data.get("x", ""),
            "Y": data.get("y", ""),
            "Z": data.get("z", "")
        }

        return sorted_data

    except requests.exceptions.RequestException as e:
        return {"error": f"⚠️ เกิดข้อผิดพลาด: {e}"}

    finally:
        processing_lock.release()  # ✅ ปลดล็อกเมื่อเสร็จไม่ว่าจะสำเร็จหรือผิดพลาด

@app.route('/', methods=['GET', 'POST'])
def index():
    character_data = None
    if request.method == 'POST':
        character_name = request.form['charname']
        character_data = get_character_data_from_admin(character_name)
    return render_template('index.html', character_data=character_data)

@app.route('/update', methods=['POST'])
def update():
    character_name = request.form['charname']
    character_data = get_character_data_from_admin(character_name)

    if character_data and 'error' not in character_data:
        character_data['Level'] = request.form.get('level', character_data['Level'])
        character_data['EXP'] = request.form.get('exp', character_data['EXP'])

    return render_template('index.html', character_data=character_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
