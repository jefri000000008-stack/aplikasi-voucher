from http.server import HTTPServer, BaseHTTPRequestHandler

html = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kurir Sumala</title>

<style>
body{
    margin:0;
    height:100vh;
    overflow:hidden;
    font-family:Arial;
    background:linear-gradient(#ff7b00,#ffd45c 65%,#4caf50 65%);
}

.judul{
    text-align:center;
    color:white;
    padding:20px;
    font-size:28px;
    font-weight:bold;
    text-shadow:0 3px 5px #7b2d00;
}

.kurir{
    position:absolute;
    left:-150px;
    bottom:28%;
    font-size:100px;
    animation:jalan 5s linear forwards;
}

@keyframes jalan{
    from{left:-150px}
    to{left:42%}
}

.paket{
    position:absolute;
    left:50%;
    bottom:20%;
    transform:translateX(-50%);
    font-size:90px;
    cursor:pointer;
    animation:goyang 1.5s infinite;
}

@keyframes goyang{
    50%{transform:translateX(-50%) translateY(-10px)}
}

.petunjuk{
    position:absolute;
    bottom:8%;
    width:100%;
    text-align:center;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.hasil{
    display:none;
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.85);
    align-items:center;
    justify-content:center;
    flex-direction:column;
    color:white;
}

.hasil h2{
    font-size:28px;
}

#kata{
    font-size:55px;
    font-weight:bold;
    color:#ffe600;
    text-shadow:0 0 20px orange;
    letter-spacing:10px;
}

button{
    margin-top:30px;
    padding:15px 30px;
    border:0;
    border-radius:25px;
    background:#ff5a00;
    color:white;
    font-size:18px;
    font-weight:bold;
}
</style>
</head>

<body>

<div class="judul">
🛵 KURIR MEMBAWA PAKET
</div>

<div class="kurir">
🛵
</div>

<div class="paket" onclick="bukaPaket()">
📦
</div>

<div class="petunjuk">
👆 SENTUH PAKET
</div>

<div class="hasil" id="hasil">

<h2>📦 ISI PAKET</h2>

<div id="kata"></div>

<button onclick="ulang()">
🔄 MAIN LAGI
</button>

</div>

<script>

let sudah=false;

function bukaPaket(){

    if(sudah) return;

    sudah=true;

    document.querySelector(".paket").innerHTML="💥";

    setTimeout(function(){

        document.getElementById("hasil").style.display="flex";

        let kata="SUMALA";
        let posisi=0;

        function keluar(){

            if(posisi < kata.length){

                document.getElementById("kata").innerHTML += kata[posisi];

                posisi++;

                setTimeout(keluar,600);
            }
        }

        keluar();

    },800);
}

function ulang(){

    sudah=false;

    document.getElementById("hasil").style.display="none";

    document.getElementById("kata").innerHTML="";

    document.querySelector(".paket").innerHTML="📦";

    location.reload();
}

</script>

</body>
</html>"""

class Web(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            html.encode("utf-8")
        )


server = HTTPServer(
    ("0.0.0.0",8080),
    Web
)

print("")
print("==============================")
print("       SUMALA WEB")
print("==============================")
print("")
print("Server aktif!")
print("")
print("Buka Chrome:")
print("http://127.0.0.1:8080")
print("")
print("Tekan CTRL+C untuk berhenti")

server.serve_forever()
