"""
widgets.py - Widget kustom PyQt5 untuk aplikasi Steganography
"""

import os
from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QImage, QFont, QPainter, QColor, QPen

from styles import STATUS_COLORS, COLORS


# ─────────────────────────────────────────────
#   IMAGE PREVIEW WIDGET
# ─────────────────────────────────────────────

class ImagePreviewWidget(QLabel):
    """Widget untuk menampilkan preview gambar dengan drop support."""

    image_dropped = pyqtSignal(str)

    def __init__(self, placeholder_text="DRAG & DROP\nATAU PILIH GAMBAR", parent=None):
        super().__init__(parent)
        self._placeholder = placeholder_text
        self._image_path = None

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(320, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setObjectName("image_placeholder")
        self._show_placeholder()

    def _show_placeholder(self):
        self.setText(f"[ {self._placeholder} ]")
        self.setStyleSheet("""
            QLabel {
                color: #1E3060;
                font-size: 12px;
                letter-spacing: 2px;
                border: 1px dashed #1E3060;
                background-color: #070B14;
                font-family: 'Courier New', monospace;
            }
        """)

    def set_image(self, image_path: str):
        """Tampilkan gambar dari path."""
        self._image_path = image_path
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self._show_placeholder()
            return
        scaled = pixmap.scaled(
            self.width() - 8, self.height() - 8,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setPixmap(scaled)
        self.setStyleSheet("""
            QLabel {
                border: 1px solid #00D4FF;
                background-color: #070B14;
                padding: 4px;
            }
        """)

    def set_image_from_bytes(self, img_bytes: bytes):
        """Tampilkan gambar dari bytes."""
        pixmap = QPixmap()
        pixmap.loadFromData(img_bytes)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.width() - 8, self.height() - 8,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
            self.setStyleSheet("""
                QLabel {
                    border: 1px solid #00D4FF;
                    background-color: #070B14;
                    padding: 4px;
                }
            """)

    def clear_image(self):
        self._image_path = None
        self.clear()
        self._show_placeholder()

    @property
    def image_path(self):
        return self._image_path

    # Drag & Drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and _is_image_file(urls[0].toLocalFile()):
                event.acceptProposedAction()
                self.setStyleSheet("""
                    QLabel {
                        border: 1px dashed #00D4FF;
                        background-color: rgba(0,212,255,0.05);
                        font-family: 'Courier New', monospace;
                    }
                """)

    def dragLeaveEvent(self, event):
        if self._image_path:
            self.set_image(self._image_path)
        else:
            self._show_placeholder()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if _is_image_file(path):
                self.set_image(path)
                self.image_dropped.emit(path)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._image_path:
            self.set_image(self._image_path)


def _is_image_file(path: str) -> bool:
    return path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"))


# ─────────────────────────────────────────────
#   STATUS INDICATOR WIDGET
# ─────────────────────────────────────────────

class StatusBar(QWidget):
    """Widget status bar kustom dengan indikator warna."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 4, 12, 4)
        self._layout.setSpacing(10)

        self._dot = QLabel("●")
        self._dot.setFixedWidth(16)

        self._label = QLabel("SIAP")
        self._label.setObjectName("status_label")

        self._layout.addWidget(self._dot)
        self._layout.addWidget(self._label)
        self._layout.addStretch()

        self.setFixedHeight(30)
        self.set_status("idle", "SIAP")

    def set_status(self, level: str, message: str):
        color = STATUS_COLORS.get(level, STATUS_COLORS["idle"])
        self._dot.setStyleSheet(f"color: {color}; font-size: 14px;")
        self._label.setStyleSheet(
            f"color: {color}; font-size: 11px; letter-spacing: 1px;"
            f" font-family: 'Courier New', monospace;"
        )
        self._label.setText(message.upper())


# ─────────────────────────────────────────────
#   INFO PANEL WIDGET
# ─────────────────────────────────────────────

class InfoPanel(QFrame):
    """Panel informasi gambar dengan layout grid."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        self._rows: dict[str, QLabel] = {}
        self.setStyleSheet("background: transparent;")

    def set_info(self, data: dict):
        """Update atau tambah baris informasi."""
        # Bersihkan widget lama
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._rows.clear()

        for key, value in data.items():
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            hl = QHBoxLayout(row)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(8)

            key_label = QLabel(f"{key}:")
            key_label.setFixedWidth(130)
            key_label.setStyleSheet(
                "color: #4A5A80; font-size: 10px; letter-spacing: 1px;"
                " font-family: 'Courier New', monospace;"
            )

            val_label = QLabel(str(value))
            val_label.setStyleSheet(
                "color: #8A9BC5; font-size: 11px;"
                " font-family: 'Courier New', monospace;"
            )
            val_label.setWordWrap(True)

            hl.addWidget(key_label)
            hl.addWidget(val_label, 1)
            self._layout.addWidget(row)
            self._rows[key] = val_label

    def clear(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._rows.clear()


# ─────────────────────────────────────────────
#   WORKER THREAD
# ─────────────────────────────────────────────

class WorkerThread(QThread):
    """Thread untuk menjalankan operasi berat tanpa memblokir UI."""

    result_ready  = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress      = pyqtSignal(int)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._func   = func
        self._args   = args
        self._kwargs = kwargs

    def run(self):
        try:
            self.progress.emit(30)
            result = self._func(*self._args, **self._kwargs)
            self.progress.emit(100)
            self.result_ready.emit(result if isinstance(result, dict) else {"data": result})
        except Exception as e:
            self.error_occurred.emit(str(e))


# ─────────────────────────────────────────────
#   HORIZONTAL SEPARATOR
# ─────────────────────────────────────────────

class HLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("color: #1E3060; background: #1E3060; max-height: 1px;")


class VLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("color: #1E3060; background: #1E3060; max-width: 1px;")
