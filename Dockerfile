FROM python:slim

WORKDIR /src

#RUN apt-get update && \
#    apt-get install ffmpeg --yes && \
#    rm -r /var/lib/apt/lists/* 
RUN python -m venv venv && . venv/bin/activate
RUN pip install -qq moviepy pydub Flask SpeechRecognition

