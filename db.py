import sqlite3

def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(date, category, amount, note):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('INSERT INTO records (date, category, amount, note) VALUES (?, ?, ?, ?)',
              (date, category, amount, note))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT date, category, amount, note FROM records ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_summary_by_category():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM records GROUP BY category')
    data = c.fetchall()
    conn.close()
    return data

def get_daily_totals():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT date, SUM(amount) FROM records GROUP BY date')
    result = c.fetchall()
    conn.close()
    return result

def get_records_by_date(date):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT category, amount, note FROM records WHERE date = ?', (date,))
    rows = c.fetchall()
    conn.close()
    return rows

