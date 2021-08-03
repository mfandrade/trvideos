#!/usr/bin/env python3

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello world!'

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return 'Called via POST method. Well done!'
    else:
        return 'GET method. Duh...'

app.run(host="0.0.0.0")
