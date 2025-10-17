# نصب پیش‌نیازها
pkg update -y && pkg install -y python

# بررسی دسترسی به حافظه
if [ ! -d "$HOME/storage/shared" ]; then
    echo "📂 Storage not set up. Running termux-setup-storage..."
    termux-setup-storage
else
    echo "✅ Storage access already granted."
fi

# بررسی نصب emoji
if ! pip show emoji > /dev/null 2>&1; then
    echo "📦 Installing emoji library..."
    pip install emoji
else
    echo "✅ emoji already installed."
fi

# گرفتن فایل پایتون
echo "📥 Downloading config_manager.py..."
curl -fsSL https://raw.githubusercontent.com/Sinaksh0/detourconfigs/refs/heads/main/config.manager.py -o config_manager.py

# اجرای فایل
echo "🚀 Launching file..."
python config_manager.py

# انتقال خروجی به حافظه گوشی
cp configs $HOME/storage/shared/ && echo "✅ All configs are added to the file"
