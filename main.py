# importing the module
import math
import cv2
import numpy as np
from copy import deepcopy
from math import floor, ceil

img = None
history = None
path = []
path_separators = []
index = 0

split = False

radius = 15

IMG = 0
PATH = 1
INDEX = 2
SEPARATOR = 3


def generate_animation(image, path, path_separators):
    global radius
    last_angle = 0
    copy_image = deepcopy(image)
    h, w, c = image.shape
    out = cv2.VideoWriter('handwritten.mp4',cv2.VideoWriter_fourcc(*'X264'), 30, (w,h))
    X=0
    Y=1
    res_mask = np.zeros((h,w), np.uint8)
    res_image = np.zeros((h,w, c), np.uint8)
    #b = img[y, x, 0]
    #g = img[y, x, 1]
    #r = img[y, x, 2]
    res_image[:] = (image[0,0,0], image[0,0,1], image[0,0,2])
    for i in range(1, len(path)):
        if path_separators[i-1]:
            continue
        first = path[i-1]
        second = path[i]
        x = second[X] - first[X]
        y = second[Y] - first[Y]

        # speed formula (downward movement is the fastest) (shorter step size equals faster)
        # how close are we to going downward
        radi_dist = 0
        three_q_r = 3 * math.pi / 2
        
        if x == 0 and y == 0:
            # just assume fastest movement, who cares the points overlap
            angle = 0
            radi_dist = 0
        else:
            angle = math.atan2(y, x)
            radi_dist = abs(three_q_r - math.atan2(y, x))

        speed = abs(angle - last_angle)
        last_angle = angle

        # conver to (1, 2) range for speed
        #speed = 1 - (radi_dist * 2 / (3 * math.pi))

        

        """START OF SMOOTH"""
        distance = (x**2 + y**2)**0.5
        step_count = int(ceil(distance))
        relx = 0
        rely = 0
        
        # basic step size
        step_size = int(ceil(radius/2))
        frames_skipped = max(int(ceil(speed * 10)), 1)
        
        # advanced step size
        #step_size = int(ceil((radius / 2) * speed))

        for step in range(0, step_count, step_size):
            relx = x * (step / step_count)
            rely = y * (step / step_count)
            # YOUR FUNCTION HERE
            mask = np.zeros((h,w), np.uint8)
            mask = cv2.circle(mask, (first[X] + int(relx), first[Y] + int(rely)), radius,255, thickness=-1)
            res_mask = res_mask + mask
            usable = 255 * res_mask
            usable = usable.clip(0, 255).astype("uint8")

            frame = deepcopy(res_image)
            mask = np.dstack([(usable > 0)]*3)
            np.copyto(frame, copy_image, where=mask)
            if step == step_count or step % frames_skipped == 0:
                out.write(frame)
            # YOUR FUNCTION HERE
            #ctypes.windll.user32.mouse_event(0x01, int(realx), int(realy), 0, 0)
            realx = 0
            realy = 0
            """END OF SMOOTH"""


    """for p in path:
        mask = np.zeros((h,w), np.uint8)
        mask = cv2.circle(mask, (p[X],p[Y]), radius,255, thickness=-1)
        res_mask = res_mask + mask
        usable = 255 * res_mask
        usable = usable.clip(0, 255).astype("uint8")

        frame = deepcopy(res_image)
        mask = np.dstack([(usable > 0)]*3)
        np.copyto(frame, copy_image, where=mask)
        out.write(frame)"""
    out.release()



class HistoryManager:
    def __init__(self) -> None:
        self.history_stack = []
        self.lookback = 10

    def add_new_state(self, element):
        print("Adding a new state.")
        if len(self.history_stack) > self.lookback:
            self.history_stack.pop(0)
        self.history_stack.append(element)
        print("[", end="")
        for x in self.history_stack:
            print(f"{x[2]}: {x[PATH]},", end="")
        print("]")

    def revert_last_state(self):
        if len(self.history_stack) >= 2:
            # must have at least one element left
            print("Reverting state.")
            self.history_stack.pop()
            print("[", end="")
            for x in self.history_stack:
                print(f"{x[2]}: {x[PATH]}, ", end="")
            print("]")
        else:
            print("Cannot revert to a non-existant state.")

    def get_current_state(self):
        if len(self.history_stack) > 0:
            return self.history_stack[-1]
        raise Exception("Error, no state in history manager to get...")

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    global img, index, history, path, IMG, PATH, split, path_separators, SEPARATOR, INDEX
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        if split and len(path_separators) > 0:
            path_separators[-1] = True
            split = False
        elif len(path) > 0:
            pair = path[-1]
            img = cv2.line(img, (x,y), (pair[0], pair[1]), (0, 255, 0), thickness=2)

        img = cv2.circle(img, (x,y), radius, (0,0,255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(index), (x,y), font,
                    0.5, (255, 255, 255), 1)
        path.append((x,y))
        path_separators.append(False)
        history.add_new_state((deepcopy(img), deepcopy(path), index, deepcopy(path_separators)))
        index += 1
        cv2.imshow('image', img)
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_RBUTTONDOWN:
        history.revert_last_state()
        pair = history.get_current_state()
        img = deepcopy(pair[IMG])
        path = deepcopy(pair[PATH])
        path_separators = deepcopy(pair[SEPARATOR])
        cv2.imshow('image', img)
 
# driver function
if __name__=="__main__":
 
    # reading the image
    img = cv2.imread('FirstPart.png', 1)
    original_image = deepcopy(img)
    history = HistoryManager()

    history.add_new_state((deepcopy(img), deepcopy(path), index, deepcopy(path_separators)))
    index += 1
 
    # displaying the image
    cv2.imshow('image', img)
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
    
    while True:
        # wait for a key to be pressed to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        if key == ord('e'):
            generate_animation(original_image, path, path_separators)
            break
        if key == ord(' '):
            split = True
 
    # close the window
    cv2.destroyAllWindows()