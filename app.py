from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ข้อมูลตัวละครเริ่มต้น
character_data = {
    "Character Name": "GMTEST",
    "Level": "25",
    "EXP": "1500",
    "ecLv": "5",
    "ecEXP": "300",
    "STR": "50",
    "LvPoint": "10",
    "DEX": "45",
    "SkPoint": "20",
    "ESP": "15",
    "LIC": "3",
    "SPT": "8",
    "Money": "2000",
    "INT": "40",
    "Bank": "5000",
    "Map": "Forest",
    "Hero": "Mage",
    "X": "150",
    "Y": "200",
    "Z": "10"
}

# หน้าแรกแสดงข้อมูล
@app.route('/')
def index():
    return render_template('index.html', character_data=character_data)

# เส้นทางสำหรับอัปเดตข้อมูลตัวละคร
@app.route('/update', methods=['POST'])
def update():
    # รับข้อมูลจากฟอร์ม
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
