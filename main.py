# -*- coding: utf-8 -*-
try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template, request, redirect
import json, datetime

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('index.html', messages_json=load_messages())


@app.route("/post", methods=['GET','POST'])
def post_message():
    return render_template('post.html', messages_json=load_messages())


@app.route("/get_text", methods=['POST'])
def get_text():
    if request.method == 'POST':
        text = request.form['message']
        title = request.form['title']
        date = datetime.datetime.now().strftime('%d.%m.%y, %H:%M')
        messages_json = load_messages()
        id_ = len(messages_json)
        messages_json.append({'id':str(id_), 'title':title, 'text':text, 'date':date})
        save_messages(messages_json)
    return redirect('/')


@app.route("/remove_msg", methods=['GET', 'POST'])
def remove_msg():
    if request.method == 'POST':
        id = request.form['id']
        remove_msg_from_json(id)
    return redirect('/')


@app.route("/about")
def about():
    return render_template('about.html')


def remove_msg_from_json(id):
    messages_json = load_messages()
    for msg in messages_json:
        if msg["id"] == id:
            messages_json.remove(msg)
            break
    save_messages(messages_json)


def load_messages():
    with open('data/messages.json', 'r', encoding='utf-8') as messages_file:
        try:
            messages_json = json.load(messages_file)
        except:
            return []
    return messages_json[::-1]


def save_messages(messages_json):
    fin = json.dumps(messages_json, indent=4)
    with open('data/messages.json', 'w', encoding='utf-8') as f:
        f.write(fin)


if __name__ == "__main__":
    app.run(port=getuid() + 1000)
