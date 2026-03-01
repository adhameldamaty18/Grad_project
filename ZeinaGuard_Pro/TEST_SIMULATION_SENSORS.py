import requests
import time
import random
import sys

# --- الإعدادات ---
SERVER_URL = "http://127.0.0.1:5000/api/report"
NEW_DEVICE_INTERVAL = 15 # قللت الوقت شوية عشان التفاعل يبقى أسرع في المناقشة

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

ACTIVE_DEVICES = []

def get_mac():
    return "AC:10:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 1. تجهيز أجهزة الشركة (Authorized Baseline)
print(f"{Colors.HEADER}[*] Initializing Corporate Network (Fingerprinted)...{Colors.ENDC}")
for i in range(1, 6): # كفاية 5 أجهزة عشان الزحمة
    device = {
        "mac": f"AA:BB:CC:00:00:{i:02x}",
        "ssid": "Zeina_Corp_Secure",
        "enc": "WPA2",
        "channel": 6,          # القناة الأصلية للشركة
        "interval": 100,       # السرعة القياسية
        "rates": 12,           # عدد السرعات المدعومة
        "vendor": "Cisco",
        "sensor": "Sensor_Main_Office"
    }
    ACTIVE_DEVICES.append(device)
    print(f"  -> Authorized Asset: {device['mac']} (CH: {device['channel']})")

# --- سيناريوهات الهجوم (تحتوي على بصمات مريبة) ---
INCOMING_SCENARIOS = [
    # هجوم Evil Twin (نفس الاسم بس قناة مختلفة وبصمة مريبة)
    {"ssid": "Zeina_Corp_Secure", "enc": "OPEN", "mac": "AA:BB:CC:00:00:01", "channel": 11, "interval": 100, "rates": 8, "vendor": "Unknown"},
    # شبكة هاكر مفتوحة
    {"ssid": "Hacker_Free_WiFi", "enc": "OPEN", "mac": get_mac(), "channel": 1, "interval": 102, "rates": 4, "vendor": "Unknown"},
    # جهاز بيفحص الشبكة بتشفير قديم
    {"ssid": "Old_Printer_Scanner", "enc": "WEP", "mac": get_mac(), "channel": 6, "interval": 100, "rates": 12, "vendor": "HP"},
]

print(f"\n{Colors.GREEN}[*] Simulation Started. Reporting to {SERVER_URL}{Colors.ENDC}")

last_added_time = time.time()

while True:
    try:
        current_time = time.time()

        # إضافة جهاز جديد من السيناريوهات
        if current_time - last_added_time > NEW_DEVICE_INTERVAL and INCOMING_SCENARIOS:
            new_device = INCOMING_SCENARIOS.pop(0)
            ACTIVE_DEVICES.append(new_device)
            last_added_time = current_time
            print(f"\n{Colors.FAIL} [!!!] SECURITY ALERT: New suspicious signal detected! {Colors.ENDC}")

        # اختيار جهاز عشوائي للتبليغ عنه
        target = random.choice(ACTIVE_DEVICES)
        signal = random.randint(-80, -30)

        # 🎯 بناء الـ Payload المكتمل (البصمة الكاملة)
        payload = {
            "mac": target['mac'],
            "ssid": target.get('ssid', 'Hidden'),
            "encryption": target['enc'],
            "signal": signal,
            "channel": target.get('channel', random.choice()),
            "beacon_interval": target.get('interval', 100),
            "supported_rates_len": target.get('rates', 12),
            "vendor": target.get('vendor', 'Unknown'),
            "sensor_id": target.get('sensor', 'Sensor_Mobile_Unit')
        }

        # إرسال التقرير
        response = requests.post(SERVER_URL, json=payload, timeout=2)
        
        if response.status_code == 200:
            cmd = response.json().get("command")
            status_icon = "🛡️ SCAN"
            col = Colors.BLUE
            if cmd == "BLOCK":
                status_icon = "⛔ NEUTRALIZING"
                col = Colors.FAIL
            
            sys.stdout.write(f"\r{col}[SOC] Monitoring {len(ACTIVE_DEVICES)} nodes | Target: {target['mac']} | Signal: {signal}dBm | Action: {status_icon}    {Colors.ENDC}")
            sys.stdout.flush()

        time.sleep(1) # سرعة التحديث ثانية واحدة عشان الـ Dashboard تبان حية

    except Exception as e:
        print(f"\n[!] Server Offline or Error: {e}")
        time.sleep(3)