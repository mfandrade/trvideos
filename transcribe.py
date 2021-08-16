#!/usr/bin/env python3
#
#- OK cortar video
#- OK extrair áudio do vídeo
#- OK mixar canais de áudio
#- TODO: reduzir ruído, acentuar volume
#        - sr.Recognizer().energy_threshold = 4000 - aumenta o nível
#- OK quebrar em trechos menores que 2min
#- OK transcrever trechos

def cut_video(videopath, start, end):
    
    from os.path import splitext
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

    # https://github.com/Zulko/moviepy/blob/cd473ff77ca630fe53fcac74d5c63da188594240/moviepy/video/io/ffmpeg_tools.py#L33
    name, ext = splitext(videopath)
    t1, t2 = [int(1000 * t) for t in [start, end]]
    outputfile = "%s_SUB%d_%d%s" % (name, t1, t2, ext)

    ffmpeg_extract_subclip(videopath, start, end, outputfile)

    return outputfile


def define_audio_path(filename=None, dir='/tmp'):
    
    #import os, time
    import time
    #from tempfile import NamedTemporaryFile as TempFile
    
    #filename = os.path.basename(videopath)
    #prefix = filename.replace('-', '').split('.')[0] + '-'
    suffix = time.strftime('%Y%m%d%H%m%S') + '.wav'
    #audiopath = TempFile(suffix=suffix, prefix=prefix, dir=dir)
    
    return dir + '/trvideos-' + suffix


def extract_audio_from_video(videopath, basedir='/tmp'):
    
    import moviepy.editor as mpye
    
    audiopath = define_audio_path(videopath, basedir)
    
    clip = mpye.VideoFileClip(videopath)
    audio = clip.audio
    audio.write_audiofile(audiopath, logger=None, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
    
    return audiopath


def split_audio(audiopath, length=3000, threshold=-52):
    
    from pydub import AudioSegment
    from pydub import silence
    import os
    
    # cria um diretorio temporario
    # quebra o audio em pedacos dentro do diretorio
    #tmpdir = tempfile.mkdtemp(prefix=audiopath.split('.')[0] + '-')
    tmpdir = audiopath.split('.')[0] # mesmo nome do arquivo sem a extensao
    os.mkdir(tmpdir)
        
    ## arquivo com resultado da traducao
    #fh = open("{0}_transcription.txt".format(tmpdir), "w+")
        
    # le o arquivo de audio
    audiodata = AudioSegment.from_wav(audiopath)
        
    # split_on_silence faz o trabalho em memoria
    audiochunks = silence.split_on_silence(
        audiodata,
        min_silence_len = length,
        silence_thresh = threshold)
        
    # cobre com silencio os segmentos de audio individuais
    i = 1
    for audio in audiochunks:
        
        #silentchunk = AudioSegment.silent(duration = 10)
        #audiochunk = silentchunk + audio + silentchunk
        audio.export(f'{tmpdir}/audiochunk{i:002}.wav', format='wav')
        i = i + 1
        #print('.', end='')
    #else:
    #    print('')

    # informando onde estao as coisas
    #print('Audio splitted to folder ' + tmpdir)
    
    return tmpdir


def transcribe_audio(audiopath, language='pt-BR'):

    import speech_recognition as sr 
    
    r = sr.Recognizer()
    
    with sr.AudioFile(audiopath) as source:

        r.adjust_for_ambient_noise(source)       
        listened = r.record(source, duration=120)
        try:
            text = r.recognize_google(listened, language=language)
            text = text.capitalize() + '.  '
            
        except sr.UnknownValueError as e:
            text = '(inaudível) '
        
        except sr.RequestError:
            text = '[ERROR: API inacessível]'

#        else:
#            print(audiopath, ": ", text)
    
    return text



def send_to_email(content, receiver):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender = 'marcelo.andrade@trt8.jus.br'
    password = 'ypcqtwjedrstrlog'
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Resultado da transcricao do seu video'
    
    msg.attach(MIMEText(content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    session.sendmail(sender, receiver, msg.as_string())
    session.quit()
    print('Mail sent')


def transcribe(videopath, begin=0.0, end=10.0, language='pt-BR'):

    import os, os.path

    realvideo = cut_video(videopath, begin, end)
    audio = extract_audio_from_video(realvideo)
    folder = split_audio(audio)
    text = ''
    for f in sorted(os.listdir(folder)):
        path = os.path.join(folder, f)
        if os.path.isfile(path) and path.endswith('.wav'):
            text += transcribe_audio(path)
    return text



import sys

from os import listdir
from os.path import isfile, join

import cgi
from tempfile import NamedTemporaryFile as TempFile

if __name__ == '__main__':
          
    if len(sys.argv) > 1:
        videopath = sys.argv[1]
        
    else:
        print ("Usage: {} <video-file>\n".format(sys.argv[0]))
        sys.exit(1)

    #print(transcribe(videopath))
    print('Debug mode. Only splitting video...')
    print(cut_video(videopath, 0.0, 10.0))

