from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame


class MoodBarWidget(QFrame):
    def __init__(self, mood, count, percent, parent=None):
        super().__init__(parent)

        self.setObjectName("StatCard")
        self.percent = percent
        self.bar_color = self.get_bar_color(mood)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.mood_label = QLabel(mood)
        self.mood_label.setStyleSheet("font-size: 15px; font-weight: 600;")

        self.count_label = QLabel(f"{count} 篇 · {percent}%")
        self.count_label.setStyleSheet("color: #f3c8ff; font-size: 13px;")

        top_row.addWidget(self.mood_label)
        top_row.addStretch()
        top_row.addWidget(self.count_label)

        self.track = QFrame()
        self.track.setFixedHeight(10)
        self.track.setStyleSheet("""
            QFrame {
                background-color: #1f2228;
                border-radius: 5px;
            }
        """)

        self.fill = QFrame(self.track)
        self.fill.setFixedHeight(10)
        self.fill.setStyleSheet(f"""
            QFrame {{
                background-color: {self.bar_color};
                border-radius: 5px;
            }}
        """)

        layout.addLayout(top_row)
        layout.addWidget(self.track)

    def get_bar_color(self, mood):
        mood_map = {
            "开心 😄": "#ffd166",
            "平静 😊": "#72ddf7",
            "疲惫 😪": "#a0aec0",
            "焦虑 😣": "#ff8fab",
            "难过 😢": "#89c2d9",
            "生气 😠": "#ef476f",
        }
        return mood_map.get(mood, "#d9a7ff")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        track_width = self.track.width()
        fill_width = max(12, int(track_width * self.percent / 100)) if self.percent > 0 else 0
        self.fill.setGeometry(0, 0, fill_width, self.track.height())