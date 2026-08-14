"""
Tests for the core caffeine_tracker functions.

These tests use small, hardcoded sample data instead of downloading the real
CSV, so they run fast and don't make unnecessary network requests (as the
assignment recommends).
"""
from app.caffeine_tracker import search_drinks, total_caffeine, caffeine_status


# Sample data that mimics the structure returned by load_drinks()
SAMPLE_DRINKS = [
    {"beverage": "Brewed Coffee", "prep": "Venti", "caffeine": 410},
    {"beverage": "Caffè Latte", "prep": "Tall", "caffeine": 75},
    {"beverage": "Caffè Americano", "prep": "Grande", "caffeine": 225},
    {"beverage": "Iced Coffee", "prep": "Tall", "caffeine": 120},
]


def test_search_drinks_finds_match():
    """Searching for 'latte' should find the Caffè Latte."""
    results = search_drinks(SAMPLE_DRINKS, "latte")
    assert len(results) == 1
    assert results[0]["beverage"] == "Caffè Latte"


def test_search_drinks_is_case_insensitive():
    """Searching should work regardless of capitalization."""
    results = search_drinks(SAMPLE_DRINKS, "COFFEE")
    # "Brewed Coffee" and "Iced Coffee" both contain "coffee"
    assert len(results) == 2


def test_search_drinks_no_match():
    """Searching for something not present returns an empty list."""
    results = search_drinks(SAMPLE_DRINKS, "tea")
    assert results == []


def test_total_caffeine():
    """Total caffeine should be the sum of the drinks' caffeine."""
    log = [SAMPLE_DRINKS[1], SAMPLE_DRINKS[3]]  # 75 + 120
    assert total_caffeine(log) == 195


def test_total_caffeine_empty():
    """An empty log has a total of 0."""
    assert total_caffeine([]) == 0


def test_caffeine_status_under():
    """A low total should be under the limit."""
    assert caffeine_status(100, limit=200) == "under limit"


def test_caffeine_status_approaching():
    """A total at 75% or more of the limit is approaching."""
    assert caffeine_status(160, limit=200) == "approaching limit"


def test_caffeine_status_over():
    """A total above the limit is over."""
    assert caffeine_status(250, limit=200) == "over limit"
