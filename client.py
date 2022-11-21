
import numpy as np
import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--device", help="window, guest, or windowBack")
args = parser.parse_args()

sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

rpi_name = socket.gethostname() # send RPi hostname with each image
#  picam = VideoStream(usePiCamera=True).start()
picam = VideoStream().start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    image = picam.read()
    new_img_str = sender.send_image(args.device, image)

    nparr = np.fromstring(new_img_str, np.uint8)
    rec_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow(rpi_name, rec_img)
    cv2.waitKey(1)

