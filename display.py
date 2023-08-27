import cv2
import numpy as np

blank_image = np.zeros((864,1920,3), np.uint8)

out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*"MP4V"), 30.0, (1920,864))

with open('points.txt', 'r') as f:
    taillight_pos_l = eval(f.read())
    
with open('points2.txt', 'r') as f:
    taillight_pos_r = eval(f.read())

vid = cv2.VideoCapture('vids0.mp4')
j = 0
while True:
    ret, frame = vid.read()
    
    if not ret :
        break
    newframe = frame.copy()
    for i in range(j-10, j):
        
        if  i+1 <len(taillight_pos_r) and i >= 0:
            if taillight_pos_r[i][0][0] != -1:
                uwu = cv2.line(frame, taillight_pos_r[i][0], taillight_pos_r[i+1][0], (0, 0, 255), int(taillight_pos_r[i][1]**0.5)+1)
                frame = cv2.addWeighted(newframe, 0.2, frame, 0.8, 1)
        
        if  i+1 <len(taillight_pos_l) and i >= 0:
            if taillight_pos_l[i][0][0] != -1:
                uwu = cv2.line(frame, taillight_pos_l[i][0], taillight_pos_l[i+1][0], (0, 0, 255), int(taillight_pos_l[i][1]**0.5)+1)
                frame = cv2.addWeighted(newframe, 0.2, frame, 0.8, 1)
                
    out.write(frame)
    # cv2.imshow('uwu', frame)
    # cv2.waitKey(10)
    j+=1
vid.release()
out.release()
cv2.destroyAllWindows()