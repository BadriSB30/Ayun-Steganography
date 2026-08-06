"""
steg_functions.py - Fungsi-fungsi inti steganography dan manipulasi gambar
Mendukung LSB untuk Gambar dan EOF (End of File) Injection untuk Audio/Video.
"""

import os
import io
from PIL import Image
import numpy as np

# Cek ketersediaan library pihak ketiga untuk steganografi cepat
try:
    from stegano import lsb
    STEGANO_AVAILABLE = True
except ImportError:
    STEGANO_AVAILABLE = False

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
MAGIC_START = b"::CYBER_STEG_START::"
MAGIC_END = b"::CYBER_STEG_END::"

# ─────────────────────────────────────────────
#   UTILITAS MULTIMEDIA
# ─────────────────────────────────────────────

def get_multimedia_info(path: str) -> dict:
    """Mengekstrak metadata tanpa memicu error jika target adalah video/audio."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
        
    ext = os.path.splitext(path)[1].lower()
    file_size = os.path.getsize(path)
    filename = os.path.basename(path)
    
    if ext in IMAGE_EXTENSIONS:
        img = Image.open(path)
        return {
            "filename": filename,
            "type": "Gambar",
            "format": img.format or ext[1:].upper(),
            "file_size": _format_size(file_size),
            "max_chars": _max_chars_lsb(img),
            "is_image": True
        }
    else:
        # Pendekatan untuk file Audio / Video
        return {
            "filename": filename,
            "type": "Audio/Video",
            "format": ext[1:].upper(),
            "file_size": _format_size(file_size),
            "max_chars": 9999999, # EOF secara teoritis tidak memiliki batas kecuali ruang disk
            "is_image": False
        }

def _format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def _max_chars_lsb(img: Image.Image) -> int:
    arr = np.array(img.convert("RGB"))
    return max(0, (arr.size // 8) - 32)

def convert_to_png(input_path: str, output_path: str) -> str:
    img = Image.open(input_path).convert("RGB")
    img.save(output_path, format="PNG")
    return output_path


# ─────────────────────────────────────────────
#   METODE 1: STEGANOGRAPHY GAMBAR (LSB)
# ─────────────────────────────────────────────

def embed_text_lsb(image_path: str, secret_text: str, output_path: str) -> dict:
    if not STEGANO_AVAILABLE:
        raise RuntimeError("Library 'stegano' tidak tersedia.")
    if not secret_text.strip():
        raise ValueError("Teks rahasia tidak boleh kosong.")

    img_info = get_multimedia_info(image_path)
    if len(secret_text) > img_info["max_chars"]:
        raise ValueError(f"Teks melebih kapasitas piksel ({img_info['max_chars']} char).")

    temp_path = image_path
    if not image_path.lower().endswith(".png"):
        temp_path = output_path + "_temp.png"
        convert_to_png(image_path, temp_path)

    secret_img = lsb.hide(temp_path, secret_text)
    secret_img.save(output_path)

    if temp_path != image_path and os.path.exists(temp_path):
        os.remove(temp_path)

    return {
        "status": "success",
        "message": "Teks disembunyikan dalam piksel (LSB).",
        "output_path": output_path,
        "chars_hidden": len(secret_text),
        "image_info": get_multimedia_info(output_path),
    }

def extract_text_lsb(image_path: str) -> dict:
    info = get_multimedia_info(image_path)
    try:
        secret = lsb.reveal(image_path)
        if not secret:
            return {"status": "not_found", "message": "Tidak ada data LSB.", "text": None, "image_info": info}
        return {"status": "success", "message": "Pesan ditemukan (LSB)!", "text": secret, "image_info": info}
    except Exception as e:
        return {"status": "error", "message": "File rusak/format tak dikenali", "text": None, "image_info": info, "error": str(e)}


# ─────────────────────────────────────────────
#   METODE 2: STEGANOGRAPHY AUDIO/VIDEO (EOF)
# ─────────────────────────────────────────────

def embed_eof_multimedia(file_path: str, secret_text: str, output_path: str) -> dict:
    """Menginjeksi data pada akhir struktur hex video/audio (End of File)."""
    if not secret_text.strip():
        raise ValueError("Teks rahasia tidak boleh kosong.")
        
    text_bytes = secret_text.encode("utf-8")
    
    with open(file_path, "rb") as f:
        original_data = f.read()
        
    with open(output_path, "wb") as f:
        f.write(original_data)
        f.write(MAGIC_START)
        f.write(text_bytes)
        f.write(MAGIC_END)
        
    return {
        "status": "success",
        "message": "Teks ditanam via End of File (EOF).",
        "output_path": output_path,
        "chars_hidden": len(secret_text),
        "image_info": get_multimedia_info(output_path)
    }

def extract_eof_multimedia(file_path: str) -> dict:
    """Membaca stempel MAGIC_START dan MAGIC_END pada EOF video/audio."""
    info = get_multimedia_info(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
        
    start_idx = content.rfind(MAGIC_START)
    end_idx = content.rfind(MAGIC_END)
    
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        data_bytes = content[start_idx + len(MAGIC_START):end_idx]
        return {
            "status": "success",
            "message": "Pesan ditemukan (EOF)!",
            "text": data_bytes.decode("utf-8", errors="ignore"),
            "image_info": info
        }
        
    return {
        "status": "not_found",
        "message": "Tidak ditemukan anomali EOF.",
        "text": None,
        "image_info": info
    }


# ─────────────────────────────────────────────
#   ANALISIS FORENSIK (HANYA GAMBAR)
# ─────────────────────────────────────────────

def compare_images(path1: str, path2: str) -> dict:
    img1 = np.array(Image.open(path1).convert("RGB"), dtype=np.float64)
    img2 = np.array(Image.open(path2).convert("RGB"), dtype=np.float64)

    if img1.shape != img2.shape:
        return {"error": "Dimensi resolusi berbeda. Tidak dapat dibandingkan secara akurat."}

    mse = np.mean((img1 - img2) ** 2)
    psnr = 10 * np.log10((255 ** 2) / mse) if mse > 0 else 999.0
    changed_pixels = int(np.sum(np.any(img1 != img2, axis=2)))
    
    return {
        "mse": float(mse),
        "psnr": float(psnr),
        "changed_pixels": changed_pixels,
        "total_pixels": img1.shape[0] * img1.shape[1],
        "change_percent": round(changed_pixels / (img1.shape[0] * img1.shape[1]) * 100, 4),
        "quality": "Sempurna" if psnr > 50 else "Buruk",
    }