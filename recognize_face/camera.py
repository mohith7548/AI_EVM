import cv2, os, pickle, glob
import numpy as np
import face_recognition
from django.conf import settings


with open('models/recognize_face_models/dataset_faces.dat','rb') as f:
	faces_encodings = pickle.load(f)

with open('models/recognize_face_models/name_faces.dat','rb') as f:
	faces_names = pickle.load(f)


face_locations = []
face_encodings = []
face_names = []

FACE_NAME = "Unknown"

def gen(camera):
    global FACE_NAME
    while True:
        frame, FACE_NAME = camera.get_frame()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class VideoCamera:
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		ret, frame = self.video.read()
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
		rgb_small_frame = small_frame[:, :, ::-1]

		face_locations = face_recognition.face_locations( rgb_small_frame)
		face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
		face_names = []
		name = "Unknown"
		
		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces (faces_encodings, face_encoding)
			face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = faces_names[best_match_index]
			face_names.append(name)

		frame = cv2.flip(frame,1)
		
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes(), name


