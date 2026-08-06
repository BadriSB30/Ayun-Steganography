"""
styles.py - Stylesheet dan konstanta visual (Dark Cyber/Forensic Theme)
"""

# Palet warna bernuansa Cyber/Forensik (Nyaman untuk mode gelap)
COLORS = {
    "bg_main": "#0F172A",        # Latar utama: Slate 900 (Gelap namun elegan, tidak murni hitam)
    "bg_panel": "#1E293B",       # Latar panel/kartu: Slate 800
    "bg_input": "#0B1120",       # Latar input: Sangat gelap agar teks menonjol
    "accent_primary": "#0EA5E9", # Aksen utama: Neon Cyan (Kesan futuristik)
    "accent_hover": "#38BDF8",   # Aksen saat di-hover (Lebih terang)
    "text_primary": "#F8FAFC",   # Teks utama: Putih bersih
    "text_secondary": "#CBD5E1", # Teks sekunder: Abu-abu terang
    "text_dim": "#64748B",       # Teks redup untuk info tambahan
    "border_light": "#334155",   # Garis batas gelap
    "border_active": "#0EA5E9",  # Garis batas aktif (Cyan)
    "success": "#10B981",        # Hijau Emerald (Untuk status sukses/aman)
    "error": "#EF4444",          # Merah tajam (Untuk status gagal/error)
    "warning": "#F59E0B",        # Oranye/Kuning (Peringatan)
}

# CSS (Stylesheet) khusus untuk mempercantik widget PyQt5
APP_STYLESHEET = """
/* === PENGATURAN DASAR === */
QMainWindow, QWidget {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}

/* === AREA JUDUL (HEADER) === */
QLabel#app_title {
    font-size: 24px;
    font-weight: 900;
    color: #0EA5E9; /* Teks judul warna Cyan */
    letter-spacing: 3px;
}
QLabel#app_subtitle {
    font-size: 11px;
    color: #94A3B8;
    letter-spacing: 2px;
    font-weight: 600;
}

/* === PANEL TAB (MENU ATAS) === */
QTabWidget::pane {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    top: -1px; /* Menggabungkan tab dengan panel */
}
QTabBar::tab {
    background-color: #0F172A;
    color: #64748B;
    padding: 12px 24px;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid #334155;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background-color: #1E293B;
    color: #0EA5E9;
    border-top: 3px solid #0EA5E9; /* Indikator tab aktif */
}
QTabBar::tab:hover:!selected {
    background-color: #1E293B;
    color: #CBD5E1;
}

/* === KOTAK GRUP (PANEL INFORMASI) === */
QGroupBox {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 24px;
    padding-top: 16px;
    font-size: 12px;
    font-weight: bold;
    color: #94A3B8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    color: #0EA5E9;
    background-color: #1E293B;
    border-radius: 4px;
}

/* === TOMBOL (BUTTONS) === */
QPushButton {
    background-color: #1E293B;
    color: #0EA5E9;
    border: 1px solid #0EA5E9;
    border-radius: 6px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: rgba(14, 165, 233, 0.1); /* Efek glow transparan */
    color: #38BDF8;
}
QPushButton:pressed {
    background-color: rgba(14, 165, 233, 0.2);
}
QPushButton:disabled {
    color: #475569;
    border-color: #334155;
    background-color: #0F172A;
}
QPushButton#btn_primary {
    background-color: #0EA5E9;
    color: #0F172A; /* Teks gelap di atas tombol terang */
    border: none;
}
QPushButton#btn_primary:hover {
    background-color: #38BDF8;
}
QPushButton#btn_success {
    background-color: #10B981;
    color: #0F172A;
    border: none;
    font-weight: 800;
}
QPushButton#btn_success:hover {
    background-color: #34D399;
}
QPushButton#btn_danger {
    background-color: transparent;
    color: #EF4444;
    border: 1px solid #EF4444;
}
QPushButton#btn_danger:hover {
    background-color: rgba(239, 68, 68, 0.1);
}

/* === AREA INPUT TEKS & LOG === */
QTextEdit, QLineEdit {
    background-color: #0B1120;
    color: #10B981; /* Teks hijau ala terminal hacker */
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 12px;
    font-family: 'Consolas', 'Courier New', monospace; /* Font ala kode/terminal */
    font-size: 13px;
    selection-background-color: #0EA5E9;
    selection-color: #0F172A;
}
QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #0EA5E9; /* Menyala saat diklik */
}
QTextEdit#output_area {
    background-color: #0B1120;
    color: #0EA5E9; /* Teks log berwarna Cyan */
    border: 1px solid #334155;
}

/* === LABEL TEKS === */
QLabel {
    color: #CBD5E1;
    background-color: transparent;
}
QLabel#section_label {
    color: #F8FAFC;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 800;
}
QLabel#image_placeholder {
    color: #64748B;
    font-weight: 700;
    border: 2px dashed #334155;
    background-color: #0B1120;
    border-radius: 8px;
}

/* === SCROLLBAR (Batang Gulir) === */
QScrollBar:vertical {
    background-color: #0F172A;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

/* === PROGRESS BAR (Bilah Kemajuan) === */
QProgressBar {
    background-color: #0B1120;
    border: 1px solid #334155;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #0EA5E9;
    border-radius: 3px;
}

/* === STATUS BAR (Bawah Aplikasi) === */
QStatusBar {
    background-color: #0B1120;
    color: #64748B;
    border-top: 1px solid #334155;
    font-size: 11px;
    font-family: 'Consolas', monospace;
}
"""

# Warna indikator untuk widget StatusBar
STATUS_COLORS = {
    "idle":    "#64748B", # Abu-abu
    "success": "#10B981", # Hijau
    "error":   "#EF4444", # Merah
    "warning": "#F59E0B", # Kuning
    "info":    "#0EA5E9", # Cyan
    "working": "#8B5CF6", # Ungu
}