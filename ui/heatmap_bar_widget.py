from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel


class HeatmapBarWidget(QFrame):
    def __init__(self, label, weekday, count, percent, parent=None):
        super().__init__(parent)

        self.setObjectName("StatCard")
        self.percent = percent

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        self.date_label = QLabel(label)
        self.date_label.setStyleSheet("font-size: 15px; font-weight: 600;")

        self.weekday_label = QLabel(weekday)
        self.weekday_label.setStyleSheet("font-size: 12px; color: #b8bec9;")

        left_layout.addWidget(self.date_label)
        left_layout.addWidget(self.weekday_label)

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
        self.fill.setStyleSheet("""
            QFrame {
                background-color: #72ddf7;
                border-radius: 5px;
            }
        """)

        self.count_label = QLabel(f"{count} 篇")
        self.count_label.setStyleSheet("font-size: 13px; color: #d4d8df;")

        layout.addLayout(left_layout, 1)
        layout.addWidget(self.track, 3)
        layout.addWidget(self.count_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        track_width = self.track.width()
        fill_width = max(10, int(track_width * self.percent / 100)) if self.percent > 0 else 0
        self.fill.setGeometry(0, 0, fill_width, self.track.height())