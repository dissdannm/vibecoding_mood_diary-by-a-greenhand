from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy


class DiaryCardWidget(QFrame):
    def __init__(self, title, mood, created_at, content, parent=None):
        super().__init__(parent)

        self.setObjectName("DiaryCard")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("DiaryCardTitle")
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.mood_label = QLabel(mood)
        self.mood_label.setObjectName("DiaryCardMood")
        self.mood_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        top_row.addWidget(self.title_label)
        top_row.addWidget(self.mood_label)

        self.date_label = QLabel(created_at[:16])
        self.date_label.setObjectName("DiaryCardDate")

        summary = content.strip().replace("\n", " ")
        if len(summary) > 60:
            summary = summary[:60] + "..."

        self.summary_label = QLabel(summary)
        self.summary_label.setObjectName("DiaryCardSummary")
        self.summary_label.setWordWrap(True)

        layout.addLayout(top_row)
        layout.addWidget(self.date_label)
        layout.addWidget(self.summary_label)