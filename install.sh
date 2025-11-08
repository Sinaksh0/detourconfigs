#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[34m🔧 Starting Detour setup...\e[0m"

# مرحله 1: بررسی نصب بودن پایتون
if ! command -v python > /dev/null 2>&1; then
    echo -e "\e[33m📦 Python not found. Installing...\e[0m"
    pkg update -y && pkg install -y python || {
        echo -e "\e[31m❌ Failed to install Python. Exiting.\e[0m"
        exit 1
    }
else
    echo -e "\e[32m✅ Python already installed.\e[0m"
fi

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

# مرحله 5: دریافت فایل پایتون
echo -e "\e[33m📥 Downloading file...\e[0m"
curl -fsSL https://raw.githubusercontent.com/Sinaksh0/detourconfigs/main/config.manager.py -o config_manager.py || {
    echo -e "\e[31m❌ Failed to download config_manager.py. Exiting.\e[0m"
    rm -f .env
    exit 1
}

# مرحله 6: اجرای فایل
echo -e "\e[36m🚀 Launching file...\e[0m"
python config_manager.py || {
    echo -e "\e[31m❌ Python script failed to run. Exiting.\e[0m"
    rm -f .env config_manager.py
    exit 1
}

if [ -f configs ]; then
    cp configs "$HOME/storage/shared/" && echo -e "\e[32m✅ All Configs copied to the file.\e[0m"
else
    echo -e "\e[33m⚠️ configs file not found. Skipping copy.\e[0m"
fi

echo -e "\e[32m🎉 Setup complete.\e[0m"
