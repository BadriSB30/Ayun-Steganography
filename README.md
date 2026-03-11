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
