class ThreatAnalyzer:
    def __init__(self):
        # 1. مصفوفة الأوزان (تم تحديثها لتشمل البصمة المتقدمة)
        self.weights = {
            'OPEN': 100,              # شبكة مفتوحة
            'WEP': 90,                # تشفير ضعيف
            'WPA_LEGACY': 40,         # تشفير قديم
            'BAD_SSID': 50,           # اسم شبكة مشبوه
            'HIGH_SIGNAL': 20,        # إشارة قريبة جداً
            'MAC_SPOOF': 100,         # انتحال صريح للشبكة
            'CHANNEL_SHIFT': 80,      # تغيير القناة (حركة الـ Evil Twin المفضلة)
            'BEACON_ANOMALY': 40,     # تغيير سرعة النبضات
            'RATES_ANOMALY': 30       # اختلاف عدد السرعات المدعومة (علامة على استخدام أداة زي airbase-ng)
        }
        
        self.keywords = ['free', 'guest', 'wifi', 'hacker', 'test', 'public', 'clone', 'hotspot']

        # 2. البصمة المعتمدة (Authorized Baseline)
        # في النسخة النهائية، البيانات دي المفروض تتقرأ من الداتابيز (جدول authorized_aps)
        # بس إحنا حاطين مثال هنا عشان نوضح اللوجيك بيشتغل إزاي
        self.authorized_baselines = {
            "00:14:22:AA:BB:CC": {  # مثال لماك أدرس راوتر الشركة الأصلي
                "ssid": "zeina_corp",
                "channel": 6,       # الراوتر الأصلي شغال على قناة 6
                "vendor": "Dell",
                "beacon_interval": 100, # 102.4 ms
                "rates_len": 12     # الراوتر الأصلي بيدعم 12 سرعة
            }
        }

    def analyze(self, data):
        score = 0
        reasons = []

        # استخراج البيانات القادمة من السنسور
        mac = data.get('mac', '')
        ssid = data.get('ssid', '').lower()
        enc = data.get('encryption', 'OPEN').upper()
        signal = int(data.get('signal', -100))
        channel = int(data.get('channel', 0))
        b_interval = int(data.get('beacon_interval', 100))
        rates_len = int(data.get('supported_rates_len', 0))

        # --- المرحلة الأولى: الفحوصات الأساسية ---
        if 'OPEN' in enc:
            score += self.weights['OPEN']
            reasons.append("Unencrypted Network")
        elif 'WEP' in enc:
            score += self.weights['WEP']
            reasons.append("Weak Encryption (WEP)")

        if any(k in ssid for k in self.keywords):
            score += self.weights['BAD_SSID']
            reasons.append("Suspicious Keyword in SSID")

        if signal > -45:
            score += self.weights['HIGH_SIGNAL']
            reasons.append(f"High Proximity (Signal: {signal}dBm)")

        # --- المرحلة الثانية: فحص البصمة المتقدمة (Fingerprint Match) ---
        baseline = self.authorized_baselines.get(mac)

        if baseline:
            # لو الماك ده تبعنا وموجود في البصمة، هنطابق الخصائص الفيزيائية
            
            # أ. فحص القناة (Channel Shift)
            # الهاكر دايماً بيعمل الراوتر الوهمي على قناة مختلفة عشان يعمل تشويش على الأصلية
            if channel != 0 and channel != baseline['channel']:
                score += self.weights['CHANNEL_SHIFT']
                reasons.append(f"Channel Shift: Expected {baseline['channel']}, Got {channel}")

            # ب. فحص النبضات (Beacon Interval)
            if b_interval != baseline['beacon_interval']:
                score += self.weights['BEACON_ANOMALY']
                reasons.append(f"Abnormal Beacon Interval: {b_interval}")

            # ج. فحص السرعات (Supported Rates)
            if rates_len > 0 and rates_len != baseline['rates_len']:
                score += self.weights['RATES_ANOMALY']
                reasons.append(f"Rates Mismatch: Expected {baseline['rates_len']}, Got {rates_len} (Possible Airbase-ng Tool)")
                
        else:
            # لو الماك مش في البصمة بتاعتنا، بس الراوتر بيذيع اسم شبكة الشركة!
            # دي حالة انتحال صريحة (Rogue AP بيحاول يخدع الموظفين)
            authorized_ssids = [b['ssid'] for b in self.authorized_baselines.values()]
            if ssid in authorized_ssids:
                score += self.weights['MAC_SPOOF']
                reasons.append("SSID Spoofing: Unknown MAC broadcasting Corporate SSID")

        # تقفيل السكور عشان ميزيدش عن 100
        return min(score, 100), reasons

# نسخة جاهزة للاستخدام
analyzer = ThreatAnalyzer()