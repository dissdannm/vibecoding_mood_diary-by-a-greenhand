from ui.export_preview_dialog import ExportPreviewDialog
from datetime import datetime

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QListWidget,
    QListWidgetItem, QMessageBox, QStackedWidget, QGridLayout,
    QFileDialog
)

from ui.styles import APP_STYLE
from ui.entry_dialog import EntryDialog
from ui.diary_card_widget import DiaryCardWidget
from ui.mood_bar_widget import MoodBarWidget
from ui.heatmap_bar_widget import HeatmapBarWidget
from data.database import (
    add_entry, get_all_entries, get_entry_by_id,
    update_entry, delete_entry, search_entries,
    get_stats_summary, get_last_7_days_activity
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mood Diary")
        self.resize(1280, 800)

        self.current_entry_id = None
        self.card_widgets = {}

        central = QWidget()
        self.setCentralWidget(central)
        self.setStyleSheet(APP_STYLE)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(16)

        sidebar = self.build_sidebar()

        self.stacked = QStackedWidget()
        self.home_page = self.build_home_page()
        self.stats_page = self.build_stats_page()

        self.stacked.addWidget(self.home_page)
        self.stacked.addWidget(self.stats_page)

        root_layout.addWidget(sidebar, 1)
        root_layout.addWidget(self.stacked, 4)

        self.load_entries()
        self.load_stats()

    def build_sidebar(self):
        frame = QFrame()
        frame.setObjectName("Sidebar")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("🌙 Mood Diary")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.btn_today = QPushButton("今天")
        self.btn_all = QPushButton("全部日记")
        self.btn_stats = QPushButton("统计")
        self.btn_settings = QPushButton("设置")

        self.btn_today.clicked.connect(self.show_home_page)
        self.btn_all.clicked.connect(self.show_home_page)
        self.btn_stats.clicked.connect(self.show_stats_page)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.btn_today)
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_stats)
        layout.addStretch()
        layout.addWidget(self.btn_settings)

        return frame

    def build_home_page(self):
        frame = QFrame()
        frame.setObjectName("CentralCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(16)

        hero_card = self.build_hero_card()
        stats_panel = self.build_stats_panel()

        top_layout.addWidget(hero_card, 3)
        top_layout.addWidget(stats_panel, 1)

        self.search = QLineEdit()
        self.search.setPlaceholderText("搜索你的心情、关键词、日期...")
        self.search.textChanged.connect(self.on_search_changed)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        list_panel = QFrame()
        list_panel.setObjectName("ContentCard")
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(14, 14, 14, 14)
        list_layout.setSpacing(10)

        list_title = QLabel("日记列表")
        list_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.result_info_label = QLabel("共 0 篇")
        self.result_info_label.setStyleSheet("color: #b8bec9; font-size: 13px;")

        self.diary_list = QListWidget()
        self.diary_list.setSpacing(8)
        self.diary_list.itemClicked.connect(self.show_entry_detail)

        list_layout.addWidget(list_title)
        list_layout.addWidget(self.result_info_label)
        list_layout.addWidget(self.diary_list)

        detail_panel = QFrame()
        detail_panel.setObjectName("ContentCard")
        detail_layout = QVBoxLayout(detail_panel)
        detail_layout.setContentsMargins(18, 18, 18, 18)
        detail_layout.setSpacing(10)

        detail_title = QLabel("日记详情")
        detail_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.detail_title_label = QLabel("请选择一篇日记")
        self.detail_title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.detail_meta_label = QLabel("")
        self.detail_meta_label.setStyleSheet("color: #b8bec9; font-size: 13px;")

        self.detail_content_label = QLabel("这里显示你选中的日记内容。")
        self.detail_content_label.setWordWrap(True)
        self.detail_content_label.setAlignment(Qt.AlignTop)
        self.detail_content_label.setStyleSheet(
            "font-size: 15px; line-height: 1.8; color: #e6e9ef;"
        )

        action_layout = QHBoxLayout()
        self.edit_btn = QPushButton("编辑")
        self.delete_btn = QPushButton("删除")
        self.export_btn = QPushButton("导出图片")

        self.edit_btn.clicked.connect(self.edit_current_entry)
        self.delete_btn.clicked.connect(self.delete_current_entry)
        self.export_btn.clicked.connect(self.export_current_entry_image)

        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.delete_btn)
        action_layout.addWidget(self.export_btn)
        action_layout.addStretch()

        detail_layout.addWidget(detail_title)
        detail_layout.addWidget(self.detail_title_label)
        detail_layout.addWidget(self.detail_meta_label)
        detail_layout.addLayout(action_layout)
        detail_layout.addSpacing(10)
        detail_layout.addWidget(self.detail_content_label)
        detail_layout.addStretch()

        content_layout.addWidget(list_panel, 2)
        content_layout.addWidget(detail_panel, 3)

        layout.addLayout(top_layout)
        layout.addWidget(self.search)
        layout.addLayout(content_layout)

        return frame

    def build_stats_page(self):
        frame = QFrame()
        frame.setObjectName("CentralCard")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("情绪统计")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")

        subtitle = QLabel("看看最近的自己，哪些情绪出现得更多一些。")
        subtitle.setStyleSheet("color: #b8bec9; font-size: 14px;")

        summary_grid = QGridLayout()
        summary_grid.setSpacing(16)

        self.stats_total_card = self.create_stat_block("总日记数", "0")
        self.stats_recent_card = self.create_stat_block("最近 7 天", "0")
        self.stats_top_mood_card = self.create_stat_block("最常出现的心情", "--")

        summary_grid.addWidget(self.stats_total_card["frame"], 0, 0)
        summary_grid.addWidget(self.stats_recent_card["frame"], 0, 1)
        summary_grid.addWidget(self.stats_top_mood_card["frame"], 0, 2)

        self.mood_list_panel = QFrame()
        self.mood_list_panel.setObjectName("ContentCard")
        mood_layout = QVBoxLayout(self.mood_list_panel)
        mood_layout.setContentsMargins(18, 18, 18, 18)
        mood_layout.setSpacing(12)

        mood_title = QLabel("心情分布")
        mood_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.mood_stats_container = QVBoxLayout()
        self.mood_stats_container.setSpacing(10)

        mood_layout.addWidget(mood_title)
        mood_layout.addLayout(self.mood_stats_container)
        mood_layout.addStretch()

        self.activity_panel = QFrame()
        self.activity_panel.setObjectName("ContentCard")
        activity_layout = QVBoxLayout(self.activity_panel)
        activity_layout.setContentsMargins(18, 18, 18, 18)
        activity_layout.setSpacing(12)

        activity_title = QLabel("最近 7 天写作热度")
        activity_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.activity_container = QVBoxLayout()
        self.activity_container.setSpacing(10)

        activity_layout.addWidget(activity_title)
        activity_layout.addLayout(self.activity_container)
        activity_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(summary_grid)
        layout.addWidget(self.mood_list_panel)
        layout.addWidget(self.activity_panel)

        return frame

    def create_stat_block(self, label_text, value_text):
        frame = QFrame()
        frame.setObjectName("StatCard")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        value_label = QLabel(value_text)
        value_label.setObjectName("StatValue")

        label = QLabel(label_text)
        label.setObjectName("StatLabel")

        layout.addWidget(value_label)
        layout.addWidget(label)
        layout.addStretch()

        return {
            "frame": frame,
            "value_label": value_label,
            "label": label
        }

    def build_hero_card(self):
        frame = QFrame()
        frame.setObjectName("HeroCard")
        frame.setMinimumHeight(190)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(10)

        self.hero_eyebrow = QLabel(self.get_today_text())
        self.hero_eyebrow.setObjectName("HeroEyebrow")

        self.hero_title = QLabel(self.get_greeting_text())
        self.hero_title.setObjectName("HeroTitle")

        self.hero_subtitle = QLabel("留一点时间给自己，把今天的情绪、片段和想法温柔地记录下来。")
        self.hero_subtitle.setObjectName("HeroSubtitle")
        self.hero_subtitle.setWordWrap(True)

        self.hero_button = QPushButton("＋ 立即记录")
        self.hero_button.setObjectName("PrimaryButton")
        self.hero_button.setFixedWidth(140)
        self.hero_button.setFixedHeight(44)
        self.hero_button.clicked.connect(self.open_entry_dialog)

        layout.addWidget(self.hero_eyebrow)
        layout.addWidget(self.hero_title)
        layout.addWidget(self.hero_subtitle)
        layout.addStretch()
        layout.addWidget(self.hero_button, alignment=Qt.AlignLeft)

        return frame

    def build_stats_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.total_card = QFrame()
        self.total_card.setObjectName("StatCard")
        total_layout = QVBoxLayout(self.total_card)
        total_layout.setContentsMargins(18, 18, 18, 18)

        self.total_value_label = QLabel("0")
        self.total_value_label.setObjectName("StatValue")

        total_text_label = QLabel("已经写下的片段")
        total_text_label.setObjectName("StatLabel")

        total_layout.addWidget(self.total_value_label)
        total_layout.addWidget(total_text_label)
        total_layout.addStretch()

        self.mood_card = QFrame()
        self.mood_card.setObjectName("StatCard")
        mood_layout = QVBoxLayout(self.mood_card)
        mood_layout.setContentsMargins(18, 18, 18, 18)

        self.latest_mood_value_label = QLabel("--")
        self.latest_mood_value_label.setObjectName("StatValue")

        mood_text_label = QLabel("最近一次心情")
        mood_text_label.setObjectName("StatLabel")

        mood_layout.addWidget(self.latest_mood_value_label)
        mood_layout.addWidget(mood_text_label)
        mood_layout.addStretch()

        layout.addWidget(self.total_card)
        layout.addWidget(self.mood_card)

        return panel

    def get_today_text(self):
        now = datetime.now()
        weekday_map = {
            0: "星期一",
            1: "星期二",
            2: "星期三",
            3: "星期四",
            4: "星期五",
            5: "星期六",
            6: "星期日",
        }
        return f"{now.year} 年 {now.month} 月 {now.day} 日 · {weekday_map[now.weekday()]}"

    def get_greeting_text(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "早上好，今天也要照顾好自己。"
        if 12 <= hour < 18:
            return "下午好，记下此刻的心情吧。"
        return "晚上好，把今天轻轻收进日记里。"

    def show_home_page(self):
        self.stacked.setCurrentWidget(self.home_page)

    def show_stats_page(self):
        self.load_stats()
        self.stacked.setCurrentWidget(self.stats_page)

    def open_entry_dialog(self):
        dialog = EntryDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            add_entry(data["title"], data["content"], data["mood"], data["theme"])
            self.load_entries(select_latest=True)
            self.load_stats()

    def on_search_changed(self):
        self.load_entries(select_latest=False)

    def load_entries(self, select_latest=False):
        self.diary_list.clear()
        self.card_widgets = {}

        keyword = self.search.text().strip()
        if keyword:
            entries = search_entries(keyword)
            self.result_info_label.setText(f"搜索到 {len(entries)} 篇")
        else:
            entries = get_all_entries()
            self.result_info_label.setText(f"共 {len(entries)} 篇")

        self.update_top_summary(entries)

        selected_row = 0
        found_current = False

        for index, entry in enumerate(entries):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, entry["id"])
            item.setSizeHint(QSize(100, 132))

            card = DiaryCardWidget(
                title=entry["title"],
                mood=entry["mood"],
                created_at=entry["created_at"],
                content=entry["content"]
            )

            self.diary_list.addItem(item)
            self.diary_list.setItemWidget(item, card)

            self.card_widgets[entry["id"]] = card

            if entry["id"] == self.current_entry_id:
                selected_row = index
                found_current = True

        if entries:
            if select_latest or not found_current:
                selected_row = 0

            self.diary_list.setCurrentRow(selected_row)
            current_item = self.diary_list.item(selected_row)
            if current_item:
                self.display_entry(current_item.data(Qt.UserRole))
                self.update_card_selection(current_item.data(Qt.UserRole))
        else:
            self.current_entry_id = None
            self.show_empty_detail(keyword=keyword)

    def load_stats(self):
        stats = get_stats_summary()

        self.stats_total_card["value_label"].setText(str(stats["total"]))
        self.stats_recent_card["value_label"].setText(str(stats["recent_count"]))
        self.stats_top_mood_card["value_label"].setText(stats["top_mood"])

        while self.mood_stats_container.count():
            item = self.mood_stats_container.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if stats["mood_stats"]:
            total = sum(item["count"] for item in stats["mood_stats"])

            for mood_item in stats["mood_stats"]:
                percent = round(mood_item["count"] * 100 / total) if total else 0

                bar = MoodBarWidget(
                    mood=mood_item["mood"],
                    count=mood_item["count"],
                    percent=percent
                )
                self.mood_stats_container.addWidget(bar)
        else:
            empty_label = QLabel("还没有数据，先写下几篇日记吧。")
            empty_label.setStyleSheet("color: #b8bec9; font-size: 14px;")
            self.mood_stats_container.addWidget(empty_label)

        while self.activity_container.count():
            item = self.activity_container.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        activities = get_last_7_days_activity()
        max_count = max((item["count"] for item in activities), default=0)

        for item in activities:
            percent = round(item["count"] * 100 / max_count) if max_count > 0 else 0

            bar = HeatmapBarWidget(
                label=item["label"],
                weekday=item["weekday"],
                count=item["count"],
                percent=percent
            )
            self.activity_container.addWidget(bar)

    def update_top_summary(self, entries):
        self.total_value_label.setText(str(len(entries)))

        if entries:
            latest_mood = entries[0]["mood"] or "--"
            self.latest_mood_value_label.setText(latest_mood)
        else:
            self.latest_mood_value_label.setText("--")

        self.hero_eyebrow.setText(self.get_today_text())
        self.hero_title.setText(self.get_greeting_text())

    def update_card_selection(self, selected_entry_id):
        for entry_id, card in self.card_widgets.items():
            is_selected = entry_id == selected_entry_id
            card.setProperty("selected", "true" if is_selected else "false")
            card.style().unpolish(card)
            card.style().polish(card)
            card.update()

    def show_empty_detail(self, keyword=""):
        if keyword:
            self.detail_title_label.setText("没有找到匹配的日记")
            self.detail_meta_label.setText("")
            self.detail_content_label.setText("试试换一个关键词，比如心情、标题或日期。")
        else:
            self.detail_title_label.setText("还没有日记")
            self.detail_meta_label.setText("")
            self.detail_content_label.setText("点击上方“＋ 立即记录”，写下第一篇吧。")

    def show_entry_detail(self, item):
        entry_id = item.data(Qt.UserRole)
        self.display_entry(entry_id)
        self.update_card_selection(entry_id)

    def display_entry(self, entry_id):
        entry = get_entry_by_id(entry_id)
        if not entry:
            return

        self.current_entry_id = entry["id"]
        self.detail_title_label.setText(entry["title"])

        updated_text = ""
        if entry["updated_at"] and entry["updated_at"] != entry["created_at"]:
            updated_text = f"    更新于：{entry['updated_at']}"

        self.detail_meta_label.setText(
            f'心情：{entry["mood"]}    创建时间：{entry["created_at"]}{updated_text}'
        )
        self.detail_content_label.setText(entry["content"])

    def edit_current_entry(self):
        if not self.current_entry_id:
            QMessageBox.information(self, "提示", "请先选择一篇日记")
            return

        entry = get_entry_by_id(self.current_entry_id)
        if not entry:
            QMessageBox.warning(self, "提示", "未找到这篇日记")
            return

        dialog = EntryDialog(self, entry=entry)
        if dialog.exec():
            data = dialog.get_data()
            update_entry(
                self.current_entry_id,
                data["title"],
                data["content"],
                data["mood"],
                data["theme"]
            )
            self.load_entries()
            self.load_stats()

    def export_current_entry_image(self):
        if not self.current_entry_id:
            QMessageBox.information(self, "提示", "请先选择一篇日记")
            return

        entry = get_entry_by_id(self.current_entry_id)
        if not entry:
            QMessageBox.warning(self, "提示", "未找到这篇日记")
            return

        dialog = ExportPreviewDialog(entry, self)
        dialog.exec()
    def delete_current_entry(self):
        if not self.current_entry_id:
            QMessageBox.information(self, "提示", "请先选择一篇日记")
            return

        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这篇日记吗？删除后无法恢复。",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_entry(self.current_entry_id)
            self.current_entry_id = None
            self.load_entries()
            self.load_stats()

    def export_current_entry_image(self):
        if not self.current_entry_id:
            QMessageBox.information(self, "提示", "请先选择一篇日记")
            return

        entry = get_entry_by_id(self.current_entry_id)
        if not entry:
            QMessageBox.warning(self, "提示", "未找到这篇日记")
            return

        dialog = ExportPreviewDialog(entry, self)
        dialog.exec()