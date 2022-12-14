"""pub_sub_broadcast.py -- broadcast OpenCV stream using PUB SUB."""

import sys

import socket
import traceback
from time import sleep
import cv2
from imutils.video import VideoStream
import imagezmq

if __name__ == "__main__":
    # Publish on port
    port = 5555
    sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)
    receiver = imagezmq.ImageHub()

    #  capture = VideoStream()  # Webcam
    # capture = VideoStream(usePiCamera=True)  # PiCamera

    #  capture.start()
    #  sleep(2.0)  # Warmup time; needed by PiCamera on some RPi's
    #  print("Input stream opened")

    # JPEG quality, 0 - 100
    #  jpeg_quality = 95

    rpi_name = socket.gethostname()

    try:
        counter = 0
        while True:

            device_name, image = receiver.recv_image()


            #  frame = capture.read()

            #  ret_code, jpg_buffer = cv2.imencode(
            #      ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

            sender.send_jpg(rpi_name, jpg_buffer)
            print("Sent frame {}".format(counter))
            counter = counter + 1
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler:')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        capture.stop()
        sender.close()
        sys.exit()
