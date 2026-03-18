from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QHBoxLayout
)


class EntryDialog(QDialog):
    def __init__(self, parent=None, entry=None):
        super().__init__(parent)
        self.entry = entry
        self.setWindowTitle("编辑日记" if entry else "新建日记")
        self.resize(500, 470)

        self.setStyleSheet("""
        QDialog {
            background-color: #23262b;
            color: #f5f5f5;
            font-family: "Microsoft YaHei";
            font-size: 14px;
        }
        QLabel {
            font-size: 14px;
            font-weight: 500;
            margin-top: 6px;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #2b2f36;
            border: 1px solid #3d434c;
            border-radius: 10px;
            padding: 8px 10px;
            color: #f5f5f5;
        }
        QPushButton {
            background-color: #3a3f47;
            border: none;
            border-radius: 10px;
            padding: 10px 14px;
            min-width: 90px;
        }
        QPushButton:hover {
            background-color: #4a5059;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title_label = QLabel("标题")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("给今天的心情起个名字")

        mood_label = QLabel("心情")
        self.mood_combo = QComboBox()
        self.mood_options = [
            "开心 😄",
            "平静 😊",
            "疲惫 😪",
            "焦虑 😣",
            "难过 😢",
            "生气 😠"
        ]
        self.mood_combo.addItems(self.mood_options)

        theme_label = QLabel("导出模板")
        self.theme_combo = QComboBox()
        self.theme_map = {
            "夜幕紫蓝": "night",
            "奶油暖光": "cream",
            "极简白卡": "minimal"
        }
        self.theme_combo.addItems(self.theme_map.keys())

        content_label = QLabel("内容")
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("今天发生了什么？你想记下什么？")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.save_btn = QPushButton("保存")

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)

        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(mood_label)
        layout.addWidget(self.mood_combo)
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(content_label)
        layout.addWidget(self.content_input)
        layout.addLayout(btn_layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.validate_and_accept)

        if self.entry:
            self.fill_entry_data()

    def fill_entry_data(self):
        self.title_input.setText(self.entry["title"])
        self.content_input.setPlainText(self.entry["content"])

        mood = self.entry["mood"] or ""
        index = self.mood_combo.findText(mood)
        if index >= 0:
            self.mood_combo.setCurrentIndex(index)

        theme_value = self.entry["theme"] or "night"
        for display_name, internal_name in self.theme_map.items():
            if internal_name == theme_value:
                index = self.theme_combo.findText(display_name)
                if index >= 0:
                    self.theme_combo.setCurrentIndex(index)
                break

    def validate_and_accept(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "提示", "请输入标题")
            return

        if not content:
            QMessageBox.warning(self, "提示", "请输入日记内容")
            return

        self.accept()

    def get_data(self):
        selected_theme_display = self.theme_combo.currentText()
        selected_theme_value = self.theme_map[selected_theme_display]

        return {
            "title": self.title_input.text().strip(),
            "content": self.content_input.toPlainText().strip(),
            "mood": self.mood_combo.currentText(),
            "theme": selected_theme_value
        }