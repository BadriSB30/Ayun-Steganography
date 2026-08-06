"""
main.py - Entry point aplikasi Steganography Desktop
File ini adalah inti yang dijalankan pertama kali untuk memuat antarmuka (UI).
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTabWidget, QStatusBar, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from styles import APP_STYLESHEET
from tabs import EmbedTab, ExtractTab, CompareTab

def resource_path(relative: str) -> str:
    """
    Fungsi untuk mencari letak aset (seperti ikon).
    Penting jika aplikasi di-build menjadi file .exe menggunakan PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

class AppHeader(QWidget):
    """Widget khusus untuk bagian atas aplikasi (Judul & Logo)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setStyleSheet("background-color: #1E293B;") # Warna panel header gelap

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 8, 24, 8)
        layout.setSpacing(16)

        # Ikon dekoratif bergaya cyber
        icon_lbl = QLabel("◈")
        icon_lbl.setStyleSheet("color: #0EA5E9; font-size: 36px; background: transparent;")
        icon_lbl.setFixedWidth(36)
        layout.addWidget(icon_lbl)

        # Kolom untuk Judul & Subjudul
        title_col = QVBoxLayout()
        title_col.setSpacing(0)

        title = QLabel("STEGANOGRAPHY")
        title.setObjectName("app_title")
        title_col.addWidget(title)

        subtitle = QLabel("Data Hiding System • LSB Method")
        subtitle.setObjectName("app_subtitle")
        title_col.addWidget(subtitle)

        layout.addLayout(title_col)
        layout.addStretch() # Memberikan ruang kosong fleksibel di tengah

        # Versi aplikasi di pojok kanan
        ver = QLabel("Steganography - v2.0.0 (Ayun_0o0)")
        ver.setStyleSheet("color: #64748B; font-family: 'Consolas'; background: transparent;")
        layout.addWidget(ver)

        # Garis bawah header (Border Bottom)
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setGeometry(0, 79, 9999, 1)
        sep.setStyleSheet("background-color: #334155;")

class MainWindow(QMainWindow):
    """Jendela utama (Main Window) yang menampung semua tab dan widget"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography - Cyber Tool")
        self.setMinimumSize(1100, 720) # Ukuran minimum agar UI tidak rusak
        self.resize(1280, 800)         # Ukuran default saat dibuka
        self.setStyleSheet(APP_STYLESHEET) # Menerapkan tema dari styles.py

        # Memasang ikon aplikasi jika file-nya ada
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._build_ui()
        self._setup_statusbar()

    def _build_ui(self):
        """Membangun layout utama: Header + Tab Widget"""
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = AppHeader()
        root.addWidget(header)

        # Container untuk Tab agar memiliki margin dari layar utama
        tab_container = QWidget()
        tab_layout = QVBoxLayout(tab_container)
        tab_layout.setContentsMargins(20, 20, 20, 20)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Inisialisasi ketiga menu utama aplikasi
        self.tab_embed   = EmbedTab()
        self.tab_extract = ExtractTab()
        self.tab_compare = CompareTab()

        self.tabs.addTab(self.tab_embed,   "⚡ Injeksi Data")
        self.tabs.addTab(self.tab_extract, "🔍 Ekstraksi Pesan")
        self.tabs.addTab(self.tab_compare, "📊 Analisis Forensik")

        tab_layout.addWidget(self.tabs)
        root.addWidget(tab_container, 1)

    def _setup_statusbar(self):
        """Membuat baris status kecil di pojok bawah aplikasi"""
        status = QStatusBar()
        status.setFixedHeight(30)
        lbl = QLabel(" ◈ Steganography Workspace • Koneksi Sistem: Aman")
        lbl.setStyleSheet("color: #64748B; font-weight: bold;")
        status.addWidget(lbl)
        self.setStatusBar(status)

def main():
    # Menangani layar resolusi tinggi (High-DPI / 4K monitors)
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Steganography")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()