from datetime import datetime
import babel.dates
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_htmx import HTMX

app = Flask(__name__)
app.config["SECRET_KEY"] = "jdiwdjqwoiwidjw"
app.config["TEMPLATES_AUTO_RELOAD"] = True
htmx = HTMX(app)
toolbar = DebugToolbarExtension(app)

# Set the FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"


@app.template_filter()
def format_datetime(value, format="medium"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    if format == "full":
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == "medium":
        format = "dd/MM/y HH:mm:ss"
    return babel.dates.format_datetime(value, format)


@app.route("/events/search", methods=["GET"])
def search_events():
    query = request.args.get("query")
    events = requests.get(f"{FASTAPI_URL}/events/search?query={query}").json()
    return render_template(
        "partials/events_table.html",
        events=events,
    )


@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
