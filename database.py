import sqlite3

def init_db():
    conn = sqlite3.connect("threats.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        risk_score INTEGER,
        reasons TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_scan(url, score, reasons):
    conn = sqlite3.connect("threats.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scans (url, risk_score, reasons) VALUES (?, ?, ?)",
        (url, score, ", ".join(reasons))
    )

    conn.commit()
    conn.close()


def get_all_scans():
    conn = sqlite3.connect("threats.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data
