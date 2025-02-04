#!/usr/bin/python3
""" start a web flas application"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """say hello"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """say HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """say c and text"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", strict_slashes=False, defaults={'text': 'is cool'})
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """say python and text"""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """say n if int"""
    return "{} is a number".format(int(n))


if __name__ == "__main__":
    """if module run as main"""
    app.run(host='0.0.0.0', port=5000)
