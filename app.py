from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# สร้าง session สำหรับการเชื่อมต่อ
session = requests.Session()

# URL สำหรับ logout, login และหน้า charedit.php
logout_url = "http://nage-warzone.com/admin/?logout=session_id()"
login_url = "http://nage-warzone.com/admin/index.php"
charedit_url = "http://nage-warzone.com/admin/charedit.php"

# ข้อมูลฟอร์มล็อกอิน
login_payload = {
    "username": "admin",  # ชื่อผู้ใช้งาน
    "password": "3770",    # รหัสผ่าน
    "submit": "Submit"     # ค่าจากปุ่ม submit
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

timeout_time = 20

# ฟังก์ชันสำหรับดึงข้อมูลจากหน้าเว็บที่เป็น admin
def get_character_data_from_admin(character_name):
    # ขั้นตอนที่ 1: ออกจากระบบ (logout)
    try:
        logout_resp = session.get(logout_url, headers=headers, timeout=timeout_time)
        print("Logout response code:", logout_resp.status_code)
    except requests.exceptions.RequestException as e:
        print("⚠️ Error/Timeout ตอน logout:", e)

    # ขั้นตอนที่ 2: เข้าไปที่หน้า login เพื่อเตรียม session
    try:
        login_page_resp = session.get(login_url, headers=headers, timeout=timeout_time)
        print("Login page response code:", login_page_resp.status_code)
    except requests.exceptions.RequestException as e:
        print("เกิดข้อผิดพลาดตอนเข้าหน้า login:", e)
        return None

    # ขั้นตอนที่ 3: ส่งข้อมูลล็อกอิน
    try:
        login_resp = session.post(login_url, data=login_payload, headers=headers, timeout=timeout_time)
        print("Login response code:", login_resp.status_code)
    except requests.exceptions.RequestException as e:
        print("เกิดข้อผิดพลาดตอนส่งข้อมูลล็อกอิน:", e)
        return None

    # เช็คว่าล็อกอินสำเร็จหรือไม่
    if "Logout" not in login_resp.text:
        print("❌ Login Failed")
        return None

    # ขั้นตอนที่ 4: เข้าไปที่หน้า charedit.php หลังล็อกอิน
    try:
        charedit_page_resp = session.get(charedit_url, headers=headers, timeout=timeout_time)
        if charedit_page_resp.status_code != 200:
            print("❌ ไม่สามารถเข้าหน้า charedit.php ได้")
            return None
    except requests.exceptions.RequestException as e:
        print("เกิดข้อผิดพลาดตอนเข้าหน้า charedit.php:", e)
        return None

    # ขั้นตอนที่ 5: ค้นหาตัวละครจากฟอร์ม
    char_payload = {
        "charname": character_name,  # ใช้ชื่อจากฟอร์ม
        "searchname": "Submit"
    }

    try:
        char_resp = session.post(charedit_url, data=char_payload, headers=headers, timeout=timeout_time)
        print("Response code จากการส่งฟอร์มค้นหาตัวละคร:", char_resp.status_code)
    except requests.exceptions.RequestException as e:
        print("เกิดข้อผิดพลาดตอนส่งฟอร์มค้นหาตัวละคร:", e)
        return None

    # --- ดึงข้อมูลจาก placeholder และจัดเรียง ---
    soup_char = BeautifulSoup(char_resp.text, "html.parser")
    placeholders = soup_char.find_all('input', {'placeholder': True})

    # สร้าง dictionary สำหรับจัดเรียงข้อมูล
    data = {}

    # ดึง placeholder และจัดเก็บใน dictionary
    for placeholder in placeholders:
        field_name = placeholder.get('name')
        placeholder_value = placeholder.get('placeholder')
        data[field_name] = placeholder_value

    # จัดเรียงข้อมูลตามหัวข้อ
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

# หน้าแรกแสดงข้อมูล
@app.route('/', methods=['GET', 'POST'])
def index():
    character_data = None
    if request.method == 'POST':
        # รับชื่อจากฟอร์มค้นหา
        character_name = request.form['charname']
        character_data = get_character_data_from_admin(character_name)
        if not character_data:
            character_data = {"error": "ไม่สามารถดึงข้อมูลจากเซิร์ฟเวอร์ได้"}  # แสดงข้อความหากไม่สามารถดึงข้อมูล
    return render_template('index.html', character_data=character_data)

# เส้นทางสำหรับอัปเดตข้อมูลตัวละคร
@app.route('/update', methods=['POST'])
def update():
    # รับข้อมูลจากฟอร์ม
    character_name = request.form['charname']  # รับชื่อที่ค้นหา
    character_data = get_character_data_from_admin(character_name)  # ดึงข้อมูลจากการ scraping ใหม่
    if character_data:
        character_data['Character Name'] = request.form['charname']
        character_data['Level'] = request.form['level']
        character_data['EXP'] = request.form['exp']
        # คุณสามารถเพิ่มการอัปเดตข้อมูลอื่นๆ ได้ที่นี่

    # แสดงข้อมูลที่อัปเดตแล้ว
    return render_template('index.html', character_data=character_data)

if __name__ == '__main__':
    # ใช้พอร์ตจากตัวแปรสภาพแวดล้อม PORT หรือใช้พอร์ต 5000 ถ้าไม่มี
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
