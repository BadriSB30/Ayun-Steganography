"""
styles.py - Stylesheet dan konstanta visual untuk aplikasi Steganography
"""

# Warna utama
COLORS = {
    "bg_dark": "#0A0E1A",
    "bg_panel": "#0F1525",
    "bg_card": "#141C30",
    "bg_input": "#0D1220",
    "accent_cyan": "#00D4FF",
    "accent_green": "#00FF9F",
    "accent_purple": "#7B2FFF",
    "accent_orange": "#FF6B35",
    "text_primary": "#E8F0FF",
    "text_secondary": "#8A9BC5",
    "text_dim": "#4A5A80",
    "border_glow": "#1E3060",
    "border_accent": "#00D4FF",
    "success": "#00FF9F",
    "error": "#FF4757",
    "warning": "#FFD700",
}

APP_STYLESHEET = """
/* === BASE === */
QMainWindow {
    background-color: #0A0E1A;
}

QWidget {
    background-color: #0A0E1A;
    color: #E8F0FF;
    font-family: 'Courier New', monospace;
    font-size: 13px;
}

/* === TITLE BAR AREA === */
QLabel#app_title {
    font-size: 26px;
    font-weight: bold;
    color: #00D4FF;
    letter-spacing: 6px;
    font-family: 'Courier New', monospace;
}

QLabel#app_subtitle {
    font-size: 11px;
    color: #4A5A80;
    letter-spacing: 3px;
}

/* === TAB WIDGET === */
QTabWidget::pane {
    background-color: #0F1525;
    border: 1px solid #1E3060;
    border-radius: 0px;
    border-top: 2px solid #00D4FF;
}

QTabBar::tab {
    background-color: #0A0E1A;
    color: #4A5A80;
    padding: 12px 32px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 3px;
    border: 1px solid #1E3060;
    border-bottom: none;
    margin-right: 2px;
    font-family: 'Courier New', monospace;
}

QTabBar::tab:selected {
    background-color: #0F1525;
    color: #00D4FF;
    border-top: 2px solid #00D4FF;
    border-left: 1px solid #1E3060;
    border-right: 1px solid #1E3060;
}

QTabBar::tab:hover:!selected {
    background-color: #111929;
    color: #8A9BC5;
}

/* === CARDS / GROUP BOXES === */
QGroupBox {
    background-color: #0F1525;
    border: 1px solid #1E3060;
    border-radius: 2px;
    margin-top: 20px;
    padding-top: 16px;
    font-size: 11px;
    font-weight: bold;
    color: #4A5A80;
    letter-spacing: 2px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 8px;
    color: #00D4FF;
    background-color: #0F1525;
    font-size: 10px;
    letter-spacing: 3px;
}

/* === BUTTONS === */
QPushButton {
    background-color: transparent;
    color: #00D4FF;
    border: 1px solid #00D4FF;
    border-radius: 1px;
    padding: 10px 24px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    font-family: 'Courier New', monospace;
}

QPushButton:hover {
    background-color: rgba(0, 212, 255, 0.10);
    color: #FFFFFF;
    border-color: #00D4FF;
}

QPushButton:pressed {
    background-color: rgba(0, 212, 255, 0.20);
}

QPushButton:disabled {
    color: #2A3A60;
    border-color: #1A2A40;
}

QPushButton#btn_primary {
    background-color: rgba(0, 212, 255, 0.08);
    color: #00D4FF;
    border: 1px solid #00D4FF;
    padding: 12px 32px;
    font-size: 12px;
    letter-spacing: 3px;
}

QPushButton#btn_primary:hover {
    background-color: rgba(0, 212, 255, 0.18);
    color: #FFFFFF;
}

QPushButton#btn_success {
    background-color: rgba(0, 255, 159, 0.08);
    color: #00FF9F;
    border: 1px solid #00FF9F;
    padding: 12px 32px;
    font-size: 12px;
    letter-spacing: 3px;
}

QPushButton#btn_success:hover {
    background-color: rgba(0, 255, 159, 0.18);
    color: #FFFFFF;
}

QPushButton#btn_danger {
    background-color: rgba(255, 71, 87, 0.08);
    color: #FF4757;
    border: 1px solid #FF4757;
    padding: 10px 24px;
}

QPushButton#btn_danger:hover {
    background-color: rgba(255, 71, 87, 0.18);
}

/* === TEXT INPUTS === */
QTextEdit, QLineEdit {
    background-color: #0D1220;
    color: #E8F0FF;
    border: 1px solid #1E3060;
    border-radius: 1px;
    padding: 10px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    selection-background-color: rgba(0, 212, 255, 0.25);
}

QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #00D4FF;
    background-color: #0F1728;
}

QTextEdit#output_area {
    background-color: #070B14;
    color: #00FF9F;
    border: 1px solid #0A2040;
    font-size: 13px;
    padding: 14px;
}

/* === LABELS === */
QLabel {
    color: #8A9BC5;
    background-color: transparent;
}

QLabel#section_label {
    color: #4A5A80;
    font-size: 10px;
    letter-spacing: 3px;
    font-weight: bold;
}

QLabel#status_label {
    font-size: 11px;
    letter-spacing: 1px;
    padding: 6px 12px;
}

QLabel#image_placeholder {
    color: #1E3060;
    font-size: 13px;
    border: 1px dashed #1E3060;
    background-color: #070B14;
}

/* === SCROLLBAR === */
QScrollBar:vertical {
    background-color: #0A0E1A;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #1E3060;
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00D4FF;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #0A0E1A;
    height: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #1E3060;
    border-radius: 3px;
}

/* === PROGRESS BAR === */
QProgressBar {
    background-color: #0D1220;
    border: 1px solid #1E3060;
    border-radius: 1px;
    height: 6px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00D4FF, stop:1 #7B2FFF);
    border-radius: 1px;
}

/* === SPINBOX === */
QSpinBox {
    background-color: #0D1220;
    color: #E8F0FF;
    border: 1px solid #1E3060;
    padding: 6px 10px;
    font-family: 'Courier New', monospace;
}

QSpinBox:focus {
    border-color: #00D4FF;
}

/* === SEPARATOR === */
QFrame[frameShape="4"] {
    color: #1E3060;
    height: 1px;
}

QFrame[frameShape="5"] {
    color: #1E3060;
    width: 1px;
}

/* === TOOLTIPS === */
QToolTip {
    background-color: #0F1525;
    color: #00D4FF;
    border: 1px solid #1E3060;
    padding: 6px 10px;
    font-size: 11px;
    font-family: 'Courier New', monospace;
}

/* === STATUSBAR === */
QStatusBar {
    background-color: #070B14;
    color: #4A5A80;
    border-top: 1px solid #1E3060;
    font-size: 11px;
    letter-spacing: 1px;
    font-family: 'Courier New', monospace;
}
"""

# Warna status
STATUS_COLORS = {
    "idle":    "#4A5A80",
    "success": "#00FF9F",
    "error":   "#FF4757",
    "warning": "#FFD700",
    "info":    "#00D4FF",
    "working": "#7B2FFF",
}
