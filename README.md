# 🔐 Cyber Steganography Desktop Suite

> **Advanced Data Hiding & Multimedia Forensic Tool** — Aplikasi desktop berbasis PyQt5 berfitur hibrida untuk menyembunyikan dan mengekstrak pesan rahasia ke dalam berbagai format media (**Gambar, Audio, dan Video**) secara aman dan efisien.

---

## 📂 Struktur Direktori Proyek

```text
steganography_app/
├── main.py              # Entry point utama & jendela navigasi GUI
├── styles.py            # Stylesheet tema kustom (Dark Cyber/Forensic UI)
├── steg_functions.py    # Logika matematis (LSB untuk Gambar & EOF untuk Audio/Video)
├── widgets.py           # Komponen UI kustom (Drag & Drop, Preview, WorkerThread)
├── tabs.py              # Panel logika Tab (Embed, Extract, Compare/Forensik)
└── requirements.txt     # Daftar dependensi modul Python

```

---

## ⚙️ Panduan Instalasi & Menjalankan

### 1. Buat & Aktifkan Virtual Environment

```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan (Windows)
.venv\Scripts\activate

# Aktifkan (macOS / Linux)
source .venv/bin/activate

```

### 2. Pasang Dependensi

```bash
pip install -r requirements.txt

```

### 3. Jalankan Aplikasi

```bash
python main.py

```

---

## 🚀 Fitur Utama & Alur Kerja

### Tab 1 — ⚡ Injeksi Data (Embed)

- **Dukungan Media Hibrida**: Mendukung berkas Gambar (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`), Audio (`.mp3`, `.wav`), dan Video (`.mp4`, `.mkv`, `.avi`).
- **Metode Otomatis**:
- **Gambar**: Menggunakan teknik _Least Significant Bit_ (LSB) pada piksel warna.
- **Audio/Video**: Menggunakan teknik _End of File_ (EOF) Injection dengan penanda biner khusus tanpa merusak durasi atau pemutaran media.

- **Fitur Interaktif**:
- Fitur _Drag & Drop_ berkas dengan indikator visual dinamis.
- _Multi-threading_ via `WorkerThread` agar UI utama tidak mengalami _freeze_ saat proses enkripsi berjalan.
- Penghitung kapasitas payload secara _real-time_.

### Tab 2 — 🔍 Ekstraksi Pesan (Extract)

- **Deteksi Format Otomatis**: Sistem secara otomatis mengenali apakah berkas target menggunakan injeksi LSB (gambar) atau penanda EOF (audio/video).
- **Inspeksi Cepat**: Salin hasil dekode dengan satu klik ke _clipboard_ sistem.
- **Pemindaian LSB Cepat**: Menganalisis anomali statistik pada bit terakhir khusus untuk berkas gambar.

### Tab 3 — 📊 Analisis Forensik & Komparasi (Compare)

> ⚠️ **Validasi Ketat**: Fitur forensik dan komparasi piksel ini **hanya eksklusif untuk berkas Gambar**. Sistem akan otomatis menolak berkas non-gambar (audio/video) dan memberikan peringatan.

- **Metrik Komparasi Matematis**: Membandingkan berkas referensi (_original_) dengan berkas target (_stegano_).
- **Parameter Analisis**:
- Menghitung **MSE** (_Mean Squared Error_).
- Menghitung rasio **PSNR** (_Peak Signal-to-Noise Ratio_).
- Menghitung total piksel yang mengalami perubahan serta persentase distorsi visual secara akurat.

---

## 🛠️ Pendekatan Teknis

| Format Media                            | Metode Digunakan                  | Prinsip Kerja                                                                                                                                                                                                                   |
| --------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Gambar** (`.png`, `.jpg`, dll)        | **LSB (_Least Significant Bit_)** | Menyisipkan bit pesan ke dalam bit paling ujung dari kanal warna RGB piksel. Output dikunci dalam format _lossless_ (`.png`) agar data tidak rusak oleh kompresi.                                                               |
| **Audio & Video** (`.mp3`, `.mp4`, dll) | **EOF (_End of File_) Injection** | Menyisipkan payload teks di ujung struktur biner berkas diapit oleh _magic bytes_ (`::CYBER_STEG_START::` & `::CYBER_STEG_END::`). Pemutar media akan mengabaikan data ekstra tersebut sehingga file tetap bisa diputar normal. |

---

## 📦 Build — Compile ke Executable (.exe / Binary)

Gunakan **PyInstaller** untuk mengemas aplikasi menjadi satu berkas mandiri.

### Perintah Build

- **Windows** (Menghasilkan `Steganography.exe`):

```bash
pyinstaller --noconfirm --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." --name=Steganography main.py

```

- **macOS / Linux** (Menghasilkan binary independen):

```bash
pyinstaller --noconfirm --onefile --windowed --icon=favicon.ico --add-data "favicon.ico:." --name=Steganography main.py

```

### Pembersihan File Cache Build

```bash
rm -rf build/ dist/ Steganography.spec

```
