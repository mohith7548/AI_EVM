import cv2, os
import numpy as np
from django.conf import settings


face_detection_videocam = cv2.CascadeClassifier(
	os.path.join(str(settings.BASE_DIR),
	'models/opencv_haarcascade_data/haarcascade_frontalface_default.xml')
)

FACES_COUNT = 0

def gen(camera):
    global FACES_COUNT
    while True:
        frame, FACES_COUNT = camera.get_frame()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class VideoCamera:
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes(), len(faces_detected)


