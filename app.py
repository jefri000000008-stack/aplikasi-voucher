from flask import Flask, request, render_template_string
from datetime import datetime
import json
import os

app = Flask(__name__)

FILE = "data_survei.json"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Form Survei</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            padding: 20px;
        }
        .box {
            max-width: 450px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 3px 15px #aaa;
        }
        h2 {
            text-align: center;
        }
        input, textarea, select, button {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            margin-bottom: 15px;
            box-sizing: border-box;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            background: #25D366;
            color: white;
            border: none;
            font-size: 17px;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>FORM SURVEI</h2>

    <form method="POST">

        <label>Nama</label>
        <input type="text" name="nama" required>

        <label>Nomor WhatsApp</label>
        <input type="tel" name="wa" required>

        <label>Paket</label>
        <select name="paket">
            <option>Telkomsel</option>
            <option>by.U</option>
            <option>IM3</option>
            <option>Tri</option>
            <option>XL</option>
        </select>

        <label>Keterangan</label>
        <textarea name="keterangan"></textarea>

        <button type="submit">KIRIM DATA</button>

    </form>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def survei():

    if request.method == "POST":

        data = {
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama": request.form.get("nama"),
            "wa": request.form.get("wa"),
            "paket": request.form.get("paket"),
            "keterangan": request.form.get("keterangan")
        }

        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                semua = json.load(f)
        else:
            semua = []

        semua.append(data)

        with open(FILE, "w") as f:
            json.dump(semua, f, indent=4)

        print("\n==============================")
        print(" DATA SURVEI BARU MASUK")
        print("==============================")
        print("Waktu      :", data["waktu"])
        print("Nama       :", data["nama"])
        print("WhatsApp   :", data["wa"])
        print("Paket      :", data["paket"])
        print("Keterangan :", data["keterangan"])
        print("==============================\n")

        return """
        <h2 style="text-align:center;margin-top:50px">
        Data berhasil dikirim ✅
        </h2>
        """

    return render_template_string(HTML)

app.run(host="0.0.0.0", port=8080)
