import cv2, os
import numpy as np


prototxt = "models/MobileNetSSD\MobileNetSSD_deploy.prototxt"
weights = "models/MobileNetSSD\MobileNetSSD_deploy.caffemodel"
thr = 0.4

classNames = {15: 'person'}
net = cv2.dnn.readNetFromCaffe(prototxt,weights)

PERSON_COUNT = 0

def gen(camera):
	global PERSON_COUNT
	video = cv2.VideoCapture(0)

	while True:
		person = 0
		if camera is not None:
			# frame, PERSON_COUNT = camera.get_frame()
			ret, frame = video.read()

			frame_resized = cv2.resize(frame,(300,300))
			blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

			net.setInput(blob)
			detections = net.forward()

			cols = frame_resized.shape[1] 
			rows = frame_resized.shape[0]


			# print(type(detections.shape[2]), detections.shape[2])
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

					if class_id == 15:

						person += 1
						label = classNames[class_id] + " " + str(person) + ": " + str(confidence)

						labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

						yLeftBottom = max(yLeftBottom, labelSize[1])
						
						# cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
						# 					(xLeftBottom + labelSize[0], yLeftBottom + baseLine),
						# 					(255, 255, 255), cv2.FILLED)

						# cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
						# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
					
					frame_flip = cv2.flip(frame,1)
					ret, jpeg = cv2.imencode('.jpg', frame_flip)
					# return jpeg.tobytes(), person
			PERSON_COUNT = person
			if frame_flip is not None:
				yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')



class VideoCamera:
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		ret, frame = self.video.read()

		frame_resized = cv2.resize(frame,(300,300))
		blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

		net.setInput(blob)
		detections = net.forward()

		cols = frame_resized.shape[1] 
		rows = frame_resized.shape[0]

		person = 0

		print(type(detections.shape[2]), detections.shape[2])
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

				if class_id == 15:

					person += 1
					label = classNames[class_id] + " " + str(person) + ": " + str(confidence)

					labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

					yLeftBottom = max(yLeftBottom, labelSize[1])
					
					# cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
					# 					(xLeftBottom + labelSize[0], yLeftBottom + baseLine),
					# 					(255, 255, 255), cv2.FILLED)

					# cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
					# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
				
				frame_flip = cv2.flip(frame,1)
				ret, jpeg = cv2.imencode('.jpg', frame_flip)
				return jpeg.tobytes(), person



