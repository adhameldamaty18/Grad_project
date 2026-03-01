from flask_socketio import emit

def register_socket_handlers(socketio):
    # الدالة دي بتتنفذ أول ما مهندس الـ SOC يفتح لوحة التحكم على المتصفح
    @socketio.on('connect')
    def handle_connect():
        print("[⚡ WebSocket] شاشة الإدارة اتصلت بالسيرفر بنجاح!")
        # بنبعت رسالة ترحيب أو تأكيد للشاشة إن الخط الساخن اشتغل
        emit('system_status', {'status': 'Connected', 'message': 'Live monitoring active'})

    # الدالة دي بتتنفذ لو المتصفح اتقفل أو النت فصل عند الأدمن
    @socketio.on('disconnect')
    def handle_disconnect():
        print("[❌ WebSocket] شاشة الإدارة فصلت!")