import numpy as np
import argparse
import cv2 

prototxt = "MobileNetSSD\MobileNetSSD_deploy.prototxt"
weights = "MobileNetSSD\MobileNetSSD_deploy.caffemodel"
thr = 0.4

classNames = {15: 'person'}

video = cv2.VideoCapture(0)

net = cv2.dnn.readNetFromCaffe(prototxt,weights)

while True:
    ret, frame = video.read()
    frame_resized = cv2.resize(frame,(300,300))
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

    net.setInput(blob)
    detections = net.forward()

    cols = frame_resized.shape[1] 
    rows = frame_resized.shape[0]

    person = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > thr:
            class_id = int(detections[0, 0, i, 1])

            xLeftBottom = int(detections[0, 0, i, 3] * cols) 
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)
            
            heightFactor = frame.shape[0]/300.0  
            widthFactor = frame.shape[1]/300.0 

            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)
  
            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),(0, 255, 0))

            if class_id in classNames:

                person+=1
                label = classNames[class_id] + " " + str(person) + ": " + str(confidence)

                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                     (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                     (255, 255, 255), cv2.FILLED)

                cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                print(label)

    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) >= 0:
        break

print("Total no. of persons: "+str(person))