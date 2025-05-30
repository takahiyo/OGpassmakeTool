from flask import Flask, request, jsonify

app = Flask(__name__)

def strcat(clsmac):
    return clsmac[2:] + clsmac[6:]

def generate_password(mac_raw):
    mac = mac_raw.replace("-", "").replace(":", "").replace(".", "").replace(" ", "").upper()
    if len(mac) != 12:
        return {"error": "MACアドレス長が不正です。"}
    if not all(c in "0123456789ABCDEF" for c in mac):
        return {"error": "MACアドレスが16進数ではありません。"}
    mac16enc = strcat(mac)
    key = "VoIPGateway48231"
    password = ""
    for i in range(16):
        m = ord(mac16enc[i])
        k = ord(key[i % len(key)])
        p = chr(m | k)
        if not (p.isalnum() or p in "/_-") or ord(p) < 0x21 or ord(p) > 0x7E:
            p = "_"
        password += p
    return {"password": password}

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json()
    mac = data.get("mac", "")
    result = generate_password(mac)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
