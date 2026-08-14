"""
Tests for the Flask web app.
"""
from web_app import create_app


def test_home_page():
    """The home page should load successfully (status 200)."""
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_shows_title():
    """The home page should contain the app title."""
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"Caffeine Tracker" in response.data
