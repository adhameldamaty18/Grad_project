# 1. بنبدأ بنسخة بايثون خفيفة ومنظمة
FROM python:3.10-slim

# 2. بنحدد المجلد اللي الشغل كله هيبقى جواه
WORKDIR /app

# 3. بنثبت المكتبات اللي بنحتاجها عشان الـ Networking والـ SocketIO يشتغلوا
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. بننسخ ملف المكتبات ونثبتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. بننسخ باقي ملفات المشروع (api, engine, database, templates, app.py)
COPY . .

# 6. بنجهز مجلد البيانات عشان الـ SQLite database
RUN mkdir -p /app/data

# 7. بنفتح المنفذ 5000 اللي السيرفر شغال عليه
EXPOSE 5000

# 8. الأمر اللي هيشغل السيرفر أول ما الحاوية تقوم
CMD ["python", "app.py"]