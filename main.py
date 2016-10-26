# -*- coding: utf-8 -*-
try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template_string, request, redirect
import json, datetime

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    with open('templates/index.html', 'r', encoding="utf-8") as f:
        index_template = process_index(f.read())
    return render_template_string(index_template)

@app.route("/post", methods=['GET','POST'])
def post_message():
    with open('templates/post.html', 'r', encoding="utf-8") as f:
        index_template = process_index(f.read())
    return render_template_string(index_template)

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
    with open('templates/about.html', 'r', encoding="utf-8") as f:
        index_template = process_index(f.read())
    return render_template_string(index_template)

def get_html_template(filename):
    with open('templates/%s' % filename, 'r', encoding="utf-8") as f:
        return f.read()

def process_index(index_template):
    for processor in [messages_block]:
        index_template = processor(index_template)
    return index_template

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
    return messages_json

def save_messages(messages_json):
    fin = json.dumps(messages_json, indent=4)
    with open('data/messages.json', 'w', encoding='utf-8') as f:
        f.write(fin)


def message_htmlfy(message, message_template):
    for key in message:
        message_template = message_template.replace('%{0}%'.format(key), message[key])
    return message_template

def messages_block(index_template="%messages_content%"):
    messages_json = load_messages()
    message_template = get_html_template("message.html")
    if messages_json:
        replacer = []
        for message in reversed(messages_json):
            replacer.append(message_htmlfy(message, message_template))
        replacer = "<br/>".join(replacer)
    else:
        replacer = "No messages"
    return index_template.replace("%messages_content%", replacer)

if __name__ == "__main__":
    app.run(port=getuid() + 1000)
