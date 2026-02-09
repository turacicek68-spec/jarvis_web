# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

ACTIVE_DEVICES = set() 

@app.route('/')
def index():
    return render_template('index.html')

# ADS.TXT ÇÖZÜMÜ: Google'ın dosyayı bulması için şart
@app.route('/ads.txt')
def ads_txt():
    # Dosyayı ana dizinden (app.py yanından) çeker
    return send_from_directory(app.root_path, 'ads.txt')

@app.route('/status')
def status():
    return f"Sistem Aktif. Kayitli Cihaz: {len(ACTIVE_DEVICES)}"

@app.post("/api/activate")
def activate():
    data = request.get_json()
    if data and "device_id" in data:
        ACTIVE_DEVICES.add(data.get("device_id"))
        return jsonify({"ok": True, "message": "Aktif Edildi"})
    return jsonify({"ok": False, "error": "Hata"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)