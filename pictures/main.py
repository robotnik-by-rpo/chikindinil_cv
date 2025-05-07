import cv2
import numpy as np

color_background = [212, 178, 254]
my_picture = 0
video = cv2.VideoCapture("output.avi")
if not video.isOpened():
    exit()
ret, frame = video.read()

while True:
    ret, frame = video.read()
    if not ret:
        break
    image = frame[0][0]

    if image[0] == color_background[0] and image[1] == color_background[1] and image[2] == color_background[2]:
        my_picture += 1
    key = cv2.waitKey(0)

print(my_picture)