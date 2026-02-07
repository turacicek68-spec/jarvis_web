# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory # send_from_directory eklendi
import os

app = Flask(__name__)

# --- BASİT VERİ TABANI ---
ACTIVE_DEVICES = set() 

# --- 1. WEB ARAYÜZÜ ---

@app.route('/')
def index():
    return render_template('index.html')

# --- ADS.TXT ÇÖZÜMÜ (Google Onayı İçin Kritik) ---
@app.route('/ads.txt')
def ads_txt():
    # Bu fonksiyon, ana dizindeki ads.txt dosyasını Google'a gösterir
    return send_from_directory(app.root_path, 'ads.txt')

@app.route('/status')
def status():
    return f"Jarvis Sunucusu Aktif. Kayitli Cihaz Sayisi: {len(ACTIVE_DEVICES)}"

# --- 2. JARVIS API ---

@app.post("/api/activate")
def activate():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "error": "Veri gonderilmedi"}), 400
        
    device_id = data.get("device_id")
    if device_id:
        ACTIVE_DEVICES.add(device_id)
        return jsonify({"ok": True, "message": "Jarvis Aktif Edildi!"})
    return jsonify({"ok": False, "error": "Cihaz ID bulunamadi"}), 400

@app.post("/api/ping")
def ping():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "error": "Veri gonderilmedi"}), 400

    device_id = data.get("device_id")
    if device_id in ACTIVE_DEVICES:
        return jsonify({"ok": True, "status": "online"})
    return jsonify({"ok": False, "error": "Cihaz kaydi yok"}), 403

# --- RENDER/VERCEL AYARI ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)