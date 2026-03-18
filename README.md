# 🌙 Mood Diary

一个精美的本地心情日记桌面应用  
A beautiful local mood diary desktop app built with PySide6

---

## ✨ 项目亮点

- 🎨 **精美 UI 设计**：卡片式日记 + 深色主题
- 😊 **情绪记录**：支持记录每日心情
- 🔍 **搜索功能**：快速查找历史日记
- 📊 **数据统计**：
  - 情绪分布
  - 最近 7 天写作热度
- 🖼️ **导出为精美图片**：
  - 多模板（夜幕 / 奶油 / 极简）
  - 支持导出分享
- 👀 **导出预览功能**
- 💻 **Windows 原生应用（已打包）**

---

## 📸 界面预览
/images 

---

## 🧰 技术栈

- Python 3
- PySide6（Qt）
- SQLite（本地数据库）
- PyInstaller（打包）
- Inno Setup（安装包）

---

## 🚀 如何运行（开发模式）

```bash
pip install PySide6
python app.py
📦 如何使用（普通用户）

👉 下载发布版本（exe / 安装包）

双击运行 MoodDiary.exe

或运行安装包安装

开始记录你的心情

📂 项目结构
mood_diary/
├── ui/            # 界面组件
├── data/          # 数据库逻辑
├── utils/         # 工具函数（图片导出等）
├── models/        # 数据模型
├── resources/     # 图标资源
├── app.py         # 程序入口
🎯 功能说明
📝 日记功能

新建 / 编辑 / 删除

卡片式展示

支持情绪标签

🔍 搜索

关键词搜索日记内容

📊 统计分析

情绪占比

最近 7 天活跃度

🖼️ 图片导出

多模板风格

导出为 PNG

支持预览
🔮 未来计划

🔐 日记加密 / 密码锁

☁️ 云同步

🎨 更多主题

📱 移动端版本

🔔 每日提醒
📌 作者

GitHub: https://github.com/dissdannm
⭐ 如果你觉得这个项目不错

欢迎 Star ⭐ 支持一下！
