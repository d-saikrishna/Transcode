# Transcoder API

## Objective of this API:
To convert video and audio files into mp4 and mp3 formats respectively.

## Tech Stack used:
1. Python
2. FastAPI Framework was used to build API
3. Dockers
4. Deployed Docker image on Heroku Container

## API:
1. The API can be used here - [FastAPI Docs](https://fastapi-transcode.herokuapp.com/docs)
2. */uploads* endpoint enables client to upload a file. 
   1. It is a POST request
   2. Gives a downloadable url as response along with stream information of the uploaded video
3. */download/{file-name}* endpoint enables the client to download the transcoded video
   1. It is a GET request
   2. It has a query parameter called *url_key* - this is generated in the POST request above whenever a user uploads a video.
   3. Thus, only the uploader can download the video.
4. */analytics* endpoint gives the details of videos uploaded.
5. */crashanalytics* endpoint gives the details application crashes:
   1. 406 - when a non-audio/video file is uploaded
   2. 408 - Time out when too large files are uploaded (or bad internet)

## Few issues that needs to be fixed:
1. .MOV formats are being recognised as audios by the ffprobe software. So the response is in mp3.
2. API not tested for large files yet
3. API stores uploaded files and their information on the server currently. Need to connect to the database.
