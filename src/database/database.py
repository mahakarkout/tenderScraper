import sqlite3
from typing import List, Dict

DB_NAME = "tenders.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tenders (
        tender_id TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        start_date TEXT,
        end_date TEXT,
        end_time TEXT,
        region TEXT,
        city TEXT,
        price TEXT,
        categories TEXT,
        category_urls TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_to_db(tenders: List[Dict]):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for t in tenders:
        cursor.execute("""
        INSERT OR REPLACE INTO tenders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["tender_id"], t["title"], t["url"], t["start_date"], t["end_date"],
            t["end_time"], t["region"], t["city"], t["price"],
            ", ".join(t["categories"]),
            ", ".join(t["category_urls"])
        ))
    conn.commit()
    conn.close()

def load_all_tenders() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tenders")
    rows = cursor.fetchall()
    conn.close()

    columns = [
        "tender_id", "title", "url", "start_date", "end_date", "end_time",
        "region", "city", "price", "categories", "category_urls"
    ]
    return [dict(zip(columns, row)) for row in rows]
