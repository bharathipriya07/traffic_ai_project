import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "challan.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT NOT NULL,
        violation TEXT NOT NULL,
        fine INTEGER NOT NULL DEFAULT 0,
        image TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Get existing columns
    cursor.execute("PRAGMA table_info(challans)")
    columns = [row[1] for row in cursor.fetchall()]

    # Add missing columns dynamically (VERY IMPORTANT 🔥)
    if "image" not in columns:
        cursor.execute("ALTER TABLE challans ADD COLUMN image TEXT")

    if "date" not in columns:
        cursor.execute("ALTER TABLE challans ADD COLUMN date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    conn.commit()
    conn.close()


def insert_challan(vehicle, violation, fine, image=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO challans (vehicle_number, violation, fine, image)
    VALUES (?, ?, ?, ?)
    """, (vehicle, violation, fine, image))

    conn.commit()
    conn.close()


def fetch_violations(search_vehicle=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM challans"
    params = []

    if search_vehicle:
        query += " WHERE vehicle_number LIKE ?"
        params.append(f"%{search_vehicle}%")

    # Safe ordering (date column always exists now ✅)
    query += " ORDER BY date DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def fetch_totals(search_vehicle=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        COUNT(*) as violation_count, 
        COALESCE(SUM(fine), 0) as total_fine 
    FROM challans
    """
    params = []

    if search_vehicle:
        query += " WHERE vehicle_number LIKE ?"
        params.append(f"%{search_vehicle}%")

    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()

    return {
        "violation_count": result["violation_count"],
        "total_fine": result["total_fine"],
    }