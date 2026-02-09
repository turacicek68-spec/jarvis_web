# app.py - Tuğra Tech AI Final Sürüm
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

# Uygulama ayarlarını ve klasör yollarını netleştiriyoruz
app = Flask(__name__, static_folder='static', template_folder='templates')

# Cihaz takip sistemi (Mevcut özelliğin)
ACTIVE_DEVICES = set() 

# --- ANA SAYFA ---
@app.route('/')
def index():
    """Web sitesinin ana sayfasını yükler."""
    return render_template('index.html')

# --- ADSENSE ONAYI İÇİN KRİTİK ROUTE ---
@app.route('/ads.txt')
def ads_txt():
    """
    Google AdSense botları bu dosyayı kök dizinde arar.
    Bu fonksiyon ads.txt dosyasını ana klasörden bulup sunar.
    """
    return send_from_directory(app.root_path, 'ads.txt', mimetype='text/plain')

# --- SİSTEM DURUMU ---
@app.route('/status')
def status():
    """Sistemin aktif olup olmadığını ve cihaz sayısını gösterir."""
    return f"Tuğra Tech AI: Sistem Aktif. Kayitli Cihaz: {len(ACTIVE_DEVICES)}"

# --- API AKTİVASYON (Cihazlar için) ---
@app.post("/api/activate")
def activate():
    """Dışarıdan gelen aktivasyon isteklerini işler."""
    data = request.get_json()
    if data and "device_id" in data:
        device_id = data.get("device_id")
        ACTIVE_DEVICES.add(device_id)
        return jsonify({"ok": True, "message": f"Cihaz {device_id} Aktif Edildi"})
    return jsonify({"ok": False, "error": "Geçersiz İstek"}), 400

# --- UYGULAMA BAŞLATICI ---
if __name__ == "__main__":
    # Vercel veya lokal ortamda port ayarını otomatik yapar
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)