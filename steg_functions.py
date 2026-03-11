"""
steg_functions.py - Fungsi-fungsi inti steganography dan manipulasi gambar
"""

import os
import io
import hashlib
import base64
from PIL import Image
import numpy as np

try:
    from stegano import lsb
    STEGANO_AVAILABLE = True
except ImportError:
    STEGANO_AVAILABLE = False


# ─────────────────────────────────────────────
#   UTILITAS GAMBAR
# ─────────────────────────────────────────────

def load_image(path: str) -> Image.Image:
    """Membuka dan mengembalikan objek PIL Image."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    img = Image.open(path)
    return img


def save_image(img: Image.Image, path: str) -> None:
    """Menyimpan PIL Image ke path yang ditentukan."""
    img.save(path)


def get_image_info(path: str) -> dict:
    """Mengembalikan informasi metadata gambar."""
    img = load_image(path)
    file_size = os.path.getsize(path)
    return {
        "filename": os.path.basename(path),
        "format":   img.format or "PNG",
        "mode":     img.mode,
        "width":    img.size[0],
        "height":   img.size[1],
        "file_size": _format_size(file_size),
        "max_chars": _max_chars_lsb(img),
    }


def _format_size(size_bytes: int) -> str:
    """Format ukuran file menjadi string yang mudah dibaca."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def _max_chars_lsb(img: Image.Image) -> int:
    """Hitung kapasitas maksimal karakter LSB untuk gambar."""
    arr = np.array(img.convert("RGB"))
    total_bits = arr.size  # width * height * 3 channel
    # LSB: 1 bit per channel, 8 bit per karakter + overhead stegano ~32 byte header
    return max(0, (total_bits // 8) - 32)


def image_to_pixmap_bytes(path: str, max_size: tuple = (400, 300)) -> bytes:
    """Mengubah gambar ke bytes PNG untuk ditampilkan di Qt (thumbnail)."""
    img = load_image(path)
    img.thumbnail(max_size, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def convert_to_png(input_path: str, output_path: str) -> str:
    """Konversi gambar ke PNG (diperlukan untuk LSB steganography)."""
    img = load_image(input_path).convert("RGB")
    img.save(output_path, format="PNG")
    return output_path


# ─────────────────────────────────────────────
#   STEGANOGRAPHY - EMBED (SEMBUNYIKAN TEKS)
# ─────────────────────────────────────────────

def embed_text_lsb(image_path: str, secret_text: str, output_path: str) -> dict:
    """
    Menyembunyikan teks di dalam gambar menggunakan metode LSB (Least Significant Bit).

    Args:
        image_path  : Path gambar sumber
        secret_text : Teks rahasia yang akan disembunyikan
        output_path : Path untuk menyimpan gambar hasil

    Returns:
        dict berisi status, pesan, dan info gambar output
    """
    if not STEGANO_AVAILABLE:
        raise RuntimeError("Library 'stegano' tidak tersedia.")

    if not secret_text.strip():
        raise ValueError("Teks rahasia tidak boleh kosong.")

    img_info = get_image_info(image_path)
    if len(secret_text) > img_info["max_chars"]:
        raise ValueError(
            f"Teks terlalu panjang ({len(secret_text)} karakter). "
            f"Kapasitas maksimal gambar ini: {img_info['max_chars']} karakter."
        )

    # Pastikan format PNG
    if not output_path.lower().endswith(".png"):
        output_path = os.path.splitext(output_path)[0] + ".png"

    # Konversi input ke PNG sementara jika bukan PNG
    temp_path = image_path
    if not image_path.lower().endswith(".png"):
        temp_path = output_path + "_temp.png"
        convert_to_png(image_path, temp_path)

    secret_img = lsb.hide(temp_path, secret_text)
    secret_img.save(output_path)

    # Hapus file temp jika ada
    if temp_path != image_path and os.path.exists(temp_path):
        os.remove(temp_path)

    out_info = get_image_info(output_path)
    return {
        "status":      "success",
        "message":     f"Teks berhasil disembunyikan ke dalam gambar.",
        "output_path": output_path,
        "chars_hidden": len(secret_text),
        "image_info":  out_info,
    }


def embed_text_manual_lsb(image_path: str, secret_text: str,
                           output_path: str, bit_depth: int = 1) -> dict:
    """
    Implementasi manual LSB menggunakan NumPy (bit_depth 1-4).
    Berguna untuk kontrol lebih dalam, mendukung multi-bit LSB.
    """
    img = load_image(image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)

    # Encode teks ke bytes lalu ke bit string
    text_bytes = secret_text.encode("utf-8")
    length_prefix = len(text_bytes).to_bytes(4, "big")
    all_bytes = length_prefix + text_bytes
    bits = "".join(f"{byte:08b}" for byte in all_bytes)

    capacity = arr.size * bit_depth
    if len(bits) > capacity:
        raise ValueError(
            f"Teks terlalu panjang. Kapasitas: {capacity // 8} byte, "
            f"Dibutuhkan: {len(all_bytes)} byte."
        )

    flat = arr.flatten()
    mask = (1 << bit_depth) - 1
    clear_mask = ~mask & 0xFF

    for i, bit_chunk in enumerate(_chunks(bits, bit_depth)):
        value = int(bit_chunk.ljust(bit_depth, "0"), 2)
        flat[i] = (flat[i] & clear_mask) | value

    result = flat.reshape(arr.shape)
    out_img = Image.fromarray(result.astype(np.uint8), "RGB")

    if not output_path.lower().endswith(".png"):
        output_path = os.path.splitext(output_path)[0] + ".png"

    out_img.save(output_path)
    out_info = get_image_info(output_path)

    return {
        "status":       "success",
        "message":      f"Teks berhasil disembunyikan ({bit_depth}-bit LSB).",
        "output_path":  output_path,
        "chars_hidden": len(secret_text),
        "image_info":   out_info,
    }


def _chunks(string: str, n: int):
    """Generator: memecah string menjadi potongan sepanjang n."""
    for i in range(0, len(string), n):
        yield string[i:i + n]


# ─────────────────────────────────────────────
#   STEGANOGRAPHY - EXTRACT (BACA TEKS)
# ─────────────────────────────────────────────

def extract_text_lsb(image_path: str) -> dict:
    """
    Mengekstrak teks tersembunyi dari gambar menggunakan metode LSB.

    Returns:
        dict berisi status, teks yang ditemukan, dan info gambar
    """
    if not STEGANO_AVAILABLE:
        raise RuntimeError("Library 'stegano' tidak tersedia.")

    img_info = get_image_info(image_path)

    try:
        secret = lsb.reveal(image_path)
        if secret is None:
            return {
                "status":  "not_found",
                "message": "Tidak ada pesan tersembunyi yang ditemukan di gambar ini.",
                "text":    None,
                "image_info": img_info,
            }
        return {
            "status":  "success",
            "message": f"Pesan berhasil ditemukan! ({len(secret)} karakter)",
            "text":    secret,
            "image_info": img_info,
        }
    except Exception as e:
        return {
            "status":  "not_found",
            "message": f"Tidak ada pesan tersembunyi atau format tidak kompatibel.",
            "text":    None,
            "image_info": img_info,
            "error":   str(e),
        }


def extract_text_manual_lsb(image_path: str, bit_depth: int = 1) -> dict:
    """Ekstrak teks dari gambar yang disisipkan dengan metode manual LSB."""
    img = load_image(image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    img_info = get_image_info(image_path)

    flat = arr.flatten()
    mask = (1 << bit_depth) - 1

    # Baca 32 bit pertama untuk mendapatkan panjang pesan
    header_bits = ""
    for i in range(32 // bit_depth):
        bits = format(flat[i] & mask, f"0{bit_depth}b")
        header_bits += bits
    header_bits = header_bits[:32]

    try:
        text_length = int(header_bits, 2)
        if text_length <= 0 or text_length > 10_000_000:
            raise ValueError("Panjang pesan tidak valid.")

        total_bits_needed = (32 + text_length * 8)
        n_pixels_needed = (total_bits_needed + bit_depth - 1) // bit_depth

        if n_pixels_needed > len(flat):
            raise ValueError("Gambar terlalu kecil untuk pesan yang diklaim.")

        all_bits = ""
        for i in range(n_pixels_needed):
            bits = format(flat[i] & mask, f"0{bit_depth}b")
            all_bits += bits

        # Skip header 32 bit
        data_bits = all_bits[32: 32 + text_length * 8]
        text_bytes = bytes(
            int(data_bits[j:j + 8], 2)
            for j in range(0, len(data_bits), 8)
        )
        secret = text_bytes.decode("utf-8")

        return {
            "status":  "success",
            "message": f"Pesan berhasil diekstrak! ({len(secret)} karakter)",
            "text":    secret,
            "image_info": img_info,
        }
    except Exception as e:
        return {
            "status":  "not_found",
            "message": "Tidak ada pesan manual LSB atau format tidak kompatibel.",
            "text":    None,
            "image_info": img_info,
            "error":   str(e),
        }


# ─────────────────────────────────────────────
#   ANALISIS GAMBAR
# ─────────────────────────────────────────────

def analyze_image_lsb(image_path: str) -> dict:
    """
    Analisis statistik sederhana untuk mendeteksi kemungkinan adanya
    pesan tersembunyi (deteksi anomali LSB sederhana).
    """
    img = load_image(image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)

    # Ambil bit terakhir setiap channel
    lsb_bits = arr & 1
    ratio = lsb_bits.mean()

    # Gambar natural: LSB mendekati 0.5 (acak)
    # Gambar steganografi: sering mendekati 0.5 tapi dengan pola berbeda
    deviation = abs(ratio - 0.5)
    is_suspicious = deviation < 0.02

    channel_means = {
        "R": float((arr[:, :, 0] & 1).mean()),
        "G": float((arr[:, :, 1] & 1).mean()),
        "B": float((arr[:, :, 2] & 1).mean()),
    }

    return {
        "lsb_ratio":       float(ratio),
        "deviation":       float(deviation),
        "is_suspicious":   is_suspicious,
        "channel_lsb":     channel_means,
        "verdict":         "Kemungkinan mengandung pesan tersembunyi" if is_suspicious
                           else "Kemungkinan gambar normal (tidak ada pesan)",
    }


def calculate_image_hash(image_path: str) -> dict:
    """Hitung hash SHA256 dari file gambar."""
    sha256 = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return {
        "sha256": sha256.hexdigest(),
        "short":  sha256.hexdigest()[:16].upper(),
    }


def compare_images(path1: str, path2: str) -> dict:
    """Bandingkan dua gambar dan hitung perbedaan pixel (PSNR)."""
    img1 = np.array(load_image(path1).convert("RGB"), dtype=np.float64)
    img2 = np.array(load_image(path2).convert("RGB"), dtype=np.float64)

    if img1.shape != img2.shape:
        return {"error": "Ukuran gambar berbeda, tidak bisa dibandingkan."}

    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10((255 ** 2) / mse)

    changed_pixels = int(np.sum(np.any(img1 != img2, axis=2)))
    total_pixels = img1.shape[0] * img1.shape[1]

    return {
        "mse":            float(mse),
        "psnr":           float(psnr) if psnr != float("inf") else 999.0,
        "changed_pixels": changed_pixels,
        "total_pixels":   total_pixels,
        "change_percent": round(changed_pixels / total_pixels * 100, 4),
        "quality":        _psnr_to_quality(psnr),
    }


def _psnr_to_quality(psnr: float) -> str:
    if psnr == float("inf") or psnr >= 999:
        return "Identik (tidak ada perubahan)"
    elif psnr > 50:
        return "Sangat baik (tidak terdeteksi mata)"
    elif psnr > 40:
        return "Baik"
    elif psnr > 30:
        return "Cukup"
    else:
        return "Buruk (perubahan terlihat)"
