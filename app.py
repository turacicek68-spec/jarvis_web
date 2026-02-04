# app.py
from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# --- BASİT VERİ TABANI ---
# Sadece hangi cihazların aktif olduğunu tutar
ACTIVE_DEVICES = set() 

# --- 1. WEB ARAYÜZÜ (Reklamların ve Panelin Olduğu Yer) ---

@app.route('/')
def index():
    # Ana sayfa: Reklamlar burada dönecek
    return render_template('index.html')

@app.route('/status')
def status():
    # Sistemin çalışıp çalışmadığını kontrol etmek için basit bir sayfa
    return f"Jarvis Sunucusu Aktif. Toplam kullanıcı: {len(ACTIVE_DEVICES)}"

# --- 2. JARVIS API (Jarvis EXE'sinin bağlandığı kısım) ---

@app.post("/api/activate")
def activate():
    # Jarvis ilk açıldığında buraya bağlanır
    device_id = request.json.get("device_id")
    if device_id:
        ACTIVE_DEVICES.add(device_id)
        return jsonify({"ok": True, "message": "Jarvis Aktif!"})
    return jsonify({"ok": False, "error": "ID bulunamadı"}), 400

@app.post("/api/ping")
def ping():
    # Jarvis çalıştığı sürece buraya sinyal gönderir
    device_id = request.json.get("device_id")
    if device_id in ACTIVE_DEVICES:
        return jsonify({"ok": True, "status": "online"})
    return jsonify({"ok": False, "error": "Cihaz kaydı yok"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)