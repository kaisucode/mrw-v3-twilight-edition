import cv2
import imagezmq
import mediapipe as mp
import queue
import numpy as np

def empty_frame(): 
    img = np.zeros([520, 520, 3], np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Disconnected"
    text_position = (30, 200)
    img = cv2.putText(img, text, text_position, font, 2, (0, 255, 255), 5, cv2.LINE_AA)
    return img

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

def safe_pop_from_queue(queue_name): 
    cur_queue = None
    if queue_name == "guest": 
        cur_queue = guestQueue
    elif queue_name == "window": 
        cur_queue = windowQueue
    elif queue_name == "windowBack": 
        cur_queue = windowBackQueue

    if cur_queue.empty(): 
        return empty_frame()

    while cur_queue.qsize() > 1: 
        cur_queue.get_nowait()
    print(queue_name, ": ", cur_queue.qsize())
    
    return cur_queue.get_nowait()



def encode_img(img): 
    return cv2.imencode('.jpg', new_img)[1].tostring()

if __name__ == "__main__":

    image_hub = imagezmq.ImageHub()

    print("Starting server on port 5555")

    #  The queue module implements multi-producer, multi-consumer queues. 
    #  It is especially useful in threaded programming when information must be exchanged safely between multiple threads. 
    #  The Queue class in this module implements all the required locking semantics.
    #  https://docs.python.org/3/library/queue.html#queue.Queue

    #  guestQueue = queue.Queue(maxsize=3)
    #  windowQueue = queue.Queue(maxsize=3)
    #  windowBackQueue = queue.Queue(maxsize=3)
    guestQueue = queue.Queue()
    windowQueue = queue.Queue()
    windowBackQueue = queue.Queue()

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation()


    frame = 0
    curGuestFrame = empty_frame()
    curWindowFrame = empty_frame()
    curWindowBackFrame = empty_frame()

    while True: 
        rpi_name, image = image_hub.recv_image()
        
        new_img = image
        if rpi_name == "guest": 
            guestQueue.put(image)
            curGuestFrame = safe_pop_from_queue("guest")

            #  guestQueue.get_nowait()
            #  guestQueue.get_nowait()
            #  guestQueue.clear()

            rb_windowFrame = replace_background(curGuestFrame, curWindowFrame)
            rb_windowBackFrame = replace_background(curGuestFrame, curWindowBackFrame)
            new_img = np.concatenate((rb_windowFrame, rb_windowBackFrame), axis=1)
        elif rpi_name == "window": 
            windowQueue.put(image)
            curWindowFrame = safe_pop_from_queue("window")
            #  windowQueue.clear()
            #  windowQueue.get_nowait()
            #  windowQueue.get_nowait()
            new_img = replace_background(curGuestFrame, curWindowFrame)
        elif rpi_name == "windowBack": 
            windowBackQueue.put(image)
            curWindowBackFrame = safe_pop_from_queue("windowBack")
            #  windowBackQueue.clear()
            #  windowBackQueue.get_nowait()
            #  windowBackQueue.get_nowait()
            new_img = replace_background(curGuestFrame, curWindowBackFrame)

        new_img_str = encode_img(new_img)
        image_hub.send_reply(new_img_str)
        
        if (frame % 10 == 0): 
            print("received image from ", rpi_name)

        frame += 1



