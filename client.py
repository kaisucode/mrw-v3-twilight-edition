
import numpy as np
import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2

sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

rpi_name = socket.gethostname() # send RPi hostname with each image
#  picam = VideoStream(usePiCamera=True).start()
picam = VideoStream().start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    image = picam.read()
    reply = sender.send_image(rpi_name, image)

    #  nparr = np.fromstring(reply, np.uint8)
    #  new_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #  cv2.imshow(rpi_name, new_img)

    #  print("reply from server: ", reply)

