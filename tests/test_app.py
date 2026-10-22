
"""Pengujian otomatis aplikasi Flask menggunakan Pytest."""

import pytest

from app import app


@pytest.fixture
def client():
    """Membuat Flask test client."""
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_homepage(client):
    """Memastikan halaman utama berhasil dibuka."""
    response = client.get("/")
    assert response.status_code == 200


def test_login_form(client):
    """Memastikan formulir login tersedia."""
    response = client.get("/")

    assert b"username" in response.data
    assert b"password" in response.data
    assert b"csrf_token" in response.data


def test_csrf_protection(client):
    """Memastikan POST tanpa token CSRF ditolak."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "password_salah",
        },
    )

    assert response.status_code == 400


def test_invalid_route(client):
    """Memastikan URL tidak dikenal menghasilkan 404."""
    response = client.get("/halaman-tidak-ada")
    assert response.status_code == 404
