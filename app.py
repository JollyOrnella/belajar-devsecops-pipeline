
"""Aplikasi Flask untuk praktikum DevSecOps."""

import os
import sqlite3

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

CSRFProtect(app)

DATABASE = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    """Membuat database dan akun demonstrasi praktikum."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
            """
        )

        demo_password = os.environ.get("DEMO_PASSWORD")
        if demo_password:
            conn.execute(
                """
                INSERT OR IGNORE INTO users
                (username, password_hash)
                VALUES (?, ?)
                """,
                ("admin", generate_password_hash(demo_password)),
            )


@app.route("/", methods=["GET", "POST"])
def index():
    """Menampilkan formulir login dan memproses autentikasi."""
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        with sqlite3.connect(DATABASE) as conn:
            user = conn.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        if user and check_password_hash(user[0], password):
            message = "Login berhasil! Selamat datang."
            status_class = "success"
        else:
            message = "Login gagal! Kredensial tidak valid."
            status_class = "danger"

    return render_template(
        "index.html",
        message=message,
        status_class=status_class,
    )


if __name__ == "__main__":
    init_db()
    app.run()
