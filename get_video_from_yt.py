from youtube_dl import YoutubeDL
import os

try:
    if not os.path.exists('input_video'):
        os.makedirs('input_video')

except OSError:
    print('Error: Creating directory of data')

url = input("Link video youtube: ").strip()
with YoutubeDL({'outtmpl': os.path.join("input_video", '%(title)s-%(id)s.%(ext)s')}) as ydl:
    info = ydl.extract_info(url)
