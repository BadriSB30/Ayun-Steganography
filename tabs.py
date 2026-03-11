"""
tabs.py - Panel tab untuk operasi Embed dan Extract steganography
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFileDialog, QGroupBox, QProgressBar,
    QSplitter, QSpinBox, QCheckBox, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from widgets import ImagePreviewWidget, StatusBar, InfoPanel, WorkerThread, HLine
import steg_functions as sf


# ─────────────────────────────────────────────
#   TAB EMBED (SEMBUNYIKAN TEKS)
# ─────────────────────────────────────────────

class EmbedTab(QWidget):
    """Tab untuk menyembunyikan teks ke dalam gambar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source_path = None
        self._output_path = None
        self._worker = None
        self._setup_ui()

    def _setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ── KOLOM KIRI: Input gambar ──
        left = QVBoxLayout()
        left.setSpacing(10)

        lbl_img = QLabel("[ GAMBAR SUMBER ]")
        lbl_img.setObjectName("section_label")
        left.addWidget(lbl_img)

        self.preview_in = ImagePreviewWidget("DRAG & DROP\nATAU PILIH GAMBAR")
        self.preview_in.image_dropped.connect(self._on_image_dropped)
        left.addWidget(self.preview_in, 1)

        # Tombol pilih gambar
        btn_row = QHBoxLayout()
        self.btn_browse = QPushButton("◈  PILIH GAMBAR")
        self.btn_browse.setObjectName("btn_primary")
        self.btn_browse.clicked.connect(self._browse_image)
        self.btn_clear = QPushButton("✕  HAPUS")
        self.btn_clear.setObjectName("btn_danger")
        self.btn_clear.clicked.connect(self._clear_image)
        btn_row.addWidget(self.btn_browse)
        btn_row.addWidget(self.btn_clear)
        left.addLayout(btn_row)

        # Info gambar
        img_group = QGroupBox("INFO GAMBAR")
        ig_layout = QVBoxLayout(img_group)
        ig_layout.setContentsMargins(12, 12, 12, 12)
        self.info_panel = InfoPanel()
        ig_layout.addWidget(self.info_panel)
        left.addWidget(img_group)

        # ── KOLOM TENGAH: Teks & Aksi ──
        mid = QVBoxLayout()
        mid.setSpacing(10)

        lbl_txt = QLabel("[ PESAN RAHASIA ]")
        lbl_txt.setObjectName("section_label")
        mid.addWidget(lbl_txt)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Ketik pesan rahasia Anda di sini...\n\n"
            "Pesan akan disembunyikan di dalam\n"
            "piksel gambar menggunakan metode LSB."
        )
        self.text_input.textChanged.connect(self._update_char_count)
        mid.addWidget(self.text_input, 1)

        # Counter karakter
        self.lbl_chars = QLabel("0 / 0 karakter")
        self.lbl_chars.setAlignment(Qt.AlignRight)
        self.lbl_chars.setStyleSheet(
            "color: #4A5A80; font-size: 10px; font-family: 'Courier New', monospace;"
        )
        mid.addWidget(self.lbl_chars)

        mid.addWidget(HLine())

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(6)
        mid.addWidget(self.progress)

        # Status
        self.status_bar = StatusBar()
        mid.addWidget(self.status_bar)

        # Tombol utama
        self.btn_embed = QPushButton("⚡  SEMBUNYIKAN PESAN")
        self.btn_embed.setObjectName("btn_success")
        self.btn_embed.setFixedHeight(48)
        self.btn_embed.clicked.connect(self._run_embed)
        mid.addWidget(self.btn_embed)

        # ── KOLOM KANAN: Output ──
        right = QVBoxLayout()
        right.setSpacing(10)

        lbl_out = QLabel("[ GAMBAR OUTPUT ]")
        lbl_out.setObjectName("section_label")
        right.addWidget(lbl_out)

        self.preview_out = ImagePreviewWidget("HASIL AKAN\nMUNCUL DI SINI")
        right.addWidget(self.preview_out, 1)

        self.btn_save = QPushButton("💾  SIMPAN GAMBAR")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_output)
        right.addWidget(self.btn_save)

        # Log output
        log_group = QGroupBox("LOG OPERASI")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(12, 12, 12, 8)
        self.log_area = QTextEdit()
        self.log_area.setObjectName("output_area")
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(120)
        log_layout.addWidget(self.log_area)
        right.addWidget(log_group)

        # ── Rakitan layout ──
        root.addLayout(left, 3)
        root.addLayout(mid, 3)
        root.addLayout(right, 3)

    # ── Handlers ──

    def _browse_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar Sumber", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)"
        )
        if path:
            self._load_image(path)

    def _on_image_dropped(self, path: str):
        self._load_image(path)

    def _load_image(self, path: str):
        self._source_path = path
        self.preview_in.set_image(path)
        try:
            info = sf.get_image_info(path)
            self.info_panel.set_info({
                "Nama File":   info["filename"],
                "Ukuran":      info["file_size"],
                "Dimensi":     f"{info['width']} × {info['height']} px",
                "Format":      info["format"],
                "Mode":        info["mode"],
                "Maks. Chars": f"{info['max_chars']:,}",
            })
            self._update_char_count()
            self.status_bar.set_status("info", f"Gambar dimuat: {info['filename']}")
        except Exception as e:
            self._log(f"ERROR: {e}", error=True)

    def _clear_image(self):
        self._source_path = None
        self.preview_in.clear_image()
        self.info_panel.clear()
        self.lbl_chars.setText("0 / 0 karakter")
        self.status_bar.set_status("idle", "SIAP")

    def _update_char_count(self):
        text = self.text_input.toPlainText()
        cur = len(text)
        if self._source_path:
            try:
                info = sf.get_image_info(self._source_path)
                max_c = info["max_chars"]
                color = "#00FF9F" if cur <= max_c else "#FF4757"
                self.lbl_chars.setText(f"{cur:,} / {max_c:,} karakter")
                self.lbl_chars.setStyleSheet(
                    f"color: {color}; font-size: 10px;"
                    f" font-family: 'Courier New', monospace;"
                )
                return
            except Exception:
                pass
        self.lbl_chars.setText(f"{cur:,} karakter")

    def _run_embed(self):
        if not self._source_path:
            self.status_bar.set_status("error", "PILIH GAMBAR TERLEBIH DAHULU")
            return
        text = self.text_input.toPlainText()
        if not text.strip():
            self.status_bar.set_status("error", "PESAN TIDAK BOLEH KOSONG")
            return

        # Tentukan output path sementara
        base = os.path.splitext(self._source_path)[0]
        self._output_path = base + "_steg.png"

        self.btn_embed.setEnabled(False)
        self.progress.setValue(10)
        self.status_bar.set_status("working", "MEMPROSES...")
        self._log("Memulai proses embedding...")

        self._worker = WorkerThread(
            sf.embed_text_lsb,
            self._source_path,
            text,
            self._output_path
        )
        self._worker.result_ready.connect(self._on_embed_done)
        self._worker.error_occurred.connect(self._on_embed_error)
        self._worker.progress.connect(self.progress.setValue)
        self._worker.start()

    def _on_embed_done(self, result: dict):
        self.btn_embed.setEnabled(True)
        if result.get("status") == "success":
            self.progress.setValue(100)
            self.status_bar.set_status("success", "PESAN BERHASIL DISEMBUNYIKAN!")
            self.preview_out.set_image(self._output_path)
            self.btn_save.setEnabled(True)
            self._log(
                f"✓ Berhasil!\n"
                f"  Karakter tersembunyi : {result['chars_hidden']:,}\n"
                f"  Output               : {self._output_path}"
            )
        else:
            self._on_embed_error(result.get("message", "Error tidak diketahui"))

        QTimer.singleShot(3000, lambda: self.progress.setValue(0))

    def _on_embed_error(self, error_msg: str):
        self.btn_embed.setEnabled(True)
        self.progress.setValue(0)
        self.status_bar.set_status("error", "GAGAL")
        self._log(f"✗ ERROR: {error_msg}", error=True)

    def _save_output(self):
        if not self._output_path or not os.path.exists(self._output_path):
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Gambar", "",
            "PNG Image (*.png)"
        )
        if path:
            if not path.lower().endswith(".png"):
                path += ".png"
            import shutil
            shutil.copy2(self._output_path, path)
            self.status_bar.set_status("success", f"DISIMPAN: {os.path.basename(path)}")
            self._log(f"✓ File disimpan ke: {path}")

    def _log(self, message: str, error: bool = False):
        color = "#FF4757" if error else "#00FF9F"
        self.log_area.append(
            f'<span style="color:{color}; font-family:\'Courier New\'">{message}</span>'
        )


# ─────────────────────────────────────────────
#   TAB EXTRACT (BACA PESAN)
# ─────────────────────────────────────────────

class ExtractTab(QWidget):
    """Tab untuk mengekstrak teks tersembunyi dari gambar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._image_path = None
        self._worker = None
        self._setup_ui()

    def _setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ── KOLOM KIRI: Input gambar ──
        left = QVBoxLayout()
        left.setSpacing(10)

        lbl = QLabel("[ GAMBAR YANG DIANALISIS ]")
        lbl.setObjectName("section_label")
        left.addWidget(lbl)

        self.preview = ImagePreviewWidget("PILIH GAMBAR\nUNTUK DIANALISIS")
        self.preview.image_dropped.connect(self._load_image)
        left.addWidget(self.preview, 1)

        btn_row = QHBoxLayout()
        self.btn_browse = QPushButton("◈  PILIH GAMBAR")
        self.btn_browse.setObjectName("btn_primary")
        self.btn_browse.clicked.connect(self._browse_image)
        self.btn_clear = QPushButton("✕  HAPUS")
        self.btn_clear.setObjectName("btn_danger")
        self.btn_clear.clicked.connect(self._clear_image)
        btn_row.addWidget(self.btn_browse)
        btn_row.addWidget(self.btn_clear)
        left.addLayout(btn_row)

        img_group = QGroupBox("INFO GAMBAR")
        ig_layout = QVBoxLayout(img_group)
        ig_layout.setContentsMargins(12, 12, 12, 12)
        self.info_panel = InfoPanel()
        ig_layout.addWidget(self.info_panel)
        left.addWidget(img_group)

        # ── KOLOM KANAN: Hasil ──
        right = QVBoxLayout()
        right.setSpacing(10)

        lbl_out = QLabel("[ PESAN TERSEMBUNYI ]")
        lbl_out.setObjectName("section_label")
        right.addWidget(lbl_out)

        # Progress & status
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(6)
        right.addWidget(self.progress)

        self.status_bar = StatusBar()
        right.addWidget(self.status_bar)

        # Tombol extract
        self.btn_extract = QPushButton("🔍  EKSTRAK PESAN")
        self.btn_extract.setObjectName("btn_success")
        self.btn_extract.setFixedHeight(48)
        self.btn_extract.clicked.connect(self._run_extract)
        right.addWidget(self.btn_extract)

        # Area output teks
        out_group = QGroupBox("HASIL EKSTRAKSI")
        og_layout = QVBoxLayout(out_group)
        og_layout.setContentsMargins(12, 12, 12, 12)
        og_layout.setSpacing(8)

        self.output_area = QTextEdit()
        self.output_area.setObjectName("output_area")
        self.output_area.setReadOnly(True)
        self.output_area.setPlaceholderText(
            "Pesan tersembunyi akan ditampilkan di sini setelah ekstraksi..."
        )
        og_layout.addWidget(self.output_area)

        copy_row = QHBoxLayout()
        self.btn_copy = QPushButton("⎘  SALIN TEKS")
        self.btn_copy.clicked.connect(self._copy_text)
        self.btn_copy.setEnabled(False)
        self.lbl_result_info = QLabel("")
        self.lbl_result_info.setStyleSheet(
            "color: #4A5A80; font-size: 10px; font-family: 'Courier New', monospace;"
        )
        copy_row.addWidget(self.btn_copy)
        copy_row.addStretch()
        copy_row.addWidget(self.lbl_result_info)
        og_layout.addLayout(copy_row)
        right.addWidget(out_group, 1)

        # Analisis LSB
        analyze_group = QGroupBox("ANALISIS LSB")
        al_layout = QVBoxLayout(analyze_group)
        al_layout.setContentsMargins(12, 12, 12, 12)
        self.analyze_area = QTextEdit()
        self.analyze_area.setObjectName("output_area")
        self.analyze_area.setReadOnly(True)
        self.analyze_area.setFixedHeight(100)
        al_layout.addWidget(self.analyze_area)

        self.btn_analyze = QPushButton("📊  ANALISIS GAMBAR")
        self.btn_analyze.clicked.connect(self._run_analyze)
        al_layout.addWidget(self.btn_analyze)
        right.addWidget(analyze_group)

        root.addLayout(left, 4)
        root.addLayout(right, 5)

    # ── Handlers ──

    def _browse_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)"
        )
        if path:
            self._load_image(path)

    def _load_image(self, path: str):
        self._image_path = path
        self.preview.set_image(path)
        try:
            info = sf.get_image_info(path)
            self.info_panel.set_info({
                "Nama File": info["filename"],
                "Ukuran":    info["file_size"],
                "Dimensi":   f"{info['width']} × {info['height']} px",
                "Format":    info["format"],
                "Mode":      info["mode"],
            })
            self.status_bar.set_status("info", f"Gambar dimuat: {info['filename']}")
        except Exception as e:
            self.status_bar.set_status("error", str(e))

    def _clear_image(self):
        self._image_path = None
        self.preview.clear_image()
        self.info_panel.clear()
        self.output_area.clear()
        self.analyze_area.clear()
        self.btn_copy.setEnabled(False)
        self.lbl_result_info.setText("")
        self.status_bar.set_status("idle", "SIAP")

    def _run_extract(self):
        if not self._image_path:
            self.status_bar.set_status("error", "PILIH GAMBAR TERLEBIH DAHULU")
            return

        self.btn_extract.setEnabled(False)
        self.progress.setValue(10)
        self.status_bar.set_status("working", "MENGANALISIS GAMBAR...")
        self.output_area.clear()
        self.btn_copy.setEnabled(False)

        self._worker = WorkerThread(sf.extract_text_lsb, self._image_path)
        self._worker.result_ready.connect(self._on_extract_done)
        self._worker.error_occurred.connect(self._on_extract_error)
        self._worker.progress.connect(self.progress.setValue)
        self._worker.start()

    def _on_extract_done(self, result: dict):
        self.btn_extract.setEnabled(True)
        self.progress.setValue(100)

        if result.get("status") == "success" and result.get("text"):
            text = result["text"]
            self.output_area.setPlainText(text)
            self.btn_copy.setEnabled(True)
            self.lbl_result_info.setText(f"{len(text):,} karakter ditemukan")
            self.status_bar.set_status("success", "PESAN DITEMUKAN!")
        else:
            self.output_area.setPlainText(
                f"[ {result.get('message', 'Tidak ada pesan ditemukan')} ]"
            )
            self.status_bar.set_status("warning", "TIDAK ADA PESAN TERSEMBUNYI")

        QTimer.singleShot(3000, lambda: self.progress.setValue(0))

    def _on_extract_error(self, error_msg: str):
        self.btn_extract.setEnabled(True)
        self.progress.setValue(0)
        self.status_bar.set_status("error", f"ERROR: {error_msg[:50]}")
        self.output_area.setPlainText(f"[ ERROR: {error_msg} ]")

    def _copy_text(self):
        from PyQt5.QtWidgets import QApplication
        text = self.output_area.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_bar.set_status("success", "TEKS DISALIN KE CLIPBOARD")
            QTimer.singleShot(2000, lambda: self.status_bar.set_status("idle", "SIAP"))

    def _run_analyze(self):
        if not self._image_path:
            self.status_bar.set_status("error", "PILIH GAMBAR TERLEBIH DAHULU")
            return

        self._worker = WorkerThread(sf.analyze_image_lsb, self._image_path)
        self._worker.result_ready.connect(self._on_analyze_done)
        self._worker.error_occurred.connect(lambda e: self.analyze_area.setPlainText(f"ERROR: {e}"))
        self._worker.start()

    def _on_analyze_done(self, result: dict):
        lines = [
            f"LSB Ratio    : {result['lsb_ratio']:.4f}",
            f"Deviasi      : {result['deviation']:.4f}",
            f"R channel    : {result['channel_lsb']['R']:.4f}",
            f"G channel    : {result['channel_lsb']['G']:.4f}",
            f"B channel    : {result['channel_lsb']['B']:.4f}",
            f"",
            f"Verdict      : {result['verdict']}",
        ]
        self.analyze_area.setPlainText("\n".join(lines))


# ─────────────────────────────────────────────
#   TAB COMPARE (BANDINGKAN GAMBAR)
# ─────────────────────────────────────────────

class CompareTab(QWidget):
    """Tab untuk membandingkan dua gambar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._path_a = None
        self._path_b = None
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        lbl = QLabel("[ BANDINGKAN DUA GAMBAR — ASLI vs STEGANO ]")
        lbl.setObjectName("section_label")
        root.addWidget(lbl)

        # Dua preview
        previews = QHBoxLayout()
        previews.setSpacing(12)

        left_col = QVBoxLayout()
        lbl_a = QLabel("GAMBAR A  (Asli)")
        lbl_a.setStyleSheet("color: #00D4FF; font-size: 10px; letter-spacing: 2px;")
        left_col.addWidget(lbl_a)
        self.preview_a = ImagePreviewWidget("GAMBAR A")
        self.preview_a.image_dropped.connect(lambda p: self._load_img("a", p))
        left_col.addWidget(self.preview_a)
        btn_a = QPushButton("◈  PILIH GAMBAR A")
        btn_a.clicked.connect(lambda: self._browse("a"))
        left_col.addWidget(btn_a)

        right_col = QVBoxLayout()
        lbl_b = QLabel("GAMBAR B  (Stegano)")
        lbl_b.setStyleSheet("color: #00FF9F; font-size: 10px; letter-spacing: 2px;")
        right_col.addWidget(lbl_b)
        self.preview_b = ImagePreviewWidget("GAMBAR B")
        self.preview_b.image_dropped.connect(lambda p: self._load_img("b", p))
        right_col.addWidget(self.preview_b)
        btn_b = QPushButton("◈  PILIH GAMBAR B")
        btn_b.clicked.connect(lambda: self._browse("b"))
        right_col.addWidget(btn_b)

        previews.addLayout(left_col)
        previews.addLayout(right_col)
        root.addLayout(previews, 1)

        self.btn_compare = QPushButton("⚡  BANDINGKAN GAMBAR")
        self.btn_compare.setObjectName("btn_primary")
        self.btn_compare.setFixedHeight(44)
        self.btn_compare.clicked.connect(self._run_compare)
        root.addWidget(self.btn_compare)

        result_group = QGroupBox("HASIL PERBANDINGAN")
        rg_layout = QVBoxLayout(result_group)
        rg_layout.setContentsMargins(12, 12, 12, 12)
        self.result_area = QTextEdit()
        self.result_area.setObjectName("output_area")
        self.result_area.setReadOnly(True)
        self.result_area.setFixedHeight(160)
        rg_layout.addWidget(self.result_area)
        root.addWidget(result_group)

    def _browse(self, which: str):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)"
        )
        if path:
            self._load_img(which, path)

    def _load_img(self, which: str, path: str):
        if which == "a":
            self._path_a = path
            self.preview_a.set_image(path)
        else:
            self._path_b = path
            self.preview_b.set_image(path)

    def _run_compare(self):
        if not self._path_a or not self._path_b:
            self.result_area.setPlainText("[ Pilih kedua gambar terlebih dahulu ]")
            return

        try:
            result = sf.compare_images(self._path_a, self._path_b)
            if "error" in result:
                self.result_area.setPlainText(f"ERROR: {result['error']}")
                return

            hash_a = sf.calculate_image_hash(self._path_a)
            hash_b = sf.calculate_image_hash(self._path_b)

            lines = [
                f"Hash A (SHA256): {hash_a['short']}...",
                f"Hash B (SHA256): {hash_b['short']}...",
                f"",
                f"MSE             : {result['mse']:.6f}",
                f"PSNR            : {result['psnr']:.2f} dB",
                f"Pixel berubah   : {result['changed_pixels']:,} / {result['total_pixels']:,}",
                f"Persentase ubah : {result['change_percent']}%",
                f"",
                f"Kualitas        : {result['quality']}",
            ]
            self.result_area.setPlainText("\n".join(lines))
        except Exception as e:
            self.result_area.setPlainText(f"ERROR: {e}")
