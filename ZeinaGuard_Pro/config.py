import os # عشان نعرف نوصل للمجلدات والملفات اللي على الجهاز

class Config:
    # بنحدد هنا مكان المجلد الرئيسي بتاع المشروع كله
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ده المسار اللي هنحفظ فيه قاعدة البيانات اللي فيها كل المعلومات
    DB_PATH = os.path.join(BASE_DIR, 'data', 'zeinaguard_core.db')
    
    # المفتاح السري اللي بنأمن بيه بيانات الموقع وبنشفر بيه الداتا
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZEINA_ULTIMATE_KEY_999'
    
    # ليفل الخطر: لو الجهاز مشبوه بنسبة 85، السيستم هيقفله فوراً
    RISK_CRITICAL = 85  
    
    # لو الخطر وصل 60، بنبعت تنبيه للمسؤول يلحق يتصرف
    RISK_HIGH = 60      
    
    # رقم النسخة واسم السيستم بتاعنا
    VERSION = "5.0.0-ENTERPRISE"
    COMPANY_NAME = "ZeinaGuard Security Systems"