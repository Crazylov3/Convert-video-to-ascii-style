from youtube_dl import YoutubeDL
import os

try:
    if not os.path.exists('input_video'):
        os.makedirs('input_video')

except OSError:
    print('Error: Creating directory of data')
    
url = "https://www.youtube.com/watch?v=Pb3OEY9XqPA&ab_channel=Ghi%E1%BB%81nQu%E1%BA%A3ngC%C3%A1o"
with YoutubeDL({'outtmpl': os.path.join("input_video", '%(title)s-%(id)s.%(ext)s')}) as ydl:
    info = ydl.extract_info(url)
