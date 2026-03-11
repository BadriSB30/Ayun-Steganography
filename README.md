# 🔐 Steganography Desktop App

Aplikasi desktop untuk menyembunyikan dan membaca teks tersembunyi di dalam gambar menggunakan metode LSB (Least Significant Bit).

## Struktur File

```
steganography_app/
├── main.py              # Entry point & jendela utama
├── styles.py            # Stylesheet & konstanta warna
├── steg_functions.py    # Fungsi inti steganography & analisis
├── widgets.py           # Widget PyQt5 kustom (preview, status, thread)
├── tabs.py              # Panel tab (Embed, Extract, Compare)
└── requirements.txt     # Dependensi Python
```

## Instalasi & Menjalankan

### 1. Buat Virtual Environment

```bash
python -m venv .venv
```

### 2. Aktifkan Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

> Setelah aktif, prompt terminal akan berubah menjadi `(.venv) ...`

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python main.py
```

### 5. Menonaktifkan Virtual Environment (selesai pakai)

```bash
deactivate
```

---

## Fitur

### Tab 1 — Sembunyikan Teks (Embed)

- Pilih gambar sumber (PNG/JPG/BMP/TIFF/WEBP) via browse atau drag & drop
- Ketik pesan rahasia (counter karakter real-time)
- Indikator kapasitas gambar (maks. karakter)
- Proses di background thread (UI tidak freeze)
- Preview gambar output
- Simpan gambar stegano (format PNG)

### Tab 2 — Baca Pesan (Extract)

- Pilih gambar yang diduga mengandung pesan tersembunyi
- Ekstrak pesan dengan satu klik
- Salin hasil ke clipboard
- Analisis LSB statistik (deteksi anomali)

### Tab 3 — Bandingkan Gambar

- Bandingkan gambar asli vs stegano
- Hitung PSNR (Peak Signal-to-Noise Ratio)
- Hitung pixel yang berubah
- Hash SHA256 kedua gambar

## Metode Teknis

Menggunakan **LSB (Least Significant Bit)** via library `stegano`:

- Setiap bit pesan disisipkan ke bit paling tidak signifikan dari setiap channel warna pixel
- Perubahan tidak terlihat oleh mata manusia (PSNR > 50dB)
- Output selalu berformat PNG (lossless)

## Catatan

- Folder `.venv` tidak perlu di-commit ke Git — tambahkan `.venv/` ke `.gitignore`
- Gunakan gambar berukuran cukup besar untuk pesan panjang
- Format output harus PNG (tidak JPEG, karena JPEG lossy dapat merusak data tersembunyi)

---

## Build — Compile ke Executable

Gunakan **PyInstaller** yang sudah termasuk di `requirements.txt`.

### Kenapa `--add-data` wajib disertakan?

Saat `--onefile`, PyInstaller mengekstrak semua file ke folder sementara
`sys._MEIPASS` di runtime — **bukan** di samping `.exe`. Tanpa `--add-data`,
`favicon.ico` tidak ikut terbundle dan icon tidak muncul.

`main.py` sudah menggunakan fungsi `resource_path()` yang otomatis mengarah
ke `sys._MEIPASS` saat berjalan dari build, dan ke folder proyek saat
berjalan dari source.

### Perintah Build

**Windows** — menghasilkan `.exe` satu file:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." --name=Steganography main.py
```

**macOS / Linux** — menghasilkan binary satu file:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=favicon.ico --add-data "favicon.ico:." --name=Steganography main.py
```

> Hasil build ada di folder `dist/Steganography.exe` (Windows) atau `dist/Steganography` (macOS/Linux).

### Penjelasan Flag

| Flag                         | Keterangan                                                                                                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `--onefile`                  | Semua dependensi dikemas dalam **satu file** executable                                                           |
| `--windowed`                 | Jalankan tanpa jendela terminal/console (mode GUI)                                                                |
| `--icon=favicon.ico`         | Icon pada file `.exe` di File Explorer / Finder                                                                   |
| `--add-data "favicon.ico;."` | **Bundel** `favicon.ico` ke dalam `.exe` agar icon muncul saat runtime (Windows pakai `;`, macOS/Linux pakai `:`) |
| `--name=Steganography`       | Nama file output                                                                                                  |
| `--noconfirm`                | Timpa folder `dist/` tanpa konfirmasi                                                                             |

### Membersihkan Hasil Build

```bash
rm -rf build/ dist/ Steganography.spec
```
