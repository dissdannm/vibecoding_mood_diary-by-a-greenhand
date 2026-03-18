from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QPixmap, QPainter, QColor, QFont, QLinearGradient,
    QPen, QTextOption
)


def get_theme_config(theme_name):
    themes = {
        "night": {
            "bg_mode": "gradient",
            "bg_start": "#6d597a",
            "bg_mid": "#355070",
            "bg_end": "#1b263b",
            "card_color": QColor(255, 255, 255, 235),
            "title_color": "#1f2430",
            "meta_color": "#6b7280",
            "body_color": "#2d3748",
            "line_color": "#d9a7ff",
            "footer_color": "#94a3b8",
            "footer_text": "Mood Diary · 写给自己的温柔记录"
        },
        "cream": {
            "bg_mode": "solid",
            "bg_color": "#f6efe7",
            "card_color": QColor("#fffaf4"),
            "title_color": "#5c4b51",
            "meta_color": "#9c7c6e",
            "body_color": "#4a403a",
            "line_color": "#e8b4a0",
            "footer_color": "#b08968",
            "footer_text": "Mood Diary · 柔和地收藏今天"
        },
        "minimal": {
            "bg_mode": "solid",
            "bg_color": "#edf2f7",
            "card_color": QColor("#ffffff"),
            "title_color": "#111827",
            "meta_color": "#6b7280",
            "body_color": "#1f2937",
            "line_color": "#94a3b8",
            "footer_color": "#9ca3af",
            "footer_text": "Mood Diary · Minimal Edition"
        }
    }
    return themes.get(theme_name, themes["night"])


def draw_background(painter, width, height, config):
    if config["bg_mode"] == "gradient":
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor(config["bg_start"]))
        gradient.setColorAt(0.45, QColor(config["bg_mid"]))
        gradient.setColorAt(1, QColor(config["bg_end"]))
        painter.fillRect(0, 0, width, height, gradient)
    else:
        painter.fillRect(0, 0, width, height, QColor(config["bg_color"]))


# ⭐⭐⭐ 关键函数：用于预览
def render_entry_to_pixmap(entry, theme_name=None):
    theme_name = theme_name or entry["theme"] or "night"
    config = get_theme_config(theme_name)

    width = 1080
    height = 1350
    margin = 70

    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)

    draw_background(painter, width, height, config)

    card_rect = QRectF(margin, margin, width - margin * 2, height - margin * 2)
    painter.setPen(Qt.NoPen)
    painter.setBrush(config["card_color"])
    painter.drawRoundedRect(card_rect, 28, 28)

    content_left = margin + 50
    content_top = margin + 90
    content_width = width - (margin + 50) * 2

    # 标题
    painter.setFont(QFont("Microsoft YaHei", 26))
    painter.setPen(QColor(config["title_color"]))
    painter.drawText(
        QRectF(content_left, content_top, content_width, 90),
        Qt.TextWordWrap,
        entry["title"]
    )

    # 元信息
    painter.setFont(QFont("Microsoft YaHei", 12))
    painter.setPen(QColor(config["meta_color"]))
    painter.drawText(content_left, content_top + 100, f'心情：{entry["mood"]}')
    painter.drawText(content_left + 220, content_top + 100, f'创建时间：{entry["created_at"]}')

    # 正文
    painter.setFont(QFont("Microsoft YaHei", 15))
    painter.setPen(QColor(config["body_color"]))

    body_text = entry["content"]
    if len(body_text) > 700:
        body_text = body_text[:700] + "\n\n..."

    text_option = QTextOption()
    text_option.setWrapMode(QTextOption.WordWrap)

    painter.drawText(
        QRectF(content_left, content_top + 150, content_width, 820),
        body_text,
        text_option
    )

    painter.end()
    return pixmap


# ⭐ 保存图片
def export_entry_as_image(entry, save_path, theme_name=None):
    pixmap = render_entry_to_pixmap(entry, theme_name)
    pixmap.save(str(Path(save_path)), "PNG")