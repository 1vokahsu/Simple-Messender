from flask import Flask, render_template, request
import json
from datetime import datetime

#func download messages from file
def load_message():
    with open('db.json', 'r') as json_file:
        data = json.load(json_file)
    return data['messages']

#func for add new messages
def add_message(sender, text):
    new_message = {
        'text': text,
        'sender': sender,
        'time': datetime.now().strftime('%H:%M')
    }
    all_messages.append(new_message)

#func for save to file
def save_messages():
    data = {
        'messages': all_messages
    }
    with open('db.json', 'w') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


all_messages = load_message()

app = Flask(__name__)  # create new app

@app.route('/index') #127.0.0.1/index > Hello world!
def index_page():
    return 'Hello world!'

@app.route('/chat')
def display_chat():
    return render_template('form.html')

@app.route('/get_messages')
def get_messages():
    return {'messages': all_messages}

@app.route('/send_message')
def send_message():
    sender = request.args['name']
    text = request.args['text']
    add_message(sender, text)
    save_messages()
    return 'OK'

@app.route('/status')
def status():
    mes_count = len(all_messages)
    user_count = 0
    users = []
    for i in all_messages:
        if i['sender'] not in users:
            users.append(i['sender'])

    return f"Кол-во пользователей: {len(users)}\nКол-во сообщений: {mes_count}"

app.run(host='0.0.0.0', port=80) #running server