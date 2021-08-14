#!/usr/bin/env python3

from flask import Flask, request, render_template
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
        if 'filefield' in request.files:
            f = request.files['filefield']
            f.save(secure_filename(f.filename))
            transcription = transcribe(f.filename)
            info = f'Arquivo: {f.filename}'
        if 'begin' in request.form and 'end' in request.form:
            begin = request.form['begin']
            end = request.form['end']
            if len(begin) > 0 and len(end) > 0:
                info += f' (trecho: {begin}-{end})'

    return render_template('trt8.html', transcription=transcription, info=info)

app.run(host="0.0.0.0", debug=True)
