"""
caffeine_tracker.py

Core logic for loading and processing the Starbucks caffeine dataset.
These functions are kept separate from the web app so they can be tested easily.
"""
import pandas as pd

# The public Starbucks dataset (caffeine content by drink and preparation)
CSV_URL = "https://raw.githubusercontent.com/reisanar/datasets/master/starbucks.csv"


def load_drinks(csv_url=CSV_URL):
    """
    Load the Starbucks CSV and return a cleaned list of drink dictionaries.

    Only drinks with a numeric caffeine value are kept (drinks labelled
    "varies" or with missing caffeine are excluded).

    Params:
        csv_url (str): the URL (or local path) of the CSV to load.

    Returns:
        list of dict: each dict has keys "beverage", "prep", and "caffeine".
    """
    df = pd.read_csv(csv_url)
    records = df.to_dict("records")

    drinks = []
    for row in records:
        caffeine = row["Caffeine (mg)"]
        # keep only rows where caffeine is a whole number
        if str(caffeine).isdigit():
            drinks.append({
                "beverage": row["Beverage"],
                "prep": row["Beverage_prep"],
                "caffeine": int(caffeine),
            })
    return drinks


def search_drinks(drinks, search_term):
    """
    Return the drinks whose beverage name contains the search term.

    Params:
        drinks (list of dict): the list returned by load_drinks().
        search_term (str): text to search for (case-insensitive).

    Returns:
        list of dict: the matching drinks.
    """
    term = search_term.lower()
    matches = []
    for drink in drinks:
        if term in drink["beverage"].lower():
            matches.append(drink)
    return matches


def total_caffeine(log):
    """
    Sum the caffeine of all drinks in a daily log.

    Params:
        log (list of dict): drinks the user has logged (each with "caffeine").

    Returns:
        int: total caffeine in mg.
    """
    return sum(drink["caffeine"] for drink in log)


def caffeine_status(total, limit=200):
    """
    Return a status describing how a caffeine total compares to a limit.

    Params:
        total (int): total caffeine consumed (mg).
        limit (int): the daily limit (mg). Defaults to 200 (pregnancy guideline).

    Returns:
        str: "under limit", "approaching limit", or "over limit".
    """
    if total > limit:
        return "over limit"
    elif total >= limit * 0.75:
        return "approaching limit"
    else:
        return "under limit"


def drink_label(drink):
    """
    Build a human-readable label for a drink, used in the dropdown menu.

    Params:
        drink (dict): a drink with "beverage", "prep", and "caffeine" keys.

    Returns:
        str: e.g. "Brewed Coffee - Venti (410 mg)".
    """
    return f"{drink['beverage']} - {drink['prep']} ({drink['caffeine']} mg)"

def make_gauge_html(total, limit=200):
    """
    Build a Plotly gauge chart showing the caffeine total against the limit,
    and return it as an HTML snippet that can be embedded in a web page.

    The gauge has a green "safe" zone up to the limit and a red zone beyond it,
    with a marker showing the limit itself.

    Params:
        total (int): total caffeine consumed today (mg).
        limit (int): the daily limit (mg). Defaults to 200.

    Returns:
        str: an HTML snippet containing the chart.
    """
    import plotly.graph_objects as go

    # The gauge axis goes a bit beyond the higher (breastfeeding) limit so the
    # needle still shows even if the user goes well over.
    axis_max = 400

    figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total,
        number={"suffix": " mg"},
        title={"text": "Today's Caffeine"},
        gauge={
            "axis": {"range": [0, axis_max]},
            "bar": {"color": "#333333"},
            "steps": [
                {"range": [0, limit], "color": "#d4edda"},        # green safe zone
                {"range": [limit, axis_max], "color": "#f8d7da"},  # red over zone
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": limit,
            },
        },
    ))
    figure.update_layout(height=300, margin={"t": 40, "b": 10, "l": 20, "r": 20})

    # include_plotlyjs="cdn" loads the Plotly library from the internet, so we
    # don't have to bundle it. full_html=False gives just the chart snippet.
    return figure.to_html(full_html=False, include_plotlyjs="cdn")
