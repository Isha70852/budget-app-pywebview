import webview
from threading import Thread
from app import app  # 這是你的 Flask app

def start_flask():
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    t = Thread(target=start_flask)
    t.daemon = True
    t.start()
    webview.create_window("個人記帳本", "http://127.0.0.1:5000", width=1000, height=700)
    webview.start()
    