
from flask import Flask, render_template, request, redirect
import webview
from db import init_db, insert_record, get_all_records, get_summary_by_category, get_daily_totals, get_records_by_date
from flask import jsonify
import sqlite3

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    records = get_all_records()
    summary = get_summary_by_category()
    categories = [row[0] for row in summary]
    totals = [row[1] for row in summary]
    return render_template('index.html', records=records, categories=categories, totals=totals)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    note = request.form['note']
    insert_record(date, category, amount, note)
    return redirect('/')

@app.route('/calendar-data')
def calendar_data():
    daily_data = get_daily_totals()
    events = []
    for date, total in daily_data:
        events.append({
            'title': f"{total:.0f} 元",
            'start': date,
            'color': "#2ecc71" if total > 0 else "#e74c3c"
        })
    return jsonify(events)

@app.route('/records/<date>')
def records_by_date(date):
    data = get_records_by_date(date)
    return jsonify(data)

@app.route('/chart-data')
def chart_data():
    start = request.args.get('start')
    end = request.args.get('end')

    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''
        SELECT category, SUM(amount)
        FROM records
        WHERE date BETWEEN ? AND ?
        GROUP BY category
    ''', (start, end))
    rows = c.fetchall()
    conn.close()

    labels = [r[0] for r in rows]
    totals = [r[1] for r in rows]
    return jsonify({'labels': labels, 'totals': totals})

@app.route('/get-range')
def get_range():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT MIN(date), MAX(date) FROM records')
    start, end = c.fetchone()
    conn.close()
    return jsonify({'start': start, 'end': end})

@app.route('/delete-all', methods=['POST'])
def delete_all():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('DELETE FROM records')
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    webview.create_window("個人記帳本", app, width=1000, height=700)
    webview.start()
