#!/usr/bin/env python3

from flask import Flask, request, render_template
from transcribe import transcribe
import time
import json

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello world!'

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ''
    if request.method == 'POST':
        transcription = transcribe('2021-07-01-114242.webm')

    return render_template('form.html', transcription=transcription)

@app.route('/process', methods=['POST'])
def process():
    time.sleep(5)
    res = {'status': 'success', 'message': 'Hello world!'}
    return json.dumps(res)
    

app.run(host="0.0.0.0")
