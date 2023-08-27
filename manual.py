import cv2
import numpy as np

vid = cv2.VideoCapture('vids0.mp4')

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

while True:
    ret, frame = vid.read()
    if not ret :
        break
    mask = taillight_mask(frame)
 
    (x, y, w, h) = cv2.selectROI("uwu", mask, fromCenter=False,showCrosshair=True)
    if w == 0:
        taillight_pos.append(((-1, -1), 0))
        continue
    smol_mask = mask[y:y+h, x:x+w]
    (x2, y2), area = bounding_contours(smol_mask)
    taillight_pos.append(((x+x2, y+y2), area))
    
with open('points2.txt', 'w') as f:
    f.write(str(taillight_pos))