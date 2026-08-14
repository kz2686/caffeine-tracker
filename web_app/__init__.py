"""
The web_app package defines the Flask web application.

It uses the "application factory" pattern: the create_app() function builds and
returns the Flask app. This is why the app is started with `FLASK_APP=web_app`
and `flask run` (Flask looks for create_app automatically).
"""
from flask import Flask, render_template


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def home():
        """Render the home page."""
        return render_template("index.html")

    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
