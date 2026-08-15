# Caffeine Tracker

A Flask web application that helps pregnant and breastfeeding women track their
daily caffeine intake from Starbucks drinks and check whether they stay within
recommended health guidelines (200 mg per day during pregnancy).

Most single Starbucks drinks are within safe caffeine limits — the real risk
comes from **cumulative** intake across several drinks in a day. This tracker
makes that running total visible.

## Features

- Pick from a dropdown of real Starbucks drinks (name, size, and caffeine shown)
- Add drinks to a running daily log
- See the cumulative caffeine total update as you add drinks
- Get a color-coded safety status (under / approaching / over the limit)
- View an interactive Plotly gauge chart of your total against the limit
- Reset to start a new day

## Data Source

Starbucks nutritional data from a public CSV file:
https://github.com/reisanar/datasets/blob/master/starbucks.csv

The caffeine column is stored as text and contains some non-numeric values
(such as "varies") and blanks. The app cleans the data by keeping only drinks
that have a numeric caffeine value.

## Tech Stack

- **Python** with **Flask** (web framework)
- **pandas** (loading and cleaning the data)
- **Plotly** (the interactive gauge chart)
- **pytest** (automated tests)

## Setup

These instructions are for macOS.

### 1. Clone the repository

Open the Terminal app and run:

```
git clone https://github.com/kz2686/caffeine-tracker.git
cd caffeine-tracker
```

### 2. Create and activate a virtual environment (via Anaconda)

```
conda create --name caffeine python=3.11
conda activate caffeine
```

### 3. Install the dependencies (via Pip)

```
pip install -r requirements.txt
```

## Running the App

```
FLASK_APP=web_app flask run
```

Then hold **Cmd** and click the link shown in the Terminal (usually
http://127.0.0.1:5000), or copy and paste it into your web browser.

To stop the app, press **Control + C** in the Terminal.

**Note:** The gauge chart loads the Plotly library from the internet, so viewing
the page requires an internet connection.

## Running the Tests

```
pytest
```

This runs the full test suite (15 tests covering the data functions and the web
app). The tests use small sample data instead of downloading the CSV, so they
run quickly and without unnecessary network requests.

## Environment Variables

This application does not require any secret credentials or API keys, since it
uses a public dataset. If secrets are added in the future, they should be stored
in a local `.env` file, which is kept out of version control by `.gitignore`.

## Project Structure

```
caffeine-tracker/
├── app/
│   ├── __init__.py
│   └── caffeine_tracker.py   # data loading, cleaning, and caffeine logic
├── web_app/
│   ├── __init__.py           # the Flask app (create_app factory)
│   └── templates/
│       └── index.html        # the web page
├── test/
│   ├── test_caffeine_data.py # tests for the caffeine logic
│   └── test_web_app.py       # tests for the web app
├── .github/workflows/
│   └── python-app.yml        # GitHub Actions CI (lint + tests)
├── conftest.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Continuous Integration

This repository uses GitHub Actions (see `.github/workflows/python-app.yml`) to
automatically check the code with flake8 and run the tests every time code is
pushed or a pull request is opened.

## Known Limitations / Future Work

- The daily log is stored in memory and resets when the app restarts. Saving
  history across sessions (to a file or database) is future work.
- Drinks with "varies" caffeine (some tea lattes) are excluded.
- Currently uses the 200 mg pregnancy limit; a future version could let the user
  choose the breastfeeding limit instead.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
