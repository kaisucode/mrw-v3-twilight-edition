import cv2
import imagezmq
import mediapipe as mp
import queue
import numpy as np

def replace_background(fg, bg):
    bg_image = bg
    frame = fg

    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # get the result
    results = selfie_segmentation.process(RGB)

    mask = results.segmentation_mask
    mask = cv2.GaussianBlur(mask, (33, 33), 0)

    # it returns true or false where the condition applies in the mask
    condition = np.stack(
        (mask,) * 3, axis=-1) > 0.6
    height, width = frame.shape[:2]
    # resize the background image to the same size of the original frame
    bg_image = cv2.resize(bg_image, (width, height))
    output_image = np.where(condition, frame, bg_image)
    return output_image


if __name__ == "__main__":

    image_hub = imagezmq.ImageHub()

    print("Starting server on port 5555")

    #  The queue module implements multi-producer, multi-consumer queues. 
    #  It is especially useful in threaded programming when information must be exchanged safely between multiple threads. 
    #  The Queue class in this module implements all the required locking semantics.
    #  https://docs.python.org/3/library/queue.html#queue.Queue

    guestQueue = queue.Queue(maxsize=3)
    windowQueue = queue.Queue(maxsize=3)
    windowBackQueue = queue.Queue(maxsize=3)

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation()


    frame = 0
    while True: 
        rpi_name, image = image_hub.recv_image()

        #  cv2.imshow(rpi_name, image)
        #  cv2.waitKey(1)
        #  image_hub.send_reply(b'OK')

        new_img = np.concatenate((image, image), axis=1)

        new_img_str = cv2.imencode('.jpg', new_img)[1].tostring()
        nparr = np.fromstring(new_img_str, np.uint8)
        con_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #  cv2.imshow("what", con_img)

        cv2.imshow(rpi_name, con_img)
        cv2.waitKey(1)
        image_hub.send_reply(b'OK')

        #  image_hub.send_reply(b'OK')
        #  image_hub.send_reply(new_img_str)
        
        if (frame % 10 == 0): 
            print("received image from ", rpi_name)

        frame += 1



