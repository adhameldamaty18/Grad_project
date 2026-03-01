import sqlite3
import os

# مسار قاعدة البيانات داخل الحاوية
DB_PATH = "/app/data/zeinaguard_core.db"

def init_db():
    """إنشاء الجداول اللازمة عند تشغيل السيرفر لأول مرة"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac TEXT UNIQUE,
            ssid TEXT,
            encryption TEXT,
            signal INTEGER,
            risk_score INTEGER,
            status TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_device(data, risk_score, status):
    """حفظ أو تحديث بيانات الجهاز المكتشف"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO devices (mac, ssid, encryption, signal, risk_score, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(mac) DO UPDATE SET
            ssid=excluded.ssid,
            encryption=excluded.encryption,
            signal=excluded.signal,
            risk_score=excluded.risk_score,
            status=excluded.status,
            last_seen=CURRENT_TIMESTAMP
    ''', (data['mac'], data.get('ssid'), data.get('encryption'), data.get('signal'), risk_score, status))
    conn.commit()
    conn.close()

def get_all_devices():
    """جلب كل الأجهزة لعرضها في الـ Dashboard"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices ORDER BY last_seen DESC')
    devices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return devices

def update_device_status(mac, status):
    """تحديث حالة الجهاز يدوياً (Authorized/Blocked)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE devices SET status=? WHERE mac=?', (status, mac))
    conn.commit()
    conn.close()

# تهيئة القاعدة عند استدعاء الملف
init_db()