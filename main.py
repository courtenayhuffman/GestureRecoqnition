# COGS 300 Term Project
# Gesture Recognition with ML

# things I need to import:
#   dataset
#   gulpIO
import pandas as pd
import numpy as np
import cv2 as cv
import os
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf

def def_model_param():
    CATEGORIES = len(CATEGORY_MAP)
    base_model = Sequential()
    base_model.add(SqueezeNet(input_shape=(225, 225, 3), include_top=False))
    base_model.add(Dropout(0.5))
    base_model.add(Convolution2D(CATEGORIES, (1, 1), padding='valid'))
    base_model.add(Activation('relu'))
    base_model.add(GlobalAveragePooling2D())
    base_model.add(Activation('softmax'))
    base_model.compile(
        optimizer=Adam(lr=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return base_model

CATEGORY_MAP = {
    "call_me": 0,
    "fingers_crossed": 1,
    "okay": 2,
    "paper": 3,
    "peace": 4,
    "rock": 5,
    "rock_on": 6,
    "scissor": 7,
    "thumbs": 8,
    "up": 9
}

training_img = 'HandGesture/images'

def label_mapper(val):
    return CATEGORY_MAP[val]



# CAMERA INTERFACE
def get_webcam():
    cap = cv.VideoCapture(0) #replace with filepath to read video
    #cap.open(0, cv.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while(True):
        ret, frame = cap.read() # frame captured stored in frame var
        cv.imshow('Input', frame)
        c = cv.waitKey(1)
        if c == 27: # escape key to exit
            break
    cap.release()
    cv.destroyAllWindows

# DATASET PROCESSING
input_data = []
for sub_folder_name in os.listdir(training_img):
    path = os.path.join(training_img, sub_folder_name)
    for fileName in os.listdir(path):
        if fileName.endswith(".jpg"):
            img = cv.imread(os.path.join(path, fileName))
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = cv.resize(img, (225, 225))
            #'input_data' stores the input image array and its corresponding label or category name
            input_data.append([img, sub_folder_name])

img_data, labels = zip(*input_data)
labels = list(map(label_mapper, labels))
labels = np_utils.to_categorical(labels)

# NEURAL NETWORK
model = def_model_param()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.fit(np.array(img_data), np.array(labels), epochs=15)
model.save("gesture-model.h5")
# NN validate model
# NN use model


