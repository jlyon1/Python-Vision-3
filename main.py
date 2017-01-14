import numpy as np
import cv2

#these arrays represent the bounds for our threhsolding operation
lowerHSV = np.array([0,230,70])
upperHSV = np.array([250,255,255])

#opening a videocapture of our laptop camera
cap = cv2.VideoCapture("http://10.30.44.20/mjpg/video.mjpg")

running = True
while running:
    #Read an image from the camera
    ret, img = cap.read()
    #convert the image to an hsv image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Take a mask using the inrange function to generate a binary image
    mask = cv2.inRange(hsv,lowerHSV,upperHSV)
    #erode to get rid of noise
    kernel = np.ones((2,2),np.uint8)
    mask = cv2.erode(mask,kernel,iterations = 3)
    #dilate to bring back the eroded area of the target object
    mask = cv2.dilate(mask,kernel,iterations = 3)
    #display the 
    cv2.imshow('frame',mask)
    #Find contours and store them in an array.
    im2,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    approxArr = []

    for contour in contours:
        epsilon = 0.025*cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,epsilon,True)
        x,y,w,h = cv2.boundingRect(contour)
        approxArr.append(approx)
        boxes.append([x,y,w,h,False])
        
    targetsPos = []
    run = False
    for i in range(len(boxes)):
        x = boxes[i][0]
        y = boxes[i][1]
        z = boxes[i][2]
        h = boxes[i][3]
        #sprint (w)
        if(run):
            break;
        boxes[i][4] = True
        if w < h:
            if(w > 5):
                if w * h > 50:
                    for j in range(len(boxes)):
                        if(boxes[j][4] == False):
                            if(abs(boxes[i][3] - boxes[j][3]) < 100):
                                targetsPos.append(boxes[i])
                                targetsPos.append(boxes[j])
                                boxes[j][4] = True
                                run = True
                                break
                            
        
               
    
    #print(len(targetsPos))
    print("-----------")
    for i in range(len(targetsPos)):
        x = targetsPos[i][0]
        y = targetsPos[i][1]
        z = targetsPos[i][2]
        h = targetsPos[i][3]
        print(h)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv2.drawContours(img,approxArr,-1,(0,255,0),3)
    print("-----------")
    
    
    
    cv2.imshow('hsv',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
#Clean Up 170 255 98
running = False
cv2.destroyAllWindows()
cap.release()
