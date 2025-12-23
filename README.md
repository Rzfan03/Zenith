# Zenith IDE v8.8 Pro

Zenith adalah Integrated Development Environment (IDE) berbasis terminal (TUI) yang menggabungkan kecepatan navigasi Miller Columns bergaya Ranger dengan fitur editor teks modern. Proyek ini dirancang untuk efisiensi alur kerja maksimal bagi pengguna yang mengutamakan penggunaan keyboard.

---

## Fitur Utama

- **Navigasi Ranger**: Sistem penjelajahan file menggunakan Miller Columns untuk visibilitas struktur folder yang mendalam.
- **Editing Modal**: Implementasi mode Normal dan Insert untuk efisiensi input dan navigasi teks.
- **Engine Tema CSS**: Kustomisasi visual penuh melalui file theme.css tanpa perlu melakukan kompilasi ulang.
- **Workspace Terintegrasi**: Penggabungan terminal, sidebar navigasi, dan editor dalam satu interface tunggal.
- **Performa Ringan**: Penggunaan sumber daya sistem yang minimal, dioptimalkan untuk lingkungan terminal Linux dan Windows.
- **Dukungan Nerd Font**: Integrasi ikon untuk berbagai bahasa pemrograman dan tipe file.

---

## Pintasan Keyboard

### Navigasi dan Manajemen File
| Tombol | Aksi |
| :--- | :--- |
| Ctrl + O | Membuka Ranger (Berpindah Workspace) |
| Ctrl + N | Membuat file baru |
| F2 | Mengubah nama file atau folder |
| Ctrl + D | Menghapus file atau folder |
| Ctrl + S | Menyimpan perubahan file |
| Ctrl + B | Toggle visibilitas sidebar |

### Mode Editor
| Tombol | Aksi |
| :--- | :--- |
| i | Mode INSERT (Mengetik teks) |
| Esc | Mode NORMAL (Navigasi dan perintah) |
| F5 | Menjalankan kode (Execute script) |

---

## Instruksi Instalasi

### Prasyarat
- Python 3.x
- Nerd Font (direkomendasikan: JetBrainsMono Nerd Font)

### Instalasi Otomatis (Linux)
Jalankan script installer yang tersedia di dalam repositori:
```bash
chmod +x install.sh
./install.sh
