# نصب پیش‌نیازها
pkg update -y && pkg install -y python

# بررسی دسترسی به حافظه
termux-setup-storage

# بررسی نصب emoji
pip install emoji

# گرفتن فایل پایتون
echo "📥 Downloading config_manager.py..."
curl -fsSL https://raw.githubusercontent.com/Sinaksh0/detourconfigs/refs/heads/main/config.manager.py -o config_manager.py

# اجرای فایل
echo "🚀 Launching file..."
python config_manager.py

# انتقال خروجی به حافظه گوشی
cp configs $HOME/storage/shared/ && echo "✅ All configs are added to the file"
