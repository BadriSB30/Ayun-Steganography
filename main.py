"""
main.py - Entry point aplikasi Steganography Desktop
Sistem untuk menyembunyikan dan membaca teks tersembunyi di dalam gambar.
"""

import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTabWidget, QStatusBar, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

from styles import APP_STYLESHEET, COLORS
from tabs import EmbedTab, ExtractTab, CompareTab


# ─────────────────────────────────────────────
#   HEADER WIDGET
# ─────────────────────────────────────────────

class AppHeader(QWidget):
    """Header atas aplikasi dengan judul dan dekorasi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setStyleSheet(f"background-color: {COLORS['bg_dark']};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 8, 24, 8)
        layout.setSpacing(16)

        # Ikon / dekorasi kiri
        icon_lbl = QLabel("◈")
        icon_lbl.setStyleSheet(
            f"color: {COLORS['accent_cyan']}; font-size: 28px; background: transparent;"
        )
        icon_lbl.setFixedWidth(36)
        layout.addWidget(icon_lbl)

        # Judul
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        title = QLabel("STEGANOGRAPHY")
        title.setObjectName("app_title")
        title_col.addWidget(title)

        subtitle = QLabel("SISTEM PENYEMBUNYIAN TEKS DALAM GAMBAR  ·  LSB METHOD")
        subtitle.setObjectName("app_subtitle")
        title_col.addWidget(subtitle)

        layout.addLayout(title_col)
        layout.addStretch()

        # Badge versi
        ver = QLabel("v1.0")
        ver.setStyleSheet(
            f"color: {COLORS['text_dim']}; font-size: 10px;"
            f" letter-spacing: 2px; background: transparent;"
            f" font-family: 'Courier New', monospace;"
        )
        layout.addWidget(ver)

        # Separator bawah
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setGeometry(0, 78, 9999, 1)
        sep.setStyleSheet(f"background-color: {COLORS['border_glow']};")


# ─────────────────────────────────────────────
#   MAIN WINDOW
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    """Jendela utama aplikasi Steganography."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography — Sembunyikan Teks di Dalam Foto")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        # Stylesheet global
        self.setStyleSheet(APP_STYLESHEET)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._build_ui()
        self._setup_statusbar()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = AppHeader()
        root.addWidget(header)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_embed   = EmbedTab()
        self.tab_extract = ExtractTab()
        self.tab_compare = CompareTab()

        self.tabs.addTab(self.tab_embed,   "  ⚡  SEMBUNYIKAN TEKS  ")
        self.tabs.addTab(self.tab_extract, "  🔍  BACA PESAN  ")
        self.tabs.addTab(self.tab_compare, "  📊  BANDINGKAN  ")

        root.addWidget(self.tabs, 1)

    def _setup_statusbar(self):
        status = QStatusBar()
        status.setFixedHeight(24)

        lbl = QLabel(
            "  ◈ Steganography Desktop  ·  "
            "Metode: LSB (Least Significant Bit)  ·  "
            "Format output: PNG"
        )
        lbl.setStyleSheet(
            f"color: {COLORS['text_dim']}; font-size: 10px;"
            f" letter-spacing: 1px; background: transparent;"
            f" font-family: 'Courier New', monospace;"
        )
        status.addWidget(lbl)
        self.setStatusBar(status)


# ─────────────────────────────────────────────
#   ENTRY POINT
# ─────────────────────────────────────────────

def main():
    # Hindari masalah DPI pada layar HiDPI
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Steganography")
    app.setOrganizationName("StegApp")

    # Set application-wide icon (taskbar, dock, dll)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Palette gelap
    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor(COLORS["bg_dark"]))
    palette.setColor(QPalette.WindowText,      QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.Base,            QColor(COLORS["bg_input"]))
    palette.setColor(QPalette.AlternateBase,   QColor(COLORS["bg_panel"]))
    palette.setColor(QPalette.ToolTipBase,     QColor(COLORS["bg_panel"]))
    palette.setColor(QPalette.ToolTipText,     QColor(COLORS["accent_cyan"]))
    palette.setColor(QPalette.Text,            QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.Button,          QColor(COLORS["bg_panel"]))
    palette.setColor(QPalette.ButtonText,      QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.Highlight,       QColor(COLORS["accent_cyan"]))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS["bg_dark"]))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()