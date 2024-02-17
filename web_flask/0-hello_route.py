#!/usr/bin/python3
""" start a web flas application"""
from flask import Flask


app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    """say hello"""
    return "Hello HBNB!"

if __name__ == "__main":
    """if module run as main"""
    app.run(port=5000, host='0.0.0.0')
