FROM python:3.8

COPY ./start.sh /app/start.sh
COPY ./Downloads /app/Downloads
COPY ./Uploads /app/Uploads
COPY ./crash_analytics.csv /app/crash_analytics.csv
COPY ./stream_info.csv /app/stream_info.csv
COPY ./transcode.py /app/transcode.py
COPY ./ffmpeg_convert.py /app/ffmpeg_convert.py
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

WORKDIR /app

RUN apt update && apt install ffmpeg -y

RUN pip3 install -r requirements.txt
RUN chmod +x /app/start.sh

EXPOSE 8000
CMD ["/app/start.sh"]
