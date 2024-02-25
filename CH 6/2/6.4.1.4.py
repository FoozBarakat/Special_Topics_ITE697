import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import zoom
import pickle as pkl

# Load test images
smile = cv2.imread('smile.jpg')
no_smile = cv2.imread('no_smile.jpg')

# Load face detection classifier
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Detect faces in smile image
gray_smile = cv2.cvtColor(smile, cv2.COLOR_BGR2GRAY)
faces_smile = faceCascade.detectMultiScale(gray_smile, scaleFactor=1.1, minNeighbors=6, minSize=(100, 100))

# Visualize detected faces
fig, ax = plt.subplots()
ax.imshow(gray_smile, cmap='gray')
for (x_smile, y_smile, w_smile, h_smile) in faces_smile:
    ax.add_artist(plt.Rectangle((x_smile, y_smile), w_smile, h_smile, fill=False, lw=3, color='green'))
ax.axis('off')
plt.show()

# Select face portion from the smile image
face_smile = gray_smile[y_smile:y_smile+h_smile, x_smile:x_smile+w_smile]

# Detect faces in no_smile image
gray_no_smile = cv2.cvtColor(no_smile, cv2.COLOR_BGR2GRAY)
faces_no_smile = faceCascade.detectMultiScale(gray_no_smile, scaleFactor=1.1, minNeighbors=6, minSize=(100, 100))

# Visualize detected faces
fig, ax = plt.subplots()
ax.imshow(gray_no_smile, cmap='gray')
for (x_no_smile, y_no_smile, w_no_smile, h_no_smile) in faces_no_smile:
    ax.add_artist(plt.Rectangle((x_no_smile, y_no_smile), w_no_smile, h_no_smile, fill=False, lw=3, color='red'))
ax.axis('off')
plt.show()

