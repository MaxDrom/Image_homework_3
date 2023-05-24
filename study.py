import matplotlib.pyplot as plt
import numpy as np
import random
import tensorflow as tf
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.layers import Dropout, BatchNormalization
from keras.models import Sequential
from sklearn.model_selection import train_test_split

seed = 0
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

img_size = 64
img_count = 1000

def make_model():
    model = Sequential()
    
    model.add(Conv2D(4, kernel_size=3, activation='relu',
    	      input_shape=(img_size, img_size, 3), padding = "valid"))
    model.add(Conv2D(4, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid',
                            data_format=None))

    model.add(Conv2D(8, kernel_size=3, activation='relu'))
    model.add(Conv2D(8, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid',
                            data_format=None))
    
    model.add(Conv2D(16, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid',
                           data_format=None))
    model.add(Dropout(rate=0.3))

    model.add(Flatten())
    model.add(Dense(75, activation="relu"))
    model.add(Dense(3, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy',
        metrics=['accuracy'],)
    return model

def make_data():
    tuples = {}
    tuples["spirals"] = []
    tuples["elliptic"] = []
    tuples["edge"] = []
    for gtype, data in tuples.items():
        data = [plt.imread(f"pictures/{gtype}_{i}.jpg") for i in range(img_count)]
        data = [d/np.max(d) for d in data]
        for i in range(len(data)):
            for ax in range(3):
                data.append(np.flip(data[i],axis = ax))
        tuples[gtype] = data

    sample_size = 3*(1+len(np.shape(tuples["edge"][0])))*img_count
    data = np.empty((sample_size, img_size, img_size, 3))
    labels = np.empty((sample_size, 3))
    for i in range(0, sample_size, 3):
        data[i] = tuples["spirals"][i//3]
        labels[i] = np.array([1, 0, 0])
        data[i+1] = tuples["elliptic"][i//3]
        labels[i+1] = np.array([0, 1, 0])
        data[i+2] = tuples["edge"][i//3]
        labels[i+2] = np.array([0, 0, 1])
    
    data_train, data_test, labels_train, labels_test =train_test_split(data, labels, test_size=0.2)
    data_train = data_train.reshape(-1, img_size, img_size, 3, 1)
    data_test = data_test.reshape(-1, img_size, img_size, 3, 1)
    return data_train, data_test, labels_train, labels_test


model = make_model()
print(model.summary())

data_train, data_test, labels_train, labels_test =make_data()
model.fit(data_train, labels_train,
validation_data=(data_test, labels_test),
epochs=10, batch_size=32)
model.save("model")