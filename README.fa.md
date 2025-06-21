[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Teacher-Android-App/blob/main/README.fa.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Teacher-Android-App/blob/main/README.md)
# سپاد (مخفف عبارت فارسی سامانه پایش آنلاین دانش آموز)  - Teacher-Android-App
این مخزن بخشی از پروژه SEPAD است و توسط [Abolfazl Rashidian](https://github.com/abolfazlrashidian) برای ورود دانش‌آموزان به کلاس و ارسال میزان توجه آنها به سرور توسعه داده شده است.

برای بازدید از سامانه سپاد، اینجا (https://github.com/SEPAD-Project) کلیک کنید.

## نمای کلی
پنل معلم در SEPAD یک رابط مدیریتی است که به معلمان اجازه می‌دهد سطح توجه دانش‌آموزان را در طول کلاس‌های آنلاین به صورت بلادرنگ رصد کنند. این پنل داده‌های مربوط به تمرکز آنها (از طریق تشخیص چهره و تحلیل نگاه از طریق وب‌کم) را جمع‌آوری کرده و آن را در برنامه دسکتاپ نمایش می‌دهد.

## نیازمندی ها
قبل از نصب، مطمئن شوید که این الزامات را برآورده می‌کنید:
- پایتون 3.8 یا بالاتر برای اجرا بر روی ویندوز یا لینوکس
- اپلیکیشن فلت برای اجرا روی اندروید

## نصب

1. مخزن را کلون کنید:
```bash
git clone https://github.com/SEPAD-Project/Teacher-Android-App.git
```
2. به دایرکتوری Teacher-android-app بروید:
```bash
cd Teacher-android-app
```
3.  یک محیط مجازی بسازید:
```bash
python -m venv .venv
```
4. محیط مجازی را فعال کنید:
```bash
.venv\Scripts\activate.bat
```
5. وابستگی های لازم را نصب کنید:
```bash
pip install -r requirements.txt
```

## اجرای اپلیکیشن
```bash
python RUN.py
```

## ساختار دایرکتوری
```bash
teacher-android-app/
├── source/
├── └──
├──── gui/                          # GUI components
│     └── login.py    # Main application entry point
├──── backend/                      # Attention analysis models
├── RUN.py                          # Run login page
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
└── .gitignore                      # Git ignore file
```

# 📬 تماس  
**Email**: SepadOrganizations@gmail.com  
**Issues**: [GitHub Issues](https://github.com/SEPAD-Project/Teacher-Desktop-App/issues)  