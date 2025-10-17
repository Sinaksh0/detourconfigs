#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[34m🔧 Starting Detour setup...\e[0m"

# مرحله 1: نصب پیش‌نیازها
echo -e "\e[33m📦 Updating packages and installing Python...\e[0m"
pkg update -y && pkg install -y python || {
    echo -e "\e[31m❌ Failed to install Python. Exiting.\e[0m"
    exit 1
}

# مرحله 2: بررسی دسترسی به حافظه
if [ ! -d "$HOME/storage/shared" ]; then
    echo -e "\e[33m📂 Storage not set up. Running termux-setup-storage...\e[0m"
    termux-setup-storage
    sleep 2
else
    echo -e "\e[32m✅ Storage access already granted.\e[0m"
fi

# مرحله 3: بررسی نصب emoji
if ! pip show emoji > /dev/null 2>&1; then
    echo -e "\e[33m📦 Installing emoji library...\e[0m"
    pip install emoji || {
        echo -e "\e[31m❌ Failed to install emoji. Exiting.\e[0m"
        exit 1
    }
else
    echo -e "\e[32m✅ emoji already installed.\e[0m"
fi

# مرحله 4: دریافت فایل پایتون
echo -e "\e[33m📥 Downloading config_manager.py...\e[0m"
curl -fsSL https://raw.githubusercontent.com/Sinaksh0/detourconfigs/main/config.manager.py -o config_manager.py || {
    echo -e "\e[31m❌ Failed to download config_manager.py. Exiting.\e[0m"
    exit 1
}

# مرحله 5: اجرای فایل
echo -e "\e[36m🚀 Launching config_manager.py...\e[0m"
python config_manager.py || {
    echo -e "\e[31m❌ Python script failed to run. Exiting.\e[0m"
    exit 1
}

# مرحله 6: انتقال خروجی به حافظه گوشی
if [ -f configs ]; then
    cp configs "$HOME/storage/shared/" && echo -e "\e[32m✅ Configs copied to shared storage.\e[0m"
else
    echo -e "\e[33m⚠️ configs file not found. Skipping copy.\e[0m"
fi

echo -e "\e[32m🎉 Setup complete.\e[0m"