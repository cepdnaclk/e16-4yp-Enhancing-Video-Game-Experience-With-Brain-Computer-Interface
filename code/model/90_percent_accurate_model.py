import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D
from tensorflow.keras.models import Sequential


x = np.load('x.npy')
y = np.load('y.npy')


print(x.shape)
print(y.shape)

# shuffle the dataset
x,y = shuffle(x,y)

x = x.astype('float32')
xmax = np.amax(x)
print(xmax)
x = x / xmax
print(x[0])


# creating train data and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)


x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

#print(x_test.shape)


'''
model = tf.keras.Sequential([
     tf.keras.layers.Flatten(input_shape=(129,7)),
     tf.keras.layers.Dense(100, activation='relu'),
     tf.keras.layers.Dense(4, activation = 'sigmoid')
])
'''

#defining model
model=Sequential()
#adding convolution layer
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(129,7,1)))
#adding pooling layer
model.add(MaxPool2D(2,2))
#adding fully connected layer
model.add(Flatten())
model.add(Dense(200,activation='relu'))
model.add(Dense(100,activation='relu'))
#adding output layer
model.add(Dense(4,activation='softmax'))

print(model.summary())

epochs = 20

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=epochs)

score = model.evaluate(x_test, y_test, verbose=0)

print(score[0])
print(score[1])

y_predicted = model.predict(x_test)

correct = 0
wrong = 0

for i in range (0,51200):
   # print("Predicted: ",np.argmax(y_predicted[i]),"     Real: ", y_test[i])

    if np.argmax(y_predicted[i]) == y_test[i]:
        correct  = correct + 1
    else:
        wrong = wrong + 1

print(correct,"/5120 correctly predicted")
print(wrong,"/5120 wrongly predicted")


print(x_test.shape)
print(y_test.shape)

