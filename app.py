#!/usr/bin/env python3

from os.path import join
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
        if not 'filefield' in request.files or request.files['filefield'].filename == '':
            redirect(request.url)

        f = request.files['filefield']
            
        filename = join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(filename)
        info = f'Arquivo: {f.filename}'

        begin = 0.0
        end = -1.0
        if not 'begin' in request.form or not 'end' in request.form:
            redirect(request.url)

        if request.form['begin'] == '' or request.form['end'] == '':
            transcription = transcribe(filename)
            
        else:
            beginmm, beginss = request.form['begin'].split(':')
            endmm, endss = request.form['end'].split(':')

            begin = int(beginss) + int(beginmm) * 60 
            end = int(endss) + int(endmm) * 60 

            info = info + f' (trecho: {beginmm}:{beginss} a {endmm}:{endss})'
            transcription = transcribe(filename, begin=min(begin, end), end=max(begin, end))

    return render_template('trt8.html', transcription=transcription, info=info)

app.run(host="0.0.0.0", debug=True)
