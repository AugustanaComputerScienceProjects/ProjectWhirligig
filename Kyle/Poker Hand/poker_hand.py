# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:50:00 2017

@author: kylemccaw15
"""

import tensorflow as tf
import tflearn
import numpy as np

#Very poor accuracy right now, ~50%. Needs more work as ideas are learned.

#clear graph
tf.reset_default_graph()

#load the dataset
from tflearn.data_utils import load_csv
data, labels = load_csv('poker-training.csv', target_column=10,
                        categorical_labels=True, n_classes=10)

# Build neural network
net = tflearn.input_data(shape=[None, 10])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 10, activation='sigmoid')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, batch_size=50, show_metric=True)

#create a hand to test against the model
f = [1,2,1,8,1,11,1,5,1,4]
pred = model.predict([f])
print("Hand:",pred[0][1])