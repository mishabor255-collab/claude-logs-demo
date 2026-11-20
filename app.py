"""
Мини-сайт со страницей входа — учебный пример «сайт лёг, пусть Claude сам прочитает логи».

Запуск:  python3 app.py   ->  откройте http://localhost:8000
Логин для проверки: demo / demo123

Сайт специально «сломан»: в файле .env не хватает одной настройки.
Задача — не искать ошибку руками, а попросить Claude Code найти причину в logs/app.log и исправить.
Внешние библиотеки не нужны: только стандартный Python 3.9+.
"""
import hashlib
import html
import logging
import os
import sqlite3
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(ROOT, "logs", "app.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("app")


def load_env(path=os.path.join(ROOT, ".env")):
    """читает настройки из файла .env (строки вида КЛЮЧ=значение)"""
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def db_path():
    url = os.environ["DATABASE_URL"]
    if not url.startswith("sqlite:///"):
        raise ValueError(f"Поддерживается только sqlite:///путь, получено: {url}")
    return os.path.join(ROOT, url[len("sqlite:///"):])


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    path = db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE IF NOT EXISTS users (login TEXT PRIMARY KEY, password TEXT)")
    con.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ("demo", hash_pw("demo123")))
    con.commit()
    return con


PAGE = """<!doctype html><html lang="ru"><meta charset="utf-8">
<title>Demo login</title>
<style>body{{font-family:system-ui;background:#141b33;color:#f2f2f2;display:grid;place-items:center;height:100vh;margin:0}}
form{{background:#1e2a4f;padding:32px;border-radius:16px;display:grid;gap:12px;width:280px}}
input,button{{padding:10px;border-radius:8px;border:0;font-size:16px}}button{{background:#f07a2a;color:#fff;cursor:pointer}}
.msg{{color:{color};min-height:1em}}</style>
<form method="post" action="/login"><h2>Вход</h2>
<input name="login" placeholder="логин" value="demo"><input name="password" type="password" placeholder="пароль">
<button>Войти</button><div class="msg">{msg}</div></form></html>"""


class Handler(BaseHTTPRequestHandler):
    def page(self, code, msg="", color="#ffb067"):
        body = PAGE.format(msg=html.escape(msg), color=color).encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.page(200)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode())
        login = form.get("login", [""])[0]
        password = form.get("password", [""])[0]
        try:
            con = get_db()
            row = con.execute("SELECT password FROM users WHERE login = ?", (login,)).fetchone()
            if row and row[0] == hash_pw(password):
                log.info("login ok user=%s", login)
                self.page(200, f"Добро пожаловать, {login}!", "#3ccb7f")
            else:
                log.warning("login failed user=%s (wrong password)", login)
                self.page(401, "Неверный логин или пароль")
        except Exception:
            log.error("login crashed user=%s\n%s", login, traceback.format_exc())
            self.page(500, "Что-то пошло не так. Попробуйте позже.", "#e5484d")

    def log_message(self, fmt, *args):     # не засоряем терминал запросами
        pass


if __name__ == "__main__":
    load_env()
    port = int(os.environ.get("PORT", "8000"))
    log.info("server started on port %s", port)
    print(f"Сайт запущен: http://localhost:{port}  (логин demo / demo123). Остановить: Ctrl+C")
    try:
        HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
