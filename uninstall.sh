#!/bin/bash

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'

clear
echo -e "${RED}${BOLD}ZENITH IDE UNINSTALLER${RESET}\n"

if [ -f "/usr/local/bin/zenith" ]; then
    echo -e "  [${YELLOW}Auth${RESET}] Menghapus binary dari /usr/local/bin (memerlukan sudo)..."
    sudo rm /usr/local/bin/zenith
    echo -e "  [ ${GREEN}OK${RESET} ] Binary berhasil dihapus."
else
    echo -e "  [ ${CYAN}Info${RESET} ] Binary tidak ditemukan."
fi

if [ -f "$HOME/.local/share/applications/zenith.desktop" ]; then
    rm "$HOME/.local/share/applications/zenith.desktop"
    echo -e "  [ ${GREEN}OK${RESET} ] Desktop shortcut berhasil dihapus."
fi

echo -ne "  [${YELLOW}Conf${RESET}] Hapus folder konfigurasi (~/.config/zenith)? (y/n): "
read -r choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    rm -rf "$HOME/.config/zenith"
    echo -e "  [ ${GREEN}OK${RESET} ] Folder konfigurasi dihapus."
else
    echo -e "  [ ${CYAN}Info${RESET} ] Folder konfigurasi tetap disimpan."
fi

if [ -d "dist" ] || [ -d "build" ]; then
    rm -rf dist build *.spec
    echo -e "  [ ${GREEN}OK${RESET} ] Folder build sementara dibersihkan."
fi

echo -e "\n${GREEN}${BOLD}Uninstall selesai. Zenith telah dihapus dari sistem.${RESET}\n"
