# -*- coding: utf-8 -*-
try:
    from os import getuid

except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'The about page'


if __name__ == "__main__":
    app.run(port=getuid() + 1000)
