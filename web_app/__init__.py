"""
The web_app package defines the Flask web application.

It uses the "application factory" pattern: the create_app() function builds and
returns the Flask app. This is why the app is started with `FLASK_APP=web_app`
and `flask run` (Flask looks for create_app automatically).
"""
from flask import Flask, render_template, request, redirect, url_for

from app.caffeine_tracker import (
    load_drinks,
    total_caffeine,
    caffeine_status,
    drink_label,
)

# The daily caffeine limit for pregnancy (mg). Used to judge the running total.
DAILY_LIMIT = 200


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load the drink data once, when the app starts.
    drinks = load_drinks()

    # The user's log of drinks consumed today. Resets when the app restarts.
    # (Persisting this across sessions is listed as future work.)
    daily_log = []

    @app.route("/")
    def home():
        """Show the drink picker, the day's log, and the running total."""
        total = total_caffeine(daily_log)
        status = caffeine_status(total, DAILY_LIMIT)
        return render_template(
            "index.html",
            drinks=drinks,
            drink_label=drink_label,
            daily_log=daily_log,
            total=total,
            status=status,
            limit=DAILY_LIMIT,
        )

    @app.route("/add", methods=["POST"])
    def add():
        """Add the selected drink to the daily log, then return to the home page."""
        # The dropdown sends the index of the chosen drink in the drinks list.
        selected = request.form.get("drink_index")
        if selected is not None and selected.isdigit():
            index = int(selected)
            if 0 <= index < len(drinks):
                daily_log.append(drinks[index])
        return redirect(url_for("home"))

    @app.route("/reset", methods=["POST"])
    def reset():
        """Clear the daily log so the user can start a new day."""
        daily_log.clear()
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)

