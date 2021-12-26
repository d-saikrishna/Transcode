from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import shutil
import os
from ffmpeg_convert import FFMConverter
from fastapi.responses import FileResponse
import glob
import ffmpeg
import pandas as pd
import random
import string
from decouple import config


# Begin API
app = FastAPI()

@app.post("/")
async def root(file: UploadFile = File(...)):
    # Stream Info
    stream_info_df = pd.read_csv('stream_info.csv')
    crash_analytics_df = pd.read_csv('crash_analytics.csv')

    file_name = file.filename
    file_path = 'Uploads/'+ file_name
    videos_list = list(glob.glob("Uploads//*.mp4"))+list(glob.glob("Uploads//*.webm"))+list(glob.glob("Uploads//*.mkv"))
    audios_list = list(glob.glob(r"Uploads//*.mp3")) + list(glob.glob(r"Uploads//*.wav")) + list(glob.glob(r"Uploads//*.wma"))
    # If a file with same name is uploaded again, overwrite permission is being asked on the server.
    # To override that we'll create a duplicate filename.
    num = 2
    print(file_path)
    print(audios_list)
    while file_path in videos_list + audios_list:
        print(file_path in audios_list)
        if num == 2:
            file_name = file_name.split('.')[0]+'-' +str(num)+'.'+file_name.split('.')[1]
            file_path = 'Uploads/' + file_name
        else:
            file_name = file_name.split('-')[0]+'-' +str(num)+'.'+file_name.split('.')[1]
            file_path = 'Uploads/' + file_name
        num = num+1
    print(file_path)

    # Save the uploaded file on server
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        await file.close()
    except:
        error_msg = 'Timeout error: The uploaded file is too large.'
        crash_analytics_df.loc[len(crash_analytics_df)] = [408,
                                                           error_msg,
                                                           0]
        crash_analytics_df.to_csv('crash_analytics.csv', index=False)
        raise HTTPException(status_code=408, detail=error_msg)


    # Transcode the uploaded file to mp3/mp4 - based on the format of the file.
    ffm = FFMConverter()
    try:
        file_type = ffmpeg.probe(file_path)['streams'][0]['codec_type']
    except:
        os.remove(file_path) #Delete the unwanted file.
        error_msg = 'The uploaded file is neither a video nor an audio file.'
        crash_analytics_df.loc[len(crash_analytics_df)] = [406,
                                                           error_msg,
                                                           file_path.split('.')[1]]
        crash_analytics_df.to_csv('crash_analytics.csv',index=False)
        raise HTTPException(status_code=406, detail=error_msg)

    url_key = "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits
                                    , 10))
    if file_type == 'audio':
        download_file_name = file_name.split('.')[0] + '_transcoded.mp3'
        ffm.convert_py(file_path, 'Downloads//'+download_file_name)
        download_url = config('host')+'download/'+file_name.split('.')[0]+'_transcoded.mp3'+'?url_key='+str(url_key)
        duration = ffmpeg.probe('Downloads//'+file_name.split('.')[0]+'_transcoded.mp3')['format']['duration']
    elif file_type == 'video':
        download_file_name = file_name.split('.')[0] + '_transcoded.mp4'
        ffm.convert_py(file_path, 'Downloads//'+download_file_name)
        download_url =config('host')+'download/' + file_name.split('.')[0] + '_transcoded.mp4'+'?url_key='+str(url_key)
        duration = ffmpeg.probe('Downloads//'+file_name.split('.')[0]+'_transcoded.mp4')['format']['duration']
    else:
        error_msg = 'The uploaded file is neither a video nor an audio file.'
        crash_analytics_df.loc[len(crash_analytics_df)] = [406,
                                                           error_msg,
                                                           file_path.split('.')[1]]
        crash_analytics_df.to_csv('crash_analytics.csv', index=False)
        raise HTTPException(status_code=406,
                            detail=error_msg)

    #os.remove(file_path) - Optional Feature to not save files on the server.


    stream_info_df.loc[len(stream_info_df)] = [file_name,
                                               file_type,
                                               float(os.path.getsize(file_path)/1024),
                                               duration,
                                               download_file_name,
                                               download_url,
                                               url_key]
    stream_info_df.to_csv('stream_info.csv',index=False)


    #Response
    return {"file name": file.filename,
            "file type": file_type,
            "size (kb)": float(os.path.getsize(file_path)/1024),
            "Download mp4 url": download_url,
            "Durations (s)": duration
            }

@app.get("/download/{file_name}")
async def download(file_name: str, url_key: str):
    stream_info_df = pd.read_csv('stream_info.csv')
    df = stream_info_df[stream_info_df['download_file_name'] == str(file_name)]
    print(str(df.url_key.to_list()[0]))
    if df.url_key.to_list()[0] == url_key:  #Remove this condition for publicly shareable URLS
        return FileResponse('Downloads//'+file_name)


@app.get("/analytics")
def analytics():
    stream_info_df = pd.read_csv('stream_info.csv')
    df = stream_info_df[['file_name', 'file_type', 'size_kb', 'duration_s']]
    return df.to_dict()


@app.get("/crashanalytics")
def analytics():
    crash_analytics_df = pd.read_csv('crash_analytics.csv')
    print(crash_analytics_df)
    return crash_analytics_df[['status_code','file_type']].to_dict()

if __name__ == '__main__':
    uvicorn.run(app)

