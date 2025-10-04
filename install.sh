

# نصب پیش‌نیازها
pkg update -y && pkg install -y python

# گرفتن فایل پایتون
curl -fsSL https://raw.githubusercontent.com/SinaDev/DetourInstaller/main/config_manager.py -o config_manager.py

# اجرای فایل
python config_manager.py

# انتقال خروجی به حافظه گوشی
cp ss_configs $HOME/storage/downloads/ && echo "✅ فایل منتقل شد به Downloads"
