# -*- coding: utf-8 -*-

try:
    from os import getuid

except ImportError:
    def getuid():
        return 4000

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return '''Hello from Flask!
<a href="/projects/">PROJECTS</a>'''

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'



if __name__ == "__main__":
    app.run(port=getuid() + 1000)
