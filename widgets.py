"""
widgets.py - Widget kustom PyQt5 untuk aplikasi Steganography
Kumpulan komponen UI yang dibuat sendiri agar lebih interaktif.
"""

import os
from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from styles import STATUS_COLORS, COLORS

class ImagePreviewWidget(QLabel):
    """
    Widget khusus berbentuk kotak (Label) yang mendukung fitur:
    - Menampilkan gambar (scaled) atau info file multimedia.
    - Mendukung tarik-dan-lepas (Drag & Drop) file multimedia dari komputer.
    """
    image_dropped = pyqtSignal(str) # Sinyal yang dipancarkan saat file di-drop

    def __init__(self, placeholder_text="DRAG & DROP\nATAU PILIH FILE MULTIMEDIA", parent=None):
        super().__init__(parent)
        self._placeholder = placeholder_text
        self._image_path = None

        self.setAcceptDrops(True) # Mengaktifkan mode Drag & Drop
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(320, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setObjectName("image_placeholder")
        self._show_placeholder()

    def _show_placeholder(self):
        """Menampilkan teks default jika belum ada file"""
        self.setText(self._placeholder)
        self.setStyleSheet("""
            QLabel {
                color: #64748B;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
                border: 2px dashed #334155;
                background-color: #0B1120;
                border-radius: 8px;
            }
        """)

    def set_image(self, file_path: str):
        """Merender gambar jika format didukung, atau teks nama file jika Audio/Video"""
        self._image_path = file_path
        
        # Cek apakah file adalah gambar untuk dirender
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Mengecilkan gambar agar muat di layar dengan menjaga rasio aslinya (KeepAspectRatio)
                scaled = pixmap.scaled(
                    self.width() - 16, self.height() - 16,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.setPixmap(scaled)
                
                # Mengubah bingkai saat gambar berhasil dimuat
                self.setStyleSheet("""
                    QLabel {
                        border: 2px solid #0EA5E9; /* Bingkai cyan */
                        background-color: #1E293B;
                        border-radius: 8px;
                        padding: 8px;
                    }
                """)
                return

        # Jika file adalah Audio / Video (atau gambar rusak)
        self.clear()
        filename = os.path.basename(file_path)
        self.setText(f"FILE MULTIMEDIA DIMUAT:\n{filename}")
        self.setStyleSheet("""
            QLabel {
                color: #10B981;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 1px;
                border: 2px solid #10B981;
                background-color: #1E293B;
                border-radius: 8px;
                padding: 8px;
            }
        """)

    def clear_image(self):
        """Menghapus file dan mengembalikan ke tampilan awal"""
        self._image_path = None
        self.clear()
        self._show_placeholder()

    @property
    def image_path(self):
        return self._image_path

    # --- Event Handler untuk Interaksi Drag & Drop ---
    def dragEnterEvent(self, event):
        """Saat kursor membawa file memasuki area widget"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Cek apakah file tersebut adalah multimedia (Gambar, Audio, Video)
            if urls and _is_multimedia_file(urls[0].toLocalFile()):
                event.acceptProposedAction()
                # Berikan efek "menyala" (Cyan) untuk memberi tahu user bahwa area ini valid
                self.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #0EA5E9;
                        background-color: rgba(14, 165, 233, 0.1);
                        color: #0EA5E9;
                        border-radius: 8px;
                    }
                """)

    def dragLeaveEvent(self, event):
        """Saat kursor membatalkan/keluar dari area widget"""
        if self._image_path:
            self.set_image(self._image_path)
        else:
            self._show_placeholder()

    def dropEvent(self, event):
        """Saat user melepaskan file multimedia (drop) di dalam widget"""
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if _is_multimedia_file(path):
                self.set_image(path)
                self.image_dropped.emit(path) # Kirim path file ke sistem (Tab)

    def resizeEvent(self, event):
        """Pastikan konten ikut meresize jika jendela diperbesar/diperkecil"""
        super().resizeEvent(event)
        if self._image_path:
            self.set_image(self._image_path)

def _is_multimedia_file(path: str) -> bool:
    """Fungsi pembantu: Mengecek ekstensi file multimedia (Gambar, Audio, Video) yang valid"""
    valid_extensions = (
        # Gambar
        ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp",
        # Audio
        ".mp3", ".wav", ".ogg", ".flac",
        # Video
        ".mp4", ".avi", ".mkv", ".mov"
    )
    return path.lower().endswith(valid_extensions)

class StatusBar(QWidget):
    """Widget panel kecil untuk menampilkan status 'Sukses', 'Error', 'Proses', dll"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 4, 12, 4)
        self._layout.setSpacing(8)

        self._dot = QLabel("●") # Ikon titik (indikator warna)
        self._dot.setFixedWidth(16)

        self._label = QLabel("STANDBY")
        self._label.setObjectName("status_label")
        self._label.setStyleSheet("font-weight: 700; font-size: 11px; font-family: 'Consolas';")

        self._layout.addWidget(self._dot)
        self._layout.addWidget(self._label)
        self._layout.addStretch()

        self.setFixedHeight(30)
        self.set_status("idle", "STANDBY")

    def set_status(self, level: str, message: str):
        """Mengubah teks dan warna indikator (level: success, error, info, working)"""
        color = STATUS_COLORS.get(level, STATUS_COLORS["idle"])
        self._dot.setStyleSheet(f"color: {color}; font-size: 14px;")
        self._label.setStyleSheet(f"color: {color}; font-weight: bold; letter-spacing: 1px;")
        self._label.setText(message.upper())

class InfoPanel(QFrame):
    """Widget untuk menampilkan rincian data (Kunci - Nilai) seperti tabel tanpa bingkai"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        self.setStyleSheet("background: transparent;")

    def set_info(self, data: dict):
        """Memasukkan data dictionary dan membuat label baris per baris"""
        self.clear()
        for key, value in data.items():
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            hl = QHBoxLayout(row)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(8)

            key_label = QLabel(f"{key}")
            key_label.setFixedWidth(100)
            key_label.setStyleSheet("color: #64748B; font-weight: bold; font-size: 11px;")

            val_label = QLabel(str(value))
            val_label.setStyleSheet("color: #CBD5E1; font-weight: bold; font-size: 12px; font-family: 'Consolas';")
            val_label.setWordWrap(True)

            hl.addWidget(key_label)
            hl.addWidget(val_label, 1)
            self._layout.addWidget(row)

    def clear(self):
        """Menghapus semua baris data"""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

class WorkerThread(QThread):
    """
    Sistem Multi-Threading:
    Memungkinkan proses steganografi (yang memakan waktu) berjalan di latar belakang (background),
    sehingga UI utama (tombol, layar) tidak 'not responding' atau 'freeze'.
    """
    result_ready  = pyqtSignal(dict) # Sinyal saat selesai
    error_occurred = pyqtSignal(str) # Sinyal jika gagal
    progress      = pyqtSignal(int)  # Sinyal untuk progress bar (0-100%)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        """Fungsi yang akan dijalankan oleh CPU di thread terpisah"""
        try:
            self.progress.emit(30) # Asumsikan progress 30% saat mulai menghitung
            result = self._func(*self._args, **self._kwargs) # Menjalankan fungsi steg_functions
            self.progress.emit(100) # Selesai
            self.result_ready.emit(result if isinstance(result, dict) else {"data": result})
        except Exception as e:
            self.error_occurred.emit(str(e))

class HLine(QFrame):
    """Widget garis pemisah horizontal sederhana"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("color: #334155; background: #334155; max-height: 1px;")