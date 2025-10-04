# نصب پیش‌نیازها
pkg update -y && pkg install -y python

#دسترسی به حافظه
termux-setup-storage

# گرفتن فایل پایتون
curl -fsSL https://raw.githubusercontent.com/Sinaksh0/detourconfigs/refs/heads/main/config.manager.py -o config_manager.py

# اجرای فایل
python config_manager.py

# انتقال خروجی به حافظه گوشی
cp configs $HOME/storage/shared/ && echo "✅ All configs are added to the file"
