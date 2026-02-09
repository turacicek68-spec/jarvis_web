# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# JARVIS'ten gelen cihazları tutmak için (Basit bellek içi depo)
ACTIVE_DEVICES = set() 

# --- WEB SAYFASI ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 🛡️ ADS.TXT ÇÖZÜMÜ (Google Onayı İçin En Kritik Kısım) ---
@app.route('/ads.txt')
def ads_txt():
    """Google botları buraya gelince ana dizindeki ads.txt dosyasını okur."""
    return send_from_directory(app.root_path, 'ads.txt')

# --- 🤖 JARVIS API (Asistan Bağlantısı İçin) ---
@app.post("/api/activate")
def activate():
    data = request.get_json()
    if data and "device_id" in data:
        ACTIVE_DEVICES.add(data.get("device_id"))
        return jsonify({"ok": True, "message": "Sistem Aktif!"})
    return jsonify({"ok": False, "error": "Cihaz ID eksik"}), 400

@app.route('/status')
def status():
    return f"Tuğra Tech Sunucusu Aktif. Bağlı Cihaz: {len(ACTIVE_DEVICES)}"

# Vercel ve Render için çalıştırma ayarı
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)