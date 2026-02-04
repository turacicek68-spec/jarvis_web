# app.py
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# --- BASİT VERİ TABANI ---
# Render ücretsiz planda sunucu uyuduğunda bu liste sıfırlanır.
# Ama şu aşamada test için en hızlı yol budur.
ACTIVE_DEVICES = set() 

# --- 1. WEB ARAYÜZÜ (Reklamların ve Panelin Olduğu Yer) ---

@app.route('/')
def index():
    # Bu ana sayfan: templates/index.html dosyanı açar
    return render_template('index.html')

@app.route('/status')
def status():
    # Sistemin çalışıp çalışmadığını anlaman için kontrol sayfası
    return f"Jarvis Sunucusu Aktif. Kayitli Cihaz Sayisi: {len(ACTIVE_DEVICES)}"

# --- 2. JARVIS API (Jarvis EXE'sinin bağlandığı kısım) ---

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

# --- RENDER İÇİN KRİTİK AYAR ---
if __name__ == "__main__":
    # Render PORT bilgisini kendisi atar, eğer bulamazsa 5000 kullanır.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)