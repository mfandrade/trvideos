#!/usr/bin/env python3

from flask import Flask, redirect, request, render_template
from werkzeug.utils import secure_filename
from transcribe import transcribe

app = Flask(__name__)
app.config['UPLOAD_FOLDER']    = '/tmp'
app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024

@app.route('/hello')
def hello():
    return 'Hello world!'

@app.route('/', methods=['GET', 'POST'])
def index():

    transcription = ''
    info = ''

    if request.method == 'POST':
        if not 'filefield' in request.files:
            redirect(request.url)

        else:
            f = request.files['filefield']
            filename = secure_filename(f.filename)
            f.save(filename)

            info = f'Arquivo: {filename}'

        begin = 0.0
        end = -1.0
        if 'begin' in request.form and 'end' in request.form:
            begin = abs(min(float(request.form['begin'], float(request.form['end']))))
            end = abs(max(float(request.form['begin'], float(request.form['end']))))
            
            info = info + f' (trecho: {begin} a {end})'

        transcription = transcribe(filename, begin=begin, end=end)

    return render_template('trt8.html', transcription=transcription, info=info)

app.run(host="0.0.0.0", debug=True)
