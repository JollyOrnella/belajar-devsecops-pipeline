
"""Aplikasi Flask untuk simulasi deteksi SQL Injection."""

import sqlite3

from flask import Flask, request

app = Flask(__name__)


def get_db_connection():
    """Membuka koneksi database SQLite."""
    return sqlite3.connect("users.db")


@app.route("/login", methods=["GET"])
def login():
    """Simulasi login yang sengaja mengandung SQL Injection."""
    username = request.args.get("username")
    password = request.args.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Sengaja rentan untuk praktikum
    query = (
        "SELECT * FROM users WHERE username = '%s' "
        "AND password = '%s'"
    ) % (username, password)

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login berhasil"
    return "Login gagal"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
