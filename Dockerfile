FROM python:3.6.8
COPY . /usr/src/audio_spliter
WORKDIR /usr/src/audio_spliter/app
RUN apt-get update
RUN apt-get -y install ffmpeg
RUN pip install spleeter
RUN pip install -r requirements.txt
CMD ["python","app.py"]