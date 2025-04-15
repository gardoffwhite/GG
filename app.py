<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>แก้ไขข้อมูลตัวละคร</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        h2 {
            text-align: center;
        }
        form {
            margin-top: 20px;
        }
        label {
            font-size: 16px;
        }
        input {
            padding: 8px;
            font-size: 14px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h2>แก้ไขข้อมูลตัวละคร</h2>

    <!-- ฟอร์มค้นหาตัวละคร -->
    <form action="/" method="POST">
        <label for="charname">ชื่อตัวละคร:</label><br>
        <input type="text" id="charname" name="charname" required><br><br>
        <button type="submit">ค้นหาตัวละคร</button>
    </form>

    <!-- แสดงข้อมูลตัวละครในตาราง -->
    {% if character_data %}
        <table>
            <thead>
                <tr>
                    <th>หัวข้อ</th>
                    <th>ข้อมูล</th>
                </tr>
            </thead>
            <tbody>
                {% for key, value in character_data.items() %}
                <tr>
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- ฟอร์มแก้ไขข้อมูล -->
        <form action="/update" method="POST">
            <h3>อัปเดตข้อมูลตัวละคร</h3>

            <label for="charname">ชื่อตัวละคร:</label><br>
            <input type="text" id="charname" name="charname" value="{{ character_data['Character Name'] }}"><br><br>

            <label for="level">เลเวล:</label><br>
            <input type="text" id="level" name="level" value="{{ character_data['Level'] }}"><br><br>

            <label for="exp">EXP:</label><br>
            <input type="text" id="exp" name="exp" value="{{ character_data['EXP'] }}"><br><br>

            <label for="eclv">ecLv:</label><br>
            <input type="text" id="eclv" name="eclv" value="{{ character_data['ecLv'] }}"><br><br>

            <label for="ecexp">ecEXP:</label><br>
            <input type="text" id="ecexp" name="ecexp" value="{{ character_data['ecEXP'] }}"><br><br>

            <label for="str">STR:</label><br>
            <input type="text" id="str" name="str" value="{{ character_data['STR'] }}"><br><br>

            <label for="lvpoint">LvPoint:</label><br>
            <input type="text" id="lvpoint" name="lvpoint" value="{{ character_data['LvPoint'] }}"><br><br>

            <label for="dex">DEX:</label><br>
            <input type="text" id="dex" name="dex" value="{{ character_data['DEX'] }}"><br><br>

            <label for="skpoint">SkPoint:</label><br>
            <input type="text" id="skpoint" name="skpoint" value="{{ character_data['SkPoint'] }}"><br><br>

            <label for="esp">ESP:</label><br>
            <input type="text" id="esp" name="esp" value="{{ character_data['ESP'] }}"><br><br>

            <label for="lic">LIC:</label><br>
            <input type="text" id="lic" name="lic" value="{{ character_data['LIC'] }}"><br><br>

            <label for="spt">SPT:</label><br>
            <input type="text" id="spt" name="spt" value="{{ character_data['SPT'] }}"><br><br>

            <label for="money">Money:</label><br>
            <input type="text" id="money" name="money" value="{{ character_data['Money'] }}"><br><br>

            <label for="int">INT:</label><br>
            <input type="text" id="int" name="int" value="{{ character_data['INT'] }}"><br><br>

            <label for="bankmoney">Bank:</label><br>
            <input type="text" id="bankmoney" name="bankmoney" value="{{ character_data['Bank'] }}"><br><br>

            <label for="cmap">Map:</label><br>
            <input type="text" id="cmap" name="cmap" value="{{ character_data['Map'] }}"><br><br>

            <label for="hero">Hero:</label><br>
            <input type="text" id="hero" name="hero" value="{{ character_data['Hero'] }}"><br><br>

            <label for="x">X:</label><br>
            <input type="text" id="x" name="x" value="{{ character_data['X'] }}"><br><br>

            <label for="y">Y:</label><br>
            <input type="text" id="y" name="y" value="{{ character_data['Y'] }}"><br><br>

            <label for="z">Z:</label><br>
            <input type="text" id="z" name="z" value="{{ character_data['Z'] }}"><br><br>

            <button type="submit">บันทึกการเปลี่ยนแปลง</button>
        </form>
    {% else %}
        <p>ไม่พบข้อมูลตัวละคร กรุณาค้นหาตัวละครอีกครั้ง</p>
    {% endif %}
</body>
</html>
