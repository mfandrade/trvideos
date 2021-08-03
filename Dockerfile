FROM python:slim

WORKDIR /src

RUN python -m venv venv && . venv/bin/activate
RUN pip install -qq moviepy pydub Flask SpeechRecognition

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]

EXPOSE 5000
