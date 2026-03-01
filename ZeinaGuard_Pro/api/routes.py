from flask import Blueprint, request, jsonify
from database.db_manager import save_device, get_all_devices, update_device_status
from engine.threat_analyzer import ThreatAnalyzer

# تعريف الـ Blueprint اللي السيرفر بيستخدمه
api_bp = Blueprint('api', __name__)
analyzer = ThreatAnalyzer()

# 1. مسار استقبال البيانات من السنسورات
@api_bp.route('/report', methods=['POST'])
def report_device():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # تحليل التهديد بناءً على البصمة المستلمة
        risk_score, details = analyzer.calculate_risk(data)
        
        # تحديد القرار التلقائي (لو السكور عالي نبعت أمر BLOCK)
        command = "BLOCK" if risk_score > 80 else "IGNORE"
        
        # حفظ البيانات في الداتابيز (SQLite) لضمان استمراريتها
        save_device(data, risk_score, command)
        
        return jsonify({
            "status": "received",
            "risk_score": risk_score,
            "command": command
        }), 200
    except Exception as e:
        print(f"Error in /report: {e}")
        return jsonify({"error": str(e)}), 500

# 2. مسار إرسال البيانات للوحة التحكم (Dashboard)
@api_bp.route('/data', methods=['GET'])
def get_data():
    try:
        # جلب كل الأجهزة المسجلة لعرضها في الجدول
        devices = get_all_devices()
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. مسار التحديث اليدوي (Authorized/Blocked) من الـ Dashboard
@api_bp.route('/update', methods=['POST'])
def update_status():
    try:
        data = request.json
        mac = data.get('mac')
        new_status = data.get('status') # مثل 'Authorized' أو 'Blocked'
        
        if mac and new_status:
            update_device_status(mac, new_status)
            return jsonify({"status": "success", "message": f"Device {mac} updated to {new_status}"}), 200
        
        return jsonify({"error": "Missing MAC or status"}), 400
    except Exception as e:
        # قفل بلوك الـ try بـ except بشكل صحيح يحل مشكلة الـ SyntaxError
        return jsonify({"error": str(e)}), 500