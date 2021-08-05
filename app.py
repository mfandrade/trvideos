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
        f = request.files['filefield']
        f.save(secure_filename(f.filename))
        transcription = transcribe(f.filename)
        info = f'Arquivo: {f.filename}'

    return render_template('form.html', transcription=transcription, info=info)

app.run(host="0.0.0.0", debug=True)
