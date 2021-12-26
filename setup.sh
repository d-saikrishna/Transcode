
# Setting up os
sudo yum -y update

#Git clone
sudo yum install git -y
git init
git clone https://github.com/d-saikrishna/Transcode

# Setting up Python-Virtual Environment
sudo yum install python3
sudo yum install python-virtualenv -y
python3 -m venv env
source env/bin/activate
cd Transcode
pip install -r requirements.txt

#Installing ffmpeg and ffprobe
# https://gist.github.com/srameshr/d6778ffdcb8ad805f29c4e3826c060f9 (alternative)
sudo su -

cd /usr/local/bin
mkdir ffmpeg

cd ffmpeg
wget https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-4.2.1-amd64-static.tar.xz
tar xvf ffmpeg-4.2.1-amd64-static.tar.xz
mv ffmpeg-4.2.1-amd64-static/ffmpeg .

ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
ln -sfn /usr/local/bin/ffmpeg/ffmpeg-*-amd64-static/ffprobe /usr/bin/ffprobe
exit

# Run the app
nohup uvicorn transcode:app --host 0.0.0.0 &