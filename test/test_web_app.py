"""
Tests for the Flask web app.
"""
from web_app import create_app


def make_client():
    """Helper: create a fresh test client for the app."""
    app = create_app()
    return app.test_client()


def test_home_page():
    """The home page should load successfully (status 200)."""
    client = make_client()
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_shows_title():
    """The home page should contain the app title."""
    client = make_client()
    response = client.get("/")
    assert b"Caffeine Tracker" in response.data


def test_home_page_shows_dropdown():
    """The home page should include a drink selection dropdown."""
    client = make_client()
    response = client.get("/")
    assert b"Choose a drink" in response.data


def test_add_drink_updates_total():
    """Adding a drink should increase the total shown on the page."""
    client = make_client()
    # Add the first drink (index 0) to the log
    client.post("/add", data={"drink_index": "0"})
    response = client.get("/")
    # After adding a drink, the page should no longer say the log is empty
    assert b"No drinks logged yet" not in response.data


def test_reset_clears_log():
    """Resetting should clear the daily log."""
    client = make_client()
    client.post("/add", data={"drink_index": "0"})
    client.post("/reset")
    response = client.get("/")
    assert b"No drinks logged yet" in response.data
