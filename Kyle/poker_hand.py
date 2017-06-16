# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:50:00 2017

@author: kylemccaw15
"""

import tensorflow as tf
import tflearn
import numpy as np

#load the dataset
from tflearn.data_utils import load_csv
data, labels = load_csv('Poker Hand/poker-training.csv', target_column=10,
                        categorical_labels=True, n_classes=10)

# Build neural network
net = tflearn.input_data(shape=[None, 8])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, batch_size=16, show_metric=True)

#create a hand to test against the model
f = [2,1,8,1,9,1,5,1,11,1]
pred = model.predict([f])
print("Hand:",pred[0][1])