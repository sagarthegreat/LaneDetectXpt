import cv2
import numpy as np
import matplotlib


cap = cv2.VideoCapture('sample2.mp4')
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #print(height)
        #print(width)

        isolateW = cv2.inRange(gray,200,255)
        points = np.array([[0, 0], [1920, 0], [1920, 540], [0, 540]])
        cv2.fillPoly(isolateW, pts=[points], color=(0, 0, 0))
        edges = cv2.Canny(isolateW,100,200)
        lines = cv2.HoughLinesP(isolateW, rho=2, theta=np.pi / 180, threshold=100,minLineLength=100,maxLineGap=300)
        #lines = cv2.HoughLinesP(isolateW, rho=2, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=250)
        #print(lines[0][0][0])
        for q in range(0,100):
            try:
                x1 = lines[q][0][0]
                y1 = lines[q][0][1]
                x2 = lines[q][0][2]
                y2 = lines[q][0][3]
                slope = abs((y2-y1)/(x2-x1))
                print(slope)
                if slope<0.5:
                    break

            except:
                pass
            try:
                cv2.line(frame,[x1,y1],[x2,y2],[0,255,0],10)


            except:
                pass

        pts1 = np.float32([[0,0], [1919,1079],
                           [0,1079], [1919,1079]])
        pts2 = np.float32([[0, 0], [1919,1079],
                           [0,1079], [1919,1079]])
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warp = cv2.warpPerspective(frame, matrix, (1920,1080))

        # Display the resulting frame
        cv2.imshow('Frame',frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()