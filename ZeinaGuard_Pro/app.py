from flask import Flask, render_template
from flask_socketio import SocketIO # 🚨 لازم نضيف دي هنا
from api.routes import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zeina_guard_secret_123' # مفتاح أمان لتشفير الاتصال اللحظي

# 1. إعداد الـ SocketIO وربطه بالتطبيق
# cors_allowed_origins="*" عشان يسمح بالاتصال من أي جهاز في الشبكة
socketio = SocketIO(app, cors_allowed_origins="*") 

# 2. تسجيل المسارات (API)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("[*] ZeinaGuard Pro Server is starting...")
    # 3. تشغيل السيرفر باستخدام socketio بدل app.run
    # ده بيخلي السيرفر يقدر يبعت ويستقبل بيانات لحظية (Real-time)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False) # 🛡️ أضف use_reloader=False