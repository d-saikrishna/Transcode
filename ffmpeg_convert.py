import subprocess
import ffmpeg
import glob
import pandas as pd

class FFMConverter():

    def convert(self, input_file, output_file):
        command = 'ffmpeg -i ' + input_file +' '+output_file
        subprocess.run(command)

    def convert_py(self, input_file, output_file):
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)


#ffm = FFMConverter()

#ffm.convert_py(r'C:\Users\saikr\Downloads\nasa.webm',r'testpy.mp4')

