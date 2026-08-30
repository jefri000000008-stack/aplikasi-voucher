from flask import Flask, request, redirect, render_template_string
import sqlite3
import urllib.parse

app = Flask(__name__)

DB = "voucher.db"


# =========================
# DATABASE
# =========================

def koneksi():
    return sqlite3.connect(DB)


def buat_database():

    con = koneksi()

    con.execute("""
        CREATE TABLE IF NOT EXISTS voucher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            gb TEXT NOT NULL,
            hari INTEGER NOT NULL,
            modal INTEGER NOT NULL,
            jual INTEGER NOT NULL,
            stok INTEGER DEFAULT 0,
            terjual INTEGER DEFAULT 0
        )
    """)

    con.commit()
    con.close()


# =========================
# FORMAT RUPIAH
# =========================

def rupiah(angka):
    return "Rp {:,.0f}".format(angka).replace(",", ".")


# =========================
# WHATSAPP
# =========================

def whatsapp(v):

    pesan = f"""
📱 *VOUCHER {v[1].upper()}*

📦 Paket : {v[2]}
📅 Masa aktif : {v[3]} hari
💰 Harga : {rupiah(v[5])}

Silakan pesan sekarang.

*Jefri Ponsel*
"""

    return "https://wa.me/?text=" + urllib.parse.quote(pesan)


# =========================
# HTML
# =========================

HTML = """

<!DOCTYPE html>

<html lang="id">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>Penjualan Voucher</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 15px;
    font-family: Arial;
    background: #f2f4f7;
}

.container {
    max-width: 1100px;
    margin: auto;
}

h1 {
    text-align: center;
}

.card {
    background: white;
    padding: 18px;
    margin-bottom: 15px;
    border-radius: 15px;
    box-shadow: 0 3px 10px #ddd;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

input {
    width: 100%;
    padding: 12px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

button {
    border: 0;
    padding: 10px 13px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
}

.tambah {
    width: 100%;
    background: #198754;
    color: white;
    margin-top: 12px;
}

.jual {
    background: #0d6efd;
    color: white;
}

.stok {
    background: #198754;
    color: white;
}

.edit {
    background: #ffc107;
}

.hapus {
    background: #dc3545;
    color: white;
}

.wa {
    background: #25D366;
    color: white;
}

.statistik {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

.stat {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 7px #ddd;
}

.stat b {
    display: block;
    margin-bottom: 8px;
}

.keuntungan {
    color: #198754;
    font-weight: bold;
}

.table-container {
    overflow-x: auto;
}

table {
    width: 100%;
    min-width: 900px;
    border-collapse: collapse;
}

th {
    background: #212529;
    color: white;
}

th, td {
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}

.aksi {
    display: flex;
    gap: 5px;
    justify-content: center;
    flex-wrap: wrap;
}

.habis {
    color: red;
    font-weight: bold;
}

.ada {
    color: green;
    font-weight: bold;
}

@media(max-width:650px) {

    .grid {
        grid-template-columns: 1fr;
    }

    .statistik {
        grid-template-columns: repeat(2, 1fr);
    }

}

</style>

</head>


<body>

<div class="container">


<h1>📱 PENJUALAN VOUCHER</h1>


<!-- STATISTIK -->

<div class="statistik">

<div class="stat">

<b>💰 OMZET</b>

{{ rupiah(omzet) }}

</div>


<div class="stat">

<b>📦 MODAL</b>

{{ rupiah(total_modal) }}

</div>


<div class="stat">

<b>📈 KEUNTUNGAN</b>

<span class="keuntungan">

{{ rupiah(total_keuntungan) }}

</span>

</div>


<div class="stat">

<b>🛒 TERJUAL</b>

{{ total_terjual }}

</div>

</div>


<br>


<!-- TAMBAH -->

<div class="card">

<h3>➕ Tambah Voucher</h3>

<form method="POST" action="/tambah">


<div class="grid">


<div>

<label>Nama Voucher</label>

<input
name="nama"
placeholder="Contoh: Telkomsel OMG"
required>

</div>


<div>

<label>GB</label>

<input
name="gb"
placeholder="Contoh: 15 GB"
required>

</div>


<div>

<label>Hari</label>

<input
type="number"
name="hari"
placeholder="30"
required>

</div>


<div>

<label>Harga Modal</label>

<input
type="number"
name="modal"
placeholder="50000"
required>

</div>


<div>

<label>Harga Jual</label>

<input
type="number"
name="jual"
placeholder="55000"
required>

</div>


<div>

<label>Stok</label>

<input
type="number"
name="stok"
placeholder="10"
required>

</div>


</div>


<button class="tambah">

➕ TAMBAH VOUCHER

</button>


</form>

</div>


<!-- DAFTAR -->

<div class="card">

<h3>📋 Daftar Voucher</h3>


<div class="table-container">


<table>


<tr>

<th>Voucher</th>
<th>GB</th>
<th>Hari</th>
<th>Modal</th>
<th>Jual</th>
<th>Stok</th>
<th>Terjual</th>
<th>Keuntungan</th>
<th>Aksi</th>

</tr>


{% for v in vouchers %}

<tr>


<td>

<b>{{ v[1] }}</b>

</td>


<td>

{{ v[2] }}

</td>


<td>

{{ v[3] }} hari

</td>


<td>

{{ rupiah(v[4]) }}

</td>


<td>

{{ rupiah(v[5]) }}

</td>


<td>

{% if v[6] > 0 %}

<span class="ada">

{{ v[6] }}

</span>

{% else %}

<span class="habis">

HABIS

</span>

{% endif %}

</td>


<td>

{{ v[7] }}

</td>


<td class="keuntungan">

{{ rupiah((v[5] - v[4]) * v[7]) }}

</td>


<td>


<div class="aksi">


{% if v[6] > 0 %}

<a href="/jual/{{ v[0] }}">

<button class="jual">

🛒 JUAL

</button>

</a>

{% endif %}


<a href="/tambah_stok/{{ v[0] }}">

<button class="stok">

+ STOK

</button>

</a>


<a href="/edit/{{ v[0] }}">

<button class="edit">

✏️ EDIT

</button>

</a>


<a
href="/hapus/{{ v[0] }}"
onclick="return confirm('Hapus voucher ini?')">

<button class="hapus">

🗑 HAPUS

</button>

</a>


<a
href="{{ whatsapp(v) }}"
target="_blank">

<button class="wa">

💬 WA

</button>

</a>


</div>

</td>


</tr>

{% endfor %}


</table>

</div>

</div>


</div>

</body>

</html>

"""


# =========================
# HALAMAN UTAMA
# =========================

@app.route("/")
def index():

    con = koneksi()

    vouchers = con.execute("""
        SELECT *
        FROM voucher
        ORDER BY id DESC
    """).fetchall()

    omzet = sum(
        v[5] * v[7]
        for v in vouchers
    )

    total_modal = sum(
        v[4] * v[7]
        for v in vouchers
    )

    total_keuntungan = omzet - total_modal

    total_terjual = sum(
        v[7]
        for v in vouchers
    )

    con.close()

    return render_template_string(
        HTML,
        vouchers=vouchers,
        omzet=omzet,
        total_modal=total_modal,
        total_keuntungan=total_keuntungan,
        total_terjual=total_terjual,
        rupiah=rupiah,
        whatsapp=whatsapp
    )


# =========================
# TAMBAH VOUCHER
# =========================

@app.route("/tambah", methods=["POST"])
def tambah():

    nama = request.form["nama"]
    gb = request.form["gb"]

    hari = int(
        request.form["hari"]
    )

    modal = int(
        request.form["modal"]
    )

    jual = int(
        request.form["jual"]
    )

    stok = int(
        request.form["stok"]
    )


    con = koneksi()

    con.execute("""
        INSERT INTO voucher
        (nama, gb, hari, modal, jual, stok, terjual)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        nama,
        gb,
        hari,
        modal,
        jual,
        stok
    ))

    con.commit()
    con.close()

    return redirect("/")


# =========================
# JUAL
# =========================

@app.route("/jual/<int:id>")
def jual(id):

    con = koneksi()

    con.execute("""
        UPDATE voucher

        SET stok = stok - 1,
            terjual = terjual + 1

        WHERE id = ?
        AND stok > 0
    """, (id,))

    con.commit()
    con.close()

    return redirect("/")


# =========================
# TAMBAH STOK
# =========================

@app.route("/tambah_stok/<int:id>")
def tambah_stok(id):

    con = koneksi()

    con.execute("""
        UPDATE voucher

        SET stok = stok + 1

        WHERE id = ?
    """, (id,))

    con.commit()
    con.close()

    return redirect("/")


# =========================
# HAPUS
# =========================

@app.route("/hapus/<int:id>")
def hapus(id):

    con = koneksi()

    con.execute("""
        DELETE FROM voucher
        WHERE id = ?
    """, (id,))

    con.commit()
    con.close()

    return redirect("/")


# =========================
# EDIT
# =========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    con = koneksi()


    if request.method == "POST":

        nama = request.form["nama"]
        gb = request.form["gb"]

        hari = int(
            request.form["hari"]
        )

        modal = int(
            request.form["modal"]
        )

        jual = int(
            request.form["jual"]
        )

        stok = int(
            request.form["stok"]
        )


        con.execute("""
            UPDATE voucher

            SET nama = ?,
                gb = ?,
                hari = ?,
                modal = ?,
                jual = ?,
                stok = ?

            WHERE id = ?
        """, (
            nama,
            gb,
            hari,
            modal,
            jual,
            stok,
            id
        ))

        con.commit()
        con.close()

        return redirect("/")


    v = con.execute("""
        SELECT *
        FROM voucher
        WHERE id = ?
    """, (id,)).fetchone()

    con.close()


    return f"""

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>Edit Voucher</title>

<style>

body {{
    font-family:Arial;
    background:#f2f4f7;
    padding:20px;
}}

.box {{
    max-width:500px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:15px;
}}

input, button {{
    width:100%;
    padding:12px;
    margin:7px 0;
    box-sizing:border-box;
}}

button {{
    border:0;
    border-radius:8px;
    background:#198754;
    color:white;
    font-weight:bold;
}}

</style>

</head>

<body>


<div class="box">

<h2>✏️ EDIT VOUCHER</h2>


<form method="POST">


Nama Voucher

<input
name="nama"
value="{v[1]}"
required>


GB

<input
name="gb"
value="{v[2]}"
required>


Hari

<input
type="number"
name="hari"
value="{v[3]}"
required>


Harga Modal

<input
type="number"
name="modal"
value="{v[4]}"
required>


Harga Jual

<input
type="number"
name="jual"
value="{v[5]}"
required>


Stok

<input
type="number"
name="stok"
value="{v[6]}"
required>


<button>

💾 SIMPAN

</button>


</form>


<a href="/">

<button>

KEMBALI

</button>

</a>


</div>

</body>

</html>

"""


# =========================
# START
# =========================

if __name__ == "__main__":

    buat_database()

    print("")
    print("==============================")
    print("   ADMIN VOUCHER AKTIF")
    print("==============================")
    print("")
    print("Buka Chrome:")
    print("http://127.0.0.1:8080")
    print("")

    app.run(
        host="0.0.0.0",
        port=8080
    )
