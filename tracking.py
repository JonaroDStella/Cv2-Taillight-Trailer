import cv2
import numpy as np

vid = cv2.VideoCapture('vids0.mp4')

tracker = cv2.TrackerCSRT_create()

initBB = None

taillight_pos = []

def taillight_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    return cv2.inRange(hsv, (90, 150, 100), (140, 255, 255))
    
    
def bounding_contours(frame):
    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours.sort(key=cv2.contourArea, reverse=True)
        box = cv2.minAreaRect(contours[0])
    else:
        return ([0, 0], 0)
    return np.int0(box[0]), cv2.contourArea(contours[0])

i = 0
while True:
    ret, frame = vid.read()
    mask = taillight_mask(frame)
    
    if not ret :
        break
 
    key = cv2.waitKey(0 if initBB == None else 50)
    
    if key == ord("s"):
        initBB = cv2.selectROI("uwu", mask, fromCenter=False,showCrosshair=True)
        tracker.init(frame, initBB)
        
    if key == ord("q"):
        break
        
    if initBB is not None:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            smol_mask = mask[y:y+h, x:x+w]
            
            (x2, y2), area = bounding_contours(smol_mask)
            
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            cv2.circle(mask, (x+x2, y+y2), 5, (0, 150, 255), -1)
            taillight_pos.append(((x+x2, y+y2), area))
            cv2.rectangle(mask, (x, y), (x+w, y+h), (150, 255, 0), 2)
    else:
        taillight_pos.append(((-1, -1), 0))
            
    cv2.imshow('uwu', mask)
    
with open('points2.txt', 'w') as f:
    f.write(str(taillight_pos))