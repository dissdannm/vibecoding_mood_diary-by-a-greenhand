APP_STYLE = """
QWidget {
    background-color: #1e1f22;
    color: #f5f5f5;
    font-family: "Microsoft YaHei";
    font-size: 14px;
}

#CentralCard {
    background-color: #2a2d33;
    border-radius: 24px;
}

#Sidebar {
    background-color: #23262b;
    border-radius: 20px;
}

#ContentCard {
    background-color: #2f333a;
    border-radius: 20px;
    padding: 12px;
}

#HeroCard {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #6d597a,
        stop:0.5 #355070,
        stop:1 #1b263b
    );
    border-radius: 24px;
}

#StatCard {
    background-color: #262a31;
    border: 1px solid #3a3f47;
    border-radius: 18px;
}

#HeroEyebrow {
    color: rgba(255, 255, 255, 0.72);
    font-size: 13px;
    font-weight: 500;
    background: transparent;
}

#HeroTitle {
    color: white;
    font-size: 32px;
    font-weight: 700;
    background: transparent;
}

#HeroSubtitle {
    color: rgba(255, 255, 255, 0.86);
    font-size: 15px;
    line-height: 1.7;
    background: transparent;
}

#StatValue {
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    background: transparent;
}

#StatLabel {
    color: #b8bec9;
    font-size: 13px;
    background: transparent;
}

QPushButton {
    background-color: #3a3f47;
    border: none;
    border-radius: 14px;
    padding: 10px 14px;
}

QPushButton:hover {
    background-color: #4a5059;
}

QPushButton:pressed {
    background-color: #343840;
}

#PrimaryButton {
    background-color: rgba(255, 255, 255, 0.16);
    color: white;
    border-radius: 14px;
    padding: 12px 18px;
    font-weight: 600;
}

#PrimaryButton:hover {
    background-color: rgba(255, 255, 255, 0.24);
}

QLineEdit {
    background-color: #2b2f36;
    border: 1px solid #3d434c;
    border-radius: 12px;
    padding: 10px 14px;
}

QLineEdit:focus {
    border: 1px solid #d9a7ff;
}

QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}

QListWidget::item {
    background-color: transparent;
    border: none;
    padding: 6px 0px;
    margin: 0px;
}

QListWidget::item:selected {
    background-color: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: #4a5059;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

#DiaryCard {
    background-color: #262a31;
    border: 1px solid transparent;
    border-radius: 18px;
}

#DiaryCard:hover {
    background-color: #2d3139;
    border: 1px solid #3c414b;
}

#DiaryCard[selected="true"] {
    background-color: #313540;
    border: 1px solid #d9a7ff;
}

#DiaryCardTitle {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    background: transparent;
}

#DiaryCardMood {
    font-size: 13px;
    color: #f3c8ff;
    background: transparent;
}

#DiaryCardDate {
    font-size: 12px;
    color: #aab2bf;
    background: transparent;
}

#DiaryCardSummary {
    font-size: 13px;
    color: #d4d8df;
    line-height: 1.5;
    background: transparent;
}
"""