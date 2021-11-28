import face_recognition
import cv2
import numpy as np
import pickle
import os
import glob


faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, os.path.join(os.getcwd(), 'faces'))

list_of_files = [f for f in glob.glob(path+'*.jpg')]

number_files = len(list_of_files)
names = list_of_files.copy()

for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])

    names[i] = names[i].replace(path, "")
    names[i] = names[i].replace(".jpg", "")
    faces_names.append(names[i])

with open('dataset_faces.dat','wb') as f:
    pickle.dump(faces_encodings,f)

with open('name_faces.dat','wb') as f:
    pickle.dump(faces_names,f)

