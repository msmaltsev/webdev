# -*- coding: utf-8 -*-
try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template, render_template_string, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open('templates/index.html', 'r', encoding="utf-8") as f:
        index_template = process_index(f.read())
    return render_template_string(index_template)

@app.route("/post")
def post_message():
    with open('templates/post.html', 'r', encoding="utf-8") as f:
        index_template = process_index(f.read())
    return render_template_string(index_template)  

def get_message_template():
    with open('templates/message.html', 'r', encoding="utf-8") as f:
        return f.read()

def process_index(index_template):
    for processor in [messages_block]:
        index_template = processor(index_template)
    return index_template

def load_messages():
    with open('data/messages.json', 'r', encoding='utf-8') as messages_file:
        try:
            messages_json = json.load(messages_file)
        except:
            return []
    return messages_json

def message_htmlfy(message, message_template):
    for key in message:
        message_template = message_template.replace('%{0}%'.format(key), message[key])
    return message_template

def messages_block(index_template="%messages_content%"):
    messages_json = load_messages()
    message_template = get_message_template()
    if messages_json:
        replacer = []
        for message in messages_json:
            replacer.append(message_htmlfy(message, message_template))
        replacer = "<br/>".join(replacer)
    else:
        replacer = "No messages"
    return index_template.replace("%messages_content%", replacer)


if __name__ == "__main__":
    app.run(port=getuid() + 1000)
