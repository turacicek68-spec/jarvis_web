# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# --- BASİT VERİ TABANI ---
ACTIVE_DEVICES = set() 

# --- 1. WEB ARAYÜZÜ ---

@app.route('/')
def index():
    # Bu rota templates/index.html dosyanı kullanıcıya gösterir
    return render_template('index.html')

# --- 🛡️ ADS.TXT VE STATİK DOSYA ÇÖZÜMÜ (Google Onayı İçin Kritik) ---
@app.route('/ads.txt')
def ads_txt():
    """Google botları jarvis-web-three.vercel.app/ads.txt adresine geldiğinde 
    ana dizindeki ads.txt dosyasını okuyabilmelerini sağlar."""
    return send_from_directory(app.root_path, 'ads.txt')

@app.route('/status')
def status():
    return f"Jarvis Sunucusu Aktif. Kayitli Cihaz Sayisi: {len(ACTIVE_DEVICES)}"

# --- 2. JARVIS API (EXE Bağlantısı İçin) ---

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

# --- RENDER/VERCEL ÇALIŞTIRMA AYARI ---
if __name__ == "__main__":
    # Vercel ve Render gibi platformlarda portu dinamik olarak alır
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)