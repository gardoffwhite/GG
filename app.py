from flask import Flask, render_template, request
import os
import time
import requests
from bs4 import BeautifulSoup

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
searched_names = set()  # เก็บรายชื่อที่เคยค้นหาแล้ว

def get_character_data_from_admin(character_name):
    if character_name in searched_names:
        print("❌ ชื่อนี้ถูกค้นหาไปแล้ว:", character_name)
        return {"error": "ชื่อตัวละครนี้ถูกใช้งานแล้ว กรุณากรอกชื่อใหม่"}

    searched_names.add(character_name)

    try:
        print("➡️ กำลัง Logout...")
        session.get(logout_url, headers=headers, timeout=timeout_time)
        time.sleep(1)

        print("➡️ เข้าหน้า Login...")
        session.get(login_url, headers=headers, timeout=timeout_time)
        time.sleep(1)

        print("➡️ กำลัง Login...")
        login_resp = session.post(login_url, data=login_payload, headers=headers, timeout=timeout_time)
        if "Logout" not in login_resp.text:
            return {"error": "❌ Login ไม่สำเร็จ"}
        time.sleep(1)

        print("➡️ เข้าหน้า charedit.php...")
        session.get(charedit_url, headers=headers, timeout=timeout_time)
        time.sleep(1)

        print("➡️ ส่งชื่อค้นหา:", character_name)
        char_payload = {
            "charname": character_name,
            "searchname": "Submit"
        }
        char_resp = session.post(charedit_url, data=char_payload, headers=headers, timeout=timeout_time)
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
        # จำลองการอัปเดต — สามารถเพิ่มระบบส่งกลับไปยังหน้าแก้ไขจริงได้
        character_data['Level'] = request.form.get('level', character_data['Level'])
        character_data['EXP'] = request.form.get('exp', character_data['EXP'])

    return render_template('index.html', character_data=character_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
