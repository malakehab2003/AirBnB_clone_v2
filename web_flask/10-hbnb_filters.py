#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states: HTML page with a list of all State objects.
    /states/<id>: HTML page displaying the given state with <id>.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb():
    """use flask with airbnb website"""
    states = list(
        sorted(storage.all("State").values(), key=lambda x: x.name))
    amenities = list(
        sorted(storage.all("Amenity").values(), key=lambda x: x.name))
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)



@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
