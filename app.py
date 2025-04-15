from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ฟังก์ชันสำหรับดึงข้อมูลจากหน้าเว็บที่เป็น admin
def get_character_data_from_admin():
    url = 'http://your-game-admin-url/charedit.php'  # URL ของหน้า admin
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # ส่งคำขอ GET เพื่อดึง HTML
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None  # ตรวจสอบว่าเชื่อมต่อสำเร็จ

    # ใช้ BeautifulSoup เพื่อแยกข้อมูล
    soup = BeautifulSoup(response.text, 'html.parser')

    # ดึงข้อมูลตัวละครจาก input หรือ element ที่ต้องการ
    # ในที่นี้จะสมมุติว่าเราดึงค่าจาก placeholder หรือ input field
    character_data = {
        "Character Name": soup.find('input', {'placeholder': 'Character Name'}).get('value', ''),
        "Level": soup.find('input', {'placeholder': 'Level'}).get('value', ''),
        "EXP": soup.find('input', {'placeholder': 'EXP'}).get('value', ''),
        "ecLv": soup.find('input', {'placeholder': 'ecLv'}).get('value', ''),
        "ecEXP": soup.find('input', {'placeholder': 'ecEXP'}).get('value', ''),
        "STR": soup.find('input', {'placeholder': 'STR'}).get('value', ''),
        "LvPoint": soup.find('input', {'placeholder': 'LvPoint'}).get('value', ''),
        "DEX": soup.find('input', {'placeholder': 'DEX'}).get('value', ''),
        "SkPoint": soup.find('input', {'placeholder': 'SkPoint'}).get('value', ''),
        "ESP": soup.find('input', {'placeholder': 'ESP'}).get('value', ''),
        "LIC": soup.find('input', {'placeholder': 'LIC'}).get('value', ''),
        "SPT": soup.find('input', {'placeholder': 'SPT'}).get('value', ''),
        "Money": soup.find('input', {'placeholder': 'Money'}).get('value', ''),
        "INT": soup.find('input', {'placeholder': 'INT'}).get('value', ''),
        "Bank": soup.find('input', {'placeholder': 'Bank'}).get('value', ''),
        "Map": soup.find('input', {'placeholder': 'Map'}).get('value', ''),
        "Hero": soup.find('input', {'placeholder': 'Hero'}).get('value', ''),
        "X": soup.find('input', {'placeholder': 'X'}).get('value', ''),
        "Y": soup.find('input', {'placeholder': 'Y'}).get('value', ''),
        "Z": soup.find('input', {'placeholder': 'Z'}).get('value', '')
    }
    return character_data

# หน้าแรกแสดงข้อมูล
@app.route('/')
def index():
    # ดึงข้อมูลจาก admin ผ่านการ web scraping
    character_data = get_character_data_from_admin()
    if not character_data:
        character_data = {"error": "ไม่สามารถดึงข้อมูลจากเซิร์ฟเวอร์ได้"}  # แสดงข้อความหากไม่สามารถดึงข้อมูล
    return render_template('index.html', character_data=character_data)

# เส้นทางสำหรับอัปเดตข้อมูลตัวละคร
@app.route('/update', methods=['POST'])
def update():
    # รับข้อมูลจากฟอร์ม
    character_data = get_character_data_from_admin()  # ดึงข้อมูลจากการ scraping ใหม่
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
