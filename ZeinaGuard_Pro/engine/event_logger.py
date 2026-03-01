from database.db_manager import db # بنسحب ملف قاعدة البيانات عشان نعرف نسجل فيه كل اللي بيحصل
import datetime # بنجيب مكتبة الوقت عشان لو حسينا إننا محتاجين نسجل اللحظة بالظبط

class EventLogger: # ده كلاس وظيفته إنه يلم كل عمليات التسجيل في مكان واحد
    def log(self, severity, event, details, target_mac="N/A"): # دي الدالة اللي بتسجل الحدث وبتاخد الأهمية والنوع والتفاصيل وكود الجهاز
        try: # بنجرب نسجل البيانات ولو حصلت مشكلة نلحقها من غير ما السيستم يقع
            # بنشوف لو التفاصيل جاية في شكل قائمة عشان نحولها لنص
            if isinstance(details, list): # لو البيانات عبارة عن لستة
                details = " | ".join(details) # بنحول اللستة لنص واحد وبنحط فاصل بين كل معلومة والتانية
                
            # بنكتب أمر الحفظ في جدول السجلات وبنبعت البيانات بالترتيب
            db.query("INSERT INTO logs (severity, event, details, target_mac) VALUES (?, ?, ?, ?)", 
                    (severity, event, str(details), target_mac))
            
            print(f"[{severity}] {event}: {details}") # بنطبع الحدث على الشاشة السوداء عشان نراقب اللي بيحصل دلوقتي
        except Exception as e: # لو حصل أي غلط في عملية الحفظ
            print(f"Logging Error: {e}") # بنطبع رسالة الغلط عشان نعرف إيه اللي عطل عملية التسجيل

logger = EventLogger() # بنعمل نسخة جاهزة للاستخدام في أي حتة تانية في المشروع