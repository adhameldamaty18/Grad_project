from scapy.all import *
import requests
import threading
import statistics # عشان نحسب متوسط قوة الإشارة بسهولة

# --- إعدادات المستشعر ---
SERVER_URL = "http://192.168.1.100:5000/api/report"
SENSOR_ID = "Pi_Zone_A_Sensor"
INTERFACE = "wlan1mon"

# 1. قائمة الأهداف (Whitelisted SSIDs): 
# السنسور هيركز على حماية الشبكات دي بس عشان ميهلكش موارده في الشارع
TARGET_SSIDS = ["Zeina_Corp", "Zeina_Guest", "Admin_Net"] 

# ذاكرة مؤقتة للسنسور عشان يحسب متوسط قوة الإشارة لكل ماك أدرس
rssi_history = {} 

# قاعدة بيانات مصغرة للشركات المصنعة (OUI) - كمثال للتوضيح
MAC_VENDORS = {
    "00:14:22": "Dell",
    "00:0C:29": "VMware",
    "00:50:56": "VMware",
    "08:00:27": "Oracle/VirtualBox", # مهمة عشان نكشف الرواتر الوهمية
    "B8:27:EB": "Raspberry Pi",
    "DC:A6:32": "Raspberry Pi"
}

def execute_deauth_attack(rogue_mac, iface=INTERFACE, packets_count=100):
    print(f"\n[⚔️] جاري تنفيذ الهجوم المضاد على {rogue_mac}...")
    dot11_radio = RadioTap()
    dot11_mac = Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=rogue_mac, addr3=rogue_mac)
    dot11_command = Dot11Deauth(reason=7)
    sendp(dot11_radio / dot11_mac / dot11_command, iface=iface, count=packets_count, inter=0.1, verbose=False)
    print(f"[✔] تم تحييد المهاجم {rogue_mac} بنجاح!\n")

def get_vendor(mac):
    # بنقطع أول 8 حروف من الماك (اللي هم أول 3 أجزاء) وندور عليهم
    oui = mac[:8].upper()
    return MAC_VENDORS.get(oui, "Unknown")

def extract_advanced_info(pkt):
    """
    دالة بتغوص في طبقات الـ Information Elements عشان تطلع البصمة
    """
    channel = 0
    rates = []
    encryption = "OPEN" # افتراضي
    
    # استخراج الـ Beacon Interval من طبقة الـ Beacon
    beacon_interval = pkt[Dot11Beacon].beacon_interval

    p = pkt[Dot11Elt]
    crypto = set()
    
    while isinstance(p, Dot11Elt):
        # ID 3: DS Parameter Set (بيحتوي على رقم القناة)
        if p.ID == 3:
            try:
                channel = int.from_bytes(p.info, byteorder='little')
            except: pass
            
        # ID 1 & 50: Supported Rates & Extended Supported Rates
        elif p.ID in (1, 50):
            try:
                rates.extend(list(p.info))
            except: pass
            
        # التشفير
        elif p.ID == 48: crypto.add("WPA2")
        elif p.ID == 221 and p.info.startswith(b'\x00P\xf2\x01\x01\x00'): crypto.add("WPA")
        
        p = p.payload

    if not crypto:
        if pkt.sprintf("%Dot11.FCfield%").find("wep") != -1: encryption = "WEP"
    else:
        encryption = "/".join(crypto)
        
    return channel, rates, encryption, beacon_interval

def packet_handler(pkt):
    if pkt.haslayer(Dot11Beacon):
        mac_address = pkt[Dot11].addr2
        try:
            ssid = pkt[Dot11Elt].info.decode('utf-8')
        except:
            ssid = "Hidden"

        # 🎯 الفلترة: لو الشبكة مش في قايمة أهداف الشركة، تجاهلها وكمل
        if TARGET_SSIDS and ssid not in TARGET_SSIDS:
            return

        # 📊 حساب متوسط الإشارة (Average RSSI)
        try:
            signal_strength = pkt[RadioTap].dBm_AntSignal
        except:
            signal_strength = -100

        if mac_address not in rssi_history:
            rssi_history[mac_address] = []
        rssi_history[mac_address].append(signal_strength)
        
        # بنحتفظ بآخر 5 قراءات بس عشان الذاكرة متتمليش
        if len(rssi_history[mac_address]) > 5:
            rssi_history[mac_address].pop(0)
            
        # بنحسب المتوسط الحسابي
        avg_signal = int(statistics.mean(rssi_history[mac_address]))

        # 🔍 استخراج البصمة المتقدمة
        channel, rates, encryption, beacon_interval = extract_advanced_info(pkt)
        vendor = get_vendor(mac_address)

        # 📦 تجهيز البلاغ (البصمة الكاملة)
        report_data = {
            "mac": mac_address,
            "ssid": ssid,
            "signal": avg_signal, # بنبعت المتوسط مش القراءة اللحظية
            "channel": channel,
            "beacon_interval": beacon_interval,
            "vendor": vendor,
            "supported_rates_len": len(rates), # عدد السرعات المدعومة بيكشف الهاكر
            "encryption": encryption,
            "sensor_id": SENSOR_ID
        }

        # 🚀 إرسال البلاغ للسيرفر
        try:
            response = requests.post(SERVER_URL, json=report_data, timeout=2)
            command = response.json().get("command", "SCAN")
            
            if command == "BLOCK":
                print(f"[!!!] خطر: هجوم من {ssid} ({mac_address})! جاري التعامل...")
                attack_thread = threading.Thread(target=execute_deauth_attack, args=(mac_address, INTERFACE))
                attack_thread.start()
        except requests.exceptions.RequestException:
            pass

if __name__ == "__main__":
    print(f"[*] جاري تشغيل مستشعر ZeinaGuard المتقدم على {INTERFACE}...")
    sniff(iface=INTERFACE, prn=packet_handler, store=0)