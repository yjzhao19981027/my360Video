import numpy as np
import cv2
import math

pi = math.pi

cap = cv2.VideoCapture("/Users/zhaoyinjie/Downloads/data.mp4")
wid = int(cap.get(3))
hei = int(cap.get(4))
framerate = int(cap.get(5))
framenum = int(cap.get(7))
video = np.zeros((framenum, hei, wid, 3), dtype='float16')
cnt = 0
while (cap.isOpened()):
    a, b = cap.read()
    cv2.imshow('%d' % cnt, b)
    cv2.waitKey(1000)
    b = b.astype('float16') / 255
    video[cnt] = b
    # print(cnt)
    cnt += 1


def compute360Pos(x, y, height, width):
    h = height / 2
    w = width / 2
    phi = y - h / h * pi / 2  # theta is between -90 degree to 90 degree
    theta = x - w / w * pi  # phi is between -180 degree to 180 degree
    return theta, phi


def computePos(theta, phi, height, width):
    h = height / 2
    w = width / 2
    y = phi / pi * w + w
    x = theta / pi * 2 * h + h
    return round(x), round(y)


def generateView(image, x_center, y_center, view_height, view_width, image_height, image_width, angle_vertical, angle_parallel):
    frame = np.zeros((view_height, view_width, 3), dtype='float16')
    per_height = angle_vertical / view_height
    per_width = angle_parallel / view_width
    theta, phi = compute360Pos(x_center, y_center, image_height, image_width)
    theta -= angle_parallel
    phi -= angle_vertical
    for i in range(view_height):
        for j in range(view_width):
            theta += per_width
            phi += per_height
            x, y = computePos(theta, phi, image_height, image_width)
            frame[i][j] = image[x][y]
    return frame

