import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path("mood_diary.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diary_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        mood TEXT,
        theme TEXT DEFAULT 'night',
        created_at TEXT NOT NULL,
        updated_at TEXT
    )
    """)

    cursor.execute("PRAGMA table_info(diary_entries)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "updated_at" not in columns:
        cursor.execute("ALTER TABLE diary_entries ADD COLUMN updated_at TEXT")

    if "theme" not in columns:
        cursor.execute("ALTER TABLE diary_entries ADD COLUMN theme TEXT DEFAULT 'night'")

    conn.commit()
    conn.close()


def add_entry(title, content, mood, theme="night"):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO diary_entries (title, content, mood, theme, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, content, mood, theme, now, now))

    conn.commit()
    conn.close()


def update_entry(entry_id, title, content, mood, theme="night"):
    conn = get_connection()
    cursor = conn.cursor()

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    UPDATE diary_entries
    SET title = ?, content = ?, mood = ?, theme = ?, updated_at = ?
    WHERE id = ?
    """, (title, content, mood, theme, updated_at, entry_id))

    conn.commit()
    conn.close()


def delete_entry(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM diary_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def get_all_entries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, content, mood, theme, created_at, updated_at
    FROM diary_entries
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def search_entries(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    like_keyword = f"%{keyword.strip()}%"

    cursor.execute("""
    SELECT id, title, content, mood, theme, created_at, updated_at
    FROM diary_entries
    WHERE title LIKE ?
       OR content LIKE ?
       OR mood LIKE ?
       OR created_at LIKE ?
       OR theme LIKE ?
    ORDER BY created_at DESC
    """, (like_keyword, like_keyword, like_keyword, like_keyword, like_keyword))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_entry_by_id(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, content, mood, theme, created_at, updated_at
    FROM diary_entries
    WHERE id = ?
    """, (entry_id,))

    row = cursor.fetchone()
    conn.close()
    return row


def get_stats_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM diary_entries")
    total = cursor.fetchone()["total"]

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    SELECT COUNT(*) AS recent_count
    FROM diary_entries
    WHERE created_at >= ?
    """, (seven_days_ago,))
    recent_count = cursor.fetchone()["recent_count"]

    cursor.execute("""
    SELECT mood, COUNT(*) AS count
    FROM diary_entries
    GROUP BY mood
    ORDER BY count DESC
    """)
    mood_rows = cursor.fetchall()

    mood_stats = []
    for row in mood_rows:
        mood_stats.append({
            "mood": row["mood"] or "未填写",
            "count": row["count"]
        })

    top_mood = mood_stats[0]["mood"] if mood_stats else "--"

    conn.close()

    return {
        "total": total,
        "recent_count": recent_count,
        "top_mood": top_mood,
        "mood_stats": mood_stats
    }


def get_last_7_days_activity():
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()
    start_day = today - timedelta(days=6)

    cursor.execute("""
    SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS count
    FROM diary_entries
    WHERE created_at >= ?
    GROUP BY substr(created_at, 1, 10)
    ORDER BY day ASC
    """, (f"{start_day} 00:00:00",))

    rows = cursor.fetchall()
    count_map = {row["day"]: row["count"] for row in rows}

    weekday_map = {
        0: "周一",
        1: "周二",
        2: "周三",
        3: "周四",
        4: "周五",
        5: "周六",
        6: "周日",
    }

    result = []
    for i in range(7):
        day_obj = start_day + timedelta(days=i)
        day_str = day_obj.strftime("%Y-%m-%d")
        result.append({
            "date": day_str,
            "label": day_obj.strftime("%m-%d"),
            "weekday": weekday_map[day_obj.weekday()],
            "count": count_map.get(day_str, 0)
        })

    conn.close()
    return result