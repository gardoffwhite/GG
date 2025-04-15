from flask import Flask, render_template, request
import os
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

timeout_time = 20

# สถานะการเชื่อมต่อระบบแอดมิน
connected_to_admin = False

def connect_to_admin():
    global connected_to_admin
    try:
        session.get(login_url, headers=headers, timeout=timeout_time)
        login_resp = session.post(login_url, data=login_payload, headers=headers, timeout=timeout_time)
        if "Logout" in login_resp.text:
            charedit_page = session.get(charedit_url, headers=headers, timeout=timeout_time)
            if charedit_page.status_code == 200:
                connected_to_admin = True
                print("✅ เชื่อมต่อ charedit.php สำเร็จแล้ว")
                return True
        print("❌ ล็อกอินไม่สำเร็จ")
    except Exception as e:
        print("⚠️ เกิดข้อผิดพลาดตอนเชื่อมต่อ:", e)
    return False

def get_character_data_from_admin(character_name):
    if not connected_to_admin:
        print("❌ ยังไม่ได้เชื่อมต่อระบบแอดมิน")
        return None

    char_payload = {
        "charname": character_name,
        "searchname": "Submit"
    }

    try:
        char_resp = session.post(charedit_url, data=char_payload, headers=headers, timeout=timeout_time)
        soup_char = BeautifulSoup(char_resp.text, "html.parser")
        placeholders = soup_char.find_all('input', {'placeholder': True})

        data = {}
        for placeholder in placeholders:
            field_name = placeholder.get('name')
            placeholder_value = placeholder.get('placeholder')
            data[field_name] = placeholder_value

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
    except Exception as e:
        print("⚠️ Error: ไม่สามารถค้นหาตัวละคร:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global connected_to_admin
    character_data = None
    status_message = ""

    if not connected_to_admin:
        if connect_to_admin():
            status_message = "✅ เชื่อมต่อระบบแอดมินแล้ว"
        else:
            status_message = "❌ เชื่อมต่อระบบแอดมินไม่สำเร็จ"

    if request.method == 'POST':
        character_name = request.form['charname']
        character_data = get_character_data_from_admin(character_name)
        if not character_data:
            character_data = {"error": "❌ ไม่สามารถดึงข้อมูลตัวละครได้"}

    return render_template('index.html', character_data=character_data, status_message=status_message)

@app.route('/update', methods=['POST'])
def update():
    character_name = request.form['charname']
    character_data = get_character_data_from_admin(character_name)
    if character_data:
        character_data['Character Name'] = request.form['charname']
        character_data['Level'] = request.form['level']
        character_data['EXP'] = request.form['exp']
        # เพิ่ม update field อื่นๆ ได้

    return render_template('index.html', character_data=character_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
