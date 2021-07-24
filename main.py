import threading
import moviepy.video.io.ImageSequenceClip
import PIL.Image
from PIL import ImageEnhance
import sys
import itertools
import time
import glob
import pygame
import cv2
import os
from moviepy.editor import *

chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
try:
    if os.path.exists('output'):
        files = glob.glob('output/*')
        for f in files:
            os.remove(f)
    if os.path.exists('data'):
        files = glob.glob('data/*')
        for f in files:
            os.remove(f)
except:
    pass


def get_image(folder):
    video_name = [video for video in os.listdir(folder) if
                  video.endswith(".mp4") or video.endswith(".mkv") or video.endswith(".avi") or video.endswith(
                      ".flv") or video.endswith(".wmv")][0]
    path = f"{folder}/{video_name}"
    cam = cv2.VideoCapture(path)
    FPS = cam.get(cv2.CAP_PROP_FPS)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')

    except OSError:
        print('Error: Creating directory of data')

    currentframe = 0

    while True:

        ret, frame = cam.read()

        if ret:
            name = './data/frame' + str(currentframe) + '.jpg'
            cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()
    return FPS, currentframe, path


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = new_width * ratio
    return image.resize((new_width, int(new_height))), new_width,int(new_height)


def high_contrast(image):
    return ImageEnhance.Contrast(image).enhance(5)


def grayify(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()
    return "".join([chars[int(pixel / 25)] for pixel in pixels])


def animate():
    global done, status, count, number_of_image
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        if count == 0:
            sys.stdout.write(f'\r{status}... ' + c)
        else:
            sys.stdout.write(f'\r{status}: {count}/{number_of_image}   ' + c)
        sys.stdout.flush()
        time.sleep(0.25)


def create_output_image(num, new_width=100):
    global status
    status = "Create image ascii style"
    ls = []
    global count

    for i in range(num):
        image = PIL.Image.open(f"data/frame{i}.jpg")
        new_image_data = pixels_to_ascii(grayify(high_contrast(resize_image(image, new_width)[0])))
        pixel_count = len(new_image_data)
        ascii_image = [new_image_data[i:i + new_width] for i in range(0, pixel_count, new_width)]
        ls.append(ascii_image)

    pygame.init()

    white = (255, 255, 255)
    black = (0, 0, 0)
    _, X, Y = resize_image(image, new_width)
    screen = pygame.display.set_mode((X * 11, Y * 11))
    font = pygame.font.SysFont("consolas", 15)

    try:
        if not os.path.exists('output'):
            os.makedirs('output')

    except OSError:
        print('Error: Creating directory of data')
    for k in range(len(ls)):
        count += 1
        screen.fill(white)
        for i in range(len(ls[k])):
            for j in range(len(ls[k][i])):
                text = font.render(ls[k][i][j].rstrip(), True, black)
                # text.set_alpha(200)
                screen.blit(text, (j * 11, i * 11))
        pygame.image.save(screen, f"output/capture{k}.png")
    pygame.quit()
    count = 0
    status = "Converting to video"


def get_audio(video_path):
    video = VideoFileClip(video_path)
    return video.audio


def set_audio(video, mp3, output_name):
    videoclip = video.set_audio(mp3)
    videoclip.write_videofile(output_name)

os.environ['SDL_VIDEODRIVER'] = 'dummy'
video_folder = "input_video"
count = 0

done = False
status = "Get image from video"
t = threading.Thread(target=animate)
t.start()

# save all images from video to folder "data"
fps, number_of_image, path_to_origin_video = get_image(video_folder)

# convert origin images to ascii style and save to folder "output"
create_output_image(number_of_image)

image_files = [f"output/capture{i}.png" for i in range(number_of_image)]

done = True

# combine images ascii  to video
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)

# get audio from origin video
audio = get_audio(path_to_origin_video)

# set audio for video ascii
set_audio(clip, audio, "video_output.mp4")
