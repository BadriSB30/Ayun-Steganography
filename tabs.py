"""
tabs.py - Panel tab untuk operasi Embed, Extract, dan Forensik
Validasi ketat: Fitur Analisis Forensik & Komparasi Piksel eksklusif untuk format Gambar.
Log aktivitas sistem diperbarui agar lebih informatif dan detail.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFileDialog, QGroupBox, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer

from widgets import ImagePreviewWidget, StatusBar, InfoPanel, WorkerThread, HLine
import steg_functions as sf

class EmbedTab(QWidget):
    """TAB 1: Fitur untuk INJEKSI DATA (Mendukung Gambar, Audio, Video)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._source_path = None
        self._output_path = None
        self._worker = None
        self._setup_ui()

    def _setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(24)

        # ── KOLOM 1 (KIRI) ──
        left = QVBoxLayout()
        left.setSpacing(12)
        lbl_img = QLabel("FILE SUMBER (CARRIER)")
        lbl_img.setObjectName("section_label")
        left.addWidget(lbl_img, 0)

        self.preview_in = ImagePreviewWidget("Tarik & Lepas\nFile Multimedia")
        self.preview_in.image_dropped.connect(self._load_file)
        left.addWidget(self.preview_in, 1)

        btn_row = QHBoxLayout()
        self.btn_browse = QPushButton("Pilih File")
        self.btn_browse.setObjectName("btn_primary")
        self.btn_browse.clicked.connect(self._browse_file)
        self.btn_clear = QPushButton("Hapus")
        self.btn_clear.setObjectName("btn_danger")
        self.btn_clear.clicked.connect(self._clear_file)
        btn_row.addWidget(self.btn_browse, 1)
        btn_row.addWidget(self.btn_clear, 0)
        
        btn_container = QWidget()
        btn_container.setLayout(btn_row)
        left.addWidget(btn_container, 0)

        img_group = QGroupBox("Metrik File")
        ig_layout = QVBoxLayout(img_group)
        self.info_panel = InfoPanel()
        ig_layout.addWidget(self.info_panel)
        left.addWidget(img_group, 0)

        # ── KOLOM 2 (TENGAH) ──
        mid = QVBoxLayout()
        mid.setSpacing(12)
        lbl_txt = QLabel("DATA INJEKSI (PAYLOAD)")
        lbl_txt.setObjectName("section_label")
        mid.addWidget(lbl_txt, 0)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("> Masukkan string payload di sini...\n> Gambar = LSB | Video/Audio = EOF Injection")
        self.text_input.textChanged.connect(self._update_char_count)
        mid.addWidget(self.text_input, 1)

        self.lbl_chars = QLabel("0 Bytes")
        self.lbl_chars.setAlignment(Qt.AlignRight)
        mid.addWidget(self.lbl_chars, 0)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        mid.addWidget(self.progress, 0)

        self.status_bar = StatusBar()
        mid.addWidget(self.status_bar, 0)

        self.btn_embed = QPushButton("JALANKAN INJEKSI")
        self.btn_embed.setObjectName("btn_success")
        self.btn_embed.setMinimumHeight(44)
        self.btn_embed.clicked.connect(self._run_embed)
        mid.addWidget(self.btn_embed, 0)

        # ── KOLOM 3 (KANAN) ──
        right = QVBoxLayout()
        right.setSpacing(12)
        lbl_out = QLabel("OUTPUT STEGANO")
        lbl_out.setObjectName("section_label")
        right.addWidget(lbl_out, 0)

        self.preview_out = ImagePreviewWidget("Pratinjau File\nTerenkripsi")
        right.addWidget(self.preview_out, 1)

        self.btn_save = QPushButton("Simpan File Hasil")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_output)
        right.addWidget(self.btn_save, 0)

        log_group = QGroupBox("Log Aktivitas Sistem")
        log_layout = QVBoxLayout(log_group)
        self.log_area = QTextEdit()
        self.log_area.setObjectName("output_area")
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        right.addWidget(log_group, 0)

        root.addLayout(left, 1)
        root.addLayout(mid, 1)
        root.addLayout(right, 1)

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Pilih Multimedia", "", "Multimedia (*.png *.jpg *.jpeg *.bmp *.webp *.mp3 *.wav *.mp4 *.mkv *.avi)")
        if path: self._load_file(path)

    def _load_file(self, path: str):
        self._source_path = path
        self.preview_in.set_image(path)
        try:
            info = sf.get_multimedia_info(path)
            self.info_panel.set_info({
                "File": info["filename"],
                "Tipe": info["type"],
                "Size": info["file_size"],
                "Format": info["format"],
                "Kapasitas": f"{info['max_chars']:,} ch" if info["is_image"] else "Tak Terbatas (EOF)",
            })
            self._update_char_count()
            self.status_bar.set_status("info", f"Carrier: {info['filename']}")
            
            # Evaluasi string kapasitas terlebih dahulu agar terhindar dari error f-string
            if info["is_image"]:
                cap_text = f"Maksimal {info['max_chars']:,} Karakter (LSB)"
            else:
                cap_text = "Tanpa Batas (EOF)"

            self._log(f"[FILE LOADED] Berhasil memuat {info['type']}")
            self._log(f" ├─ Nama Berkas : {info['filename']}")
            self._log(f" ├─ Ukuran File : {info['file_size']}")
            self._log(f" └─ Kapasitas   : {cap_text}")
        except Exception as e:
            self._log(f"[FATAL ERROR] Gagal membaca metadata: {e}", error=True)

    def _clear_file(self):
        self._source_path = None
        self.preview_in.clear_image()
        self.info_panel.clear()
        self.lbl_chars.setText("0 Bytes")
        self.status_bar.set_status("idle", "STANDBY")
        self._log("[RESET] Area kerja dibersihkan.")

    def _update_char_count(self):
        text = self.text_input.toPlainText()
        self.lbl_chars.setText(f"{len(text):,} Bytes")

    def _run_embed(self):
        if not self._source_path:
            self.status_bar.set_status("error", "Carrier belum dipilih!")
            self._log("[WARNING] Proses dibatalkan: File carrier belum dipilih.", error=True)
            return
            
        text = self.text_input.toPlainText()
        if not text.strip():
            self.status_bar.set_status("error", "Payload kosong!")
            self._log("[WARNING] Proses dibatalkan: Teks payload masih kosong.", error=True)
            return

        info = sf.get_multimedia_info(self._source_path)
        base, ext = os.path.splitext(self._source_path)
        
        self.btn_embed.setEnabled(False)
        self.progress.setValue(10)

        if info.get("is_image", True):
            self._output_path = base + "_steg.png"
            method_desc = "LSB (Least Significant Bit) pada Piksel Gambar"
            self.status_bar.set_status("working", "Memproses LSB (Gambar)...")
            self._worker = WorkerThread(sf.embed_text_lsb, self._source_path, text, self._output_path)
        else:
            self._output_path = base + "_steg" + ext
            method_desc = f"EOF (End of File) Injection pada {info['type']}"
            self.status_bar.set_status("working", f"Memproses EOF ({info['type']})...")
            self._worker = WorkerThread(sf.embed_eof_multimedia, self._source_path, text, self._output_path)

        self._log(f"[INIT] Memulai proses penyembunyian data...")
        self._log(f" ├─ Metode Injeksi : {method_desc}")
        self._log(f" ├─ Ukuran Payload : {len(text):,} Karakter / Bytes")
        self._log(f" └─ Target Output  : {os.path.basename(self._output_path)}")

        self._worker.result_ready.connect(self._on_embed_done)
        self._worker.error_occurred.connect(self._on_embed_error)
        self._worker.progress.connect(self.progress.setValue)
        self._worker.start()

    def _on_embed_done(self, result: dict):
        self.btn_embed.setEnabled(True)
        if result.get("status") == "success":
            self.progress.setValue(100)
            self.status_bar.set_status("success", "Injeksi Berhasil!")
            self.preview_out.set_image(self._output_path)
            self.btn_save.setEnabled(True)
            
            self._log(f"[SUCCESS] Injeksi data berhasil diselesaikan!")
            self._log(f" ├─ Tipe Media    : {result['image_info']['type']}")
            self._log(f" ├─ Karakter Hidden: {result.get('chars_hidden', 0):,} Bytes")
            self._log(f" └─ Status File   : Siap untuk diekspor/disimpan.")
        else:
            self._on_embed_error(result.get("message", "Error tidak diketahui"))
        QTimer.singleShot(3000, lambda: self.progress.setValue(0))

    def _on_embed_error(self, error_msg: str):
        self.btn_embed.setEnabled(True)
        self.progress.setValue(0)
        self.status_bar.set_status("error", "Injeksi Gagal")
        self._log(f"[ERROR FAILED] {error_msg}", error=True)

    def _save_output(self):
        if not self._output_path or not os.path.exists(self._output_path): return
        ext = os.path.splitext(self._output_path)[1]
        path, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", f"File Hasil (*{ext})")
        if path:
            if not path.lower().endswith(ext): path += ext
            import shutil
            shutil.copy2(self._output_path, path)
            self.status_bar.set_status("success", "Tersimpan")
            self._log(f"[EXPORT] Berkas berhasil disimpan ke direktori:")
            self._log(f" └─ {path}")

    def _log(self, message: str, error: bool = False):
        color = "#EF4444" if error else "#0EA5E9"
        self.log_area.append(f'<span style="color:{color}; font-family:Consolas;">{message}</span>')


class ExtractTab(QWidget):
    """TAB 2: Fitur untuk EKSTRAKSI DATA (Mendukung Gambar, Audio, Video)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._image_path = None
        self._setup_ui()

    def _setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        
        left = QVBoxLayout()
        self.preview = ImagePreviewWidget("Pilih File\nUntuk Ekstraksi")
        self.preview.image_dropped.connect(self._load_file)
        left.addWidget(self.preview)
        
        btn_browse = QPushButton("Pilih File")
        btn_browse.clicked.connect(self._browse_file)
        left.addWidget(btn_browse)

        self.info_panel = InfoPanel()
        left.addWidget(self.info_panel)

        right = QVBoxLayout()
        self.status_bar = StatusBar()
        right.addWidget(self.status_bar)
        
        self.btn_extract = QPushButton("JALANKAN EKSTRAKSI DATA")
        self.btn_extract.setObjectName("btn_success")
        self.btn_extract.setMinimumHeight(44)
        self.btn_extract.clicked.connect(self._run_extract)
        right.addWidget(self.btn_extract)

        self.output_area = QTextEdit()
        self.output_area.setObjectName("output_area")
        right.addWidget(self.output_area)

        analyze_group = QGroupBox("Inspeksi Forensik Chi-Square (Khusus Gambar)")
        al_layout = QVBoxLayout(analyze_group)
        self.analyze_area = QTextEdit()
        self.analyze_area.setObjectName("output_area")
        self.analyze_area.setReadOnly(True)
        self.analyze_area.setFixedHeight(75)
        al_layout.addWidget(self.analyze_area)
        self.btn_analyze = QPushButton("Pemindaian Chi-Square")
        self.btn_analyze.clicked.connect(self._run_analyze)
        al_layout.addWidget(self.btn_analyze)
        right.addWidget(analyze_group)

        root.addLayout(left, 1)
        root.addLayout(right, 1)

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Pilih File", "", "Semua File (*.*)")
        if path: self._load_file(path)

    def _load_file(self, path: str):
        self._image_path = path
        self.preview.set_image(path)
        info = sf.get_multimedia_info(path)
        self.info_panel.set_info({"File": info["filename"], "Tipe": info["type"], "Size": info["file_size"]})
        self.analyze_area.clear()

    def _run_extract(self):
        if not self._image_path: return
        self.btn_extract.setEnabled(False)
        info = sf.get_multimedia_info(self._image_path)
        
        if info.get("is_image", True):
            self.status_bar.set_status("working", "Ekstraksi LSB...")
            self._worker = WorkerThread(sf.extract_text_lsb, self._image_path)
        else:
            self.status_bar.set_status("working", "Mencari Marker EOF...")
            self._worker = WorkerThread(sf.extract_eof_multimedia, self._image_path)
            
        self._worker.result_ready.connect(self._on_extract_done)
        self._worker.start()

    def _on_extract_done(self, result: dict):
        self.btn_extract.setEnabled(True)
        if result.get("status") == "success" and result.get("text"):
            self.output_area.setPlainText(result["text"])
            self.status_bar.set_status("success", "Payload Ditemukan!")
        else:
            self.output_area.setPlainText(result.get("message", "Gagal menemukan anomali."))
            self.status_bar.set_status("warning", "Data Kosong")

    def _run_analyze(self):
        if not self._image_path: return
        info = sf.get_multimedia_info(self._image_path)
        if not info.get("is_image", False):
            self.analyze_area.setPlainText("[!] PERINGATAN: Analisis Chi-Square hanya dapat dilakukan pada file Gambar (PNG/JPG/WEBP).")
            return

        self._worker = WorkerThread(sf.analyze_image_lsb, self._image_path)
        self._worker.result_ready.connect(self._on_analyze_done)
        self._worker.start()

    def _on_analyze_done(self, result: dict):
        lines = [
            f"> Chi2 Stat   : {result['chi2_stat']:.2f}",
            f"> LSB Ratio   : {result['lsb_ratio']:.4f}",
            f"> Status      : {result['verdict']}",
        ]
        self.analyze_area.setPlainText("\n".join(lines))


class CompareTab(QWidget):
    """TAB 3: Fitur Analisis Forensik & Komparasi Piksel (EKSKLUSIF KHUSUS GAMBAR)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._path_a = None
        self._path_b = None
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        lbl = QLabel("INSPEKSI FORENSIK & KOMPARASI PIKSEL (KHUSUS FORMAT GAMBAR)")
        lbl.setObjectName("section_label")
        root.addWidget(lbl, 0)

        previews = QHBoxLayout()
        previews.setSpacing(20)

        left_col = QVBoxLayout()
        lbl_a = QLabel("File Referensi (Original)")
        lbl_a.setStyleSheet("color: #0EA5E9; font-weight: bold;")
        left_col.addWidget(lbl_a, 0)
        self.preview_a = ImagePreviewWidget("Gambar A (Wajib Format Gambar)")
        self.preview_a.image_dropped.connect(lambda p: self._load_img("a", p))
        left_col.addWidget(self.preview_a, 1)
        btn_a = QPushButton("Pilih Gambar Original")
        btn_a.clicked.connect(lambda: self._browse("a"))
        left_col.addWidget(btn_a, 0)

        right_col = QVBoxLayout()
        lbl_b = QLabel("File Target (Stegano)")
        lbl_b.setStyleSheet("color: #10B981; font-weight: bold;")
        right_col.addWidget(lbl_b, 0)
        self.preview_b = ImagePreviewWidget("Gambar B (Wajib Format Gambar)")
        self.preview_b.image_dropped.connect(lambda p: self._load_img("b", p))
        right_col.addWidget(self.preview_b, 1)
        btn_b = QPushButton("Pilih Gambar Target")
        btn_b.clicked.connect(lambda: self._browse("b"))
        right_col.addWidget(btn_b, 0)

        previews.addLayout(left_col)
        previews.addLayout(right_col)
        root.addLayout(previews, 1)

        self.btn_compare = QPushButton("JALANKAN KOMPARASI FORENSIK (PSNR & MSE)")
        self.btn_compare.setObjectName("btn_primary")
        self.btn_compare.setMinimumHeight(44)
        self.btn_compare.clicked.connect(self._run_compare)
        root.addWidget(self.btn_compare, 0)

        result_group = QGroupBox("Log Hasil Analisis Forensik Pixel")
        rg_layout = QVBoxLayout(result_group)
        self.result_area = QTextEdit()
        self.result_area.setObjectName("output_area")
        self.result_area.setReadOnly(True)
        self.result_area.setMinimumHeight(100)
        rg_layout.addWidget(self.result_area)
        root.addWidget(result_group, 0)

    def _browse(self, which: str):
        path, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)")
        if path: 
            self._load_img(which, path)

    def _load_img(self, which: str, path: str):
        info = sf.get_multimedia_info(path)
        if not info.get("is_image", False):
            self.result_area.setPlainText(
                f"[!] PERINGATAN PENOLAKAN BERKAS:\n"
                f"File '{info['filename']}' berformat ({info['type']}).\n"
                f"Fitur Analisis Forensik & Komparasi Piksel HANYA DAPAT MEMPROSES FILE GAMBAR!"
            )
            return

        if which == "a":
            self._path_a = path
            self.preview_a.set_image(path)
        else:
            self._path_b = path
            self.preview_b.set_image(path)
        self.result_area.clear()

    def _run_compare(self):
        if not self._path_a or not self._path_b:
            self.result_area.setPlainText("[!] Harap masukkan file gambar referensi dan file target terlebih dahulu.")
            return
        try:
            result = sf.compare_images(self._path_a, self._path_b)
            if "error" in result:
                self.result_area.setPlainText(f"[FATAL] ERROR: {result['error']}")
                return

            lines = [
                f"> MSE (Mean Squared Error) : {result['mse']:.6f}",
                f"> PSNR Ratio               : {result['psnr']:.2f} dB",
                f"> Piksel Termanipulasi     : {result['changed_pixels']:,} dari {result['total_pixels']:,} total piksel",
                f"> Tingkat Perubahan File   : {result['change_percent']}%",
                f"> Estimasi Kualitas        : {result['quality']}",
            ]
            self.result_area.setPlainText("\n".join(lines))
        except Exception as e:
            self.result_area.setPlainText(f"[FATAL] ERROR: {e}")