from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QFrame, QScrollArea
)

from utils.image_exporter import render_entry_to_pixmap, export_entry_as_image


class ExportPreviewDialog(QDialog):
    def __init__(self, entry, parent=None):
        super().__init__(parent)

        self.entry = entry
        self.current_theme = entry["theme"] if "theme" in entry.keys() else "night"

        self.theme_display_map = {
            "夜幕紫蓝": "night",
            "奶油暖光": "cream",
            "极简白卡": "minimal"
        }
        self.reverse_theme_map = {v: k for k, v in self.theme_display_map.items()}

        self.setWindowTitle("导出图片预览")
        self.resize(900, 700)

        root_layout = QVBoxLayout(self)

        # 顶部栏
        top_bar = QHBoxLayout()
        title = QLabel("导出预览")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_display_map.keys())

        default_display = self.reverse_theme_map.get(self.current_theme, "夜幕紫蓝")
        self.theme_combo.setCurrentText(default_display)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)

        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(QLabel("模板："))
        top_bar.addWidget(self.theme_combo)

        # 预览区
        preview_frame = QFrame()
        preview_layout = QVBoxLayout(preview_frame)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)

        self.scroll.setWidget(self.preview_label)
        preview_layout.addWidget(self.scroll)

        # 底部按钮
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.save_btn = QPushButton("保存图片")

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_image)

        bottom_bar.addWidget(self.cancel_btn)
        bottom_bar.addWidget(self.save_btn)

        root_layout.addLayout(top_bar)
        root_layout.addWidget(preview_frame)
        root_layout.addLayout(bottom_bar)

        self.update_preview()

    def on_theme_changed(self):
        display_name = self.theme_combo.currentText()
        self.current_theme = self.theme_display_map[display_name]
        self.update_preview()

    def update_preview(self):
        pixmap = render_entry_to_pixmap(self.entry, theme_name=self.current_theme)
        scaled = pixmap.scaled(600, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_label.setPixmap(scaled)

    def save_image(self):
        safe_title = self.entry["title"].replace("/", "_").replace("\\", "_")
        default_name = f'{self.entry["created_at"][:10]}_{safe_title}_{self.current_theme}.png'
        default_path = str(Path.home() / "Desktop" / default_name)

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            default_path,
            "PNG 图片 (*.png)"
        )

        if not save_path:
            return

        export_entry_as_image(self.entry, save_path, theme_name=self.current_theme)

        QMessageBox.information(self, "成功", f"已保存到：\n{save_path}")
        self.accept()