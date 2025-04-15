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
        # ล็อกอิน
        session.get(login_url, headers=headers, timeout=timeout_time)
        login_resp = session.post(login_url, data=login_payload, headers=headers, timeout=timeout_time)
        
        if "Logout" in login_resp.text:
            # เชื่อมต่อไปยังหน้าจัดการตัวละคร
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
        if character_name:  # ตรวจสอบว่ามีการกรอกชื่อหรือไม่
            character_data = get_character_data_from_admin(character_name)
            if not character_data:
                character_data = {"error": "❌ ไม่สามารถดึงข้อมูลตัวละครได้"}
        else:
            character_data = {"error": "❌ กรุณากรอกชื่อของตัวละคร"}

    return render_template('index.html', character_data=character_data, status_message=status_message)

@app.route('/update', methods=['POST'])
def update():
    character_name = request.form['charname']
    level = request.form.get('level')
    exp = request.form.get('exp')

    if not character_name:
        return render_template('index.html', status_message="❌ กรุณากรอกชื่อของตัวละคร")

    # ดึงข้อมูลเดิมจากระบบแอดมิน
    character_data = get_character_data_from_admin(character_name)
    if character_data:
        # อัปเดตข้อมูลที่ได้รับจากฟอร์ม
        if level:
            character_data['Level'] = level
        if exp:
            character_data['EXP'] = exp

        # ส่งข้อมูลไปยังระบบแอดมินเพื่ออัปเดต
        update_payload = {
            "charname": character_name,
            "level": character_data['Level'],
            "exp": character_data['EXP'],
            "eclv": character_data['ecLv'],
            "ecexp": character_data['ecEXP'],
            "str": character_data['STR'],
            "lvpoint": character_data['LvPoint'],
            "dex": character_data['DEX'],
            "skpoint": character_data['SkPoint'],
            "esp": character_data['ESP'],
            "lic": character_data['LIC'],
            "spt": character_data['SPT'],
            "money": character_data['Money'],
            "int": character_data['INT'],
            "bankmoney": character_data['Bank'],
            "cmap": character_data['Map'],
            "hero": character_data['Hero'],
            "x": character_data['X'],
            "y": character_data['Y'],
            "z": character_data['Z']
        }

        # ส่งคำขอ POST ไปยังหน้า charedit.php สำหรับอัปเดตข้อมูล
        try:
            update_resp = session.post(charedit_url, data=update_payload, headers=headers, timeout=timeout_time)
            if update_resp.status_code == 200:
                # ดึงข้อมูลหลังจากอัปเดต
                updated_data = get_character_data_from_admin(character_name)
                if updated_data:
                    # ตรวจสอบว่าข้อมูลที่อัปเดตตรงกับข้อมูลที่ส่งไป
                    if updated_data['Level'] == level and updated_data['EXP'] == exp:
                        status_message = "✅ อัปเดตข้อมูลสำเร็จ"
                    else:
                        status_message = "❌ อัปเดตข้อมูลไม่สำเร็จ"
                else:
                    status_message = "❌ ไม่สามารถดึงข้อมูลหลังอัปเดต"
            else:
                status_message = "❌ ไม่สามารถอัปเดตข้อมูลได้"
        except Exception as e:
            status_message = f"⚠️ เกิดข้อผิดพลาดในการอัปเดตข้อมูล: {e}"

        return render_template('index.html', character_data=updated_data, status_message=status_message)
    else:
        return render_template('index.html', status_message="❌ ไม่สามารถดึงข้อมูลตัวละครได้")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
