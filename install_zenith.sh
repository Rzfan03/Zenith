#!/bin/bash

# --- WARNA ---
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'

clear
echo -e "${PURPLE}${BOLD}"
echo "  ███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗"
echo "  ╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║"
echo "    ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║"
echo "   ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║"
echo "  ███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║"
echo "  ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝"
echo -e "             ZENITH IDE v8.9 PRO INSTALLER${RESET}\n"

# --- CEK FILE ---
echo -ne "  [${YELLOW}Wait${RESET}] Checking source files..."
if [[ ! -f "code.py" || ! -f "theme.css" ]]; then
    echo -e "\r  [ ${RED}ERR${RESET} ] code.py atau theme.css tidak ditemukan!"
    exit 1
fi
echo -e "\r  [ ${GREEN}OK${RESET} ] Source files detected."

# --- 1. INSTALL DEPENDENCIES ---
echo -ne "  [${YELLOW}Wait${RESET}] Syncing dependencies..."
pip install pyinstaller textual > /dev/null 2>&1
echo -e "\r  [ ${GREEN}OK${RESET} ] Dependencies ready."

# --- 2. BUILD BINARY DENGAN EMBEDDED CSS ---
echo -ne "  [${YELLOW}Wait${RESET}] Compiling Zenith (this may take a moment)..."
# Menggunakan --add-data agar theme.css masuk ke dalam binary
pyinstaller --onefile --windowed --add-data "theme.css:." --name zenith code.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "\r  [ ${RED}ERR${RESET} ] Build failed! Check your code.py."
    exit 1
fi
echo -e "\r  [ ${GREEN}OK${RESET} ] Binary compiled successfully."

# --- 3. PINDAHKAN KE SYSTEM PATH ---
echo -e "  [${YELLOW}Auth${RESET}] Moving to /usr/local/bin (requires sudo)..."
sudo mv dist/zenith /usr/local/bin/
sudo chmod +x /usr/local/bin/zenith

# --- 4. SETUP USER CONFIG ---
echo -ne "  [${YELLOW}Wait${RESET}] Setting up user configuration..."
mkdir -p ~/.config/zenith
cp theme.css ~/.config/zenith/
echo -e "\r  [ ${GREEN}OK${RESET} ] Config folder created at ~/.config/zenith/"

# --- 5. GENERATE DESKTOP ENTRY ---
echo -ne "  [${YELLOW}Wait${RESET}] Creating desktop shortcut..."
cat <<EOF > ~/.local/share/applications/zenith.desktop
[Desktop Entry]
Type=Application
Name=Zenith IDE
Comment=Professional TUI IDE
Exec=alacritty -e zenith %f
Icon=utilities-terminal
Terminal=false
Categories=Development;TextEditor;
EOF
echo -e "\r  [ ${GREEN}OK${RESET} ] Desktop entry generated."

# --- SELESAI ---
echo -e "\n${GREEN}${BOLD}  ✨ ZENITH IDE INSTALLED SUCCESSFULLY! ✨${RESET}"
echo -e "${CYAN}--------------------------------------------------${RESET}"
echo -e "  🚀  Command:      ${BOLD}zenith${RESET}"
echo -e "  🎨  Custom Theme: ${BOLD}~/.config/zenith/theme.css${RESET}"
echo -e "  📂  Workspace:    ${BOLD}zenith <folder_path>${RESET}"
echo -e "${CYAN}--------------------------------------------------${RESET}\n"
