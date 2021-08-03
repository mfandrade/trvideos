#!/usr/bin/env python3

from flask import Flask, request, render_template
from transcribe import transcribe

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello world!'

@app.route('/', methods=['GET', 'POST'])
def index():
    text = '(blank)'
    if request.method == 'POST':
        text = transcribe('2021-07-01-114242.webm')

    return render_template('form.html', text=text)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return 'Called via POST method. Well done!'
    else:
        return 'GET method. Duh...'

app.run(host="0.0.0.0")
