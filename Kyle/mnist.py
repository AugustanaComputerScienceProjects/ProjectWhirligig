# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import mnist data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

#start 
import tensorflow as tf
sess = tf.InteractiveSession()

#placeholders
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

#create variables
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

#initialize all variables with tensors full of zeros
sess.run(tf.global_variables_initializer())

#implement regression model
y = tf.matmul(x,W) + b

#specify a loss function (indicates how bad the model's
#prediction was on a single example
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))

#train the model
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#repeatedly run train_step to train in batches
for _ in range(1000):
  batch = mnist.train.next_batch(100)
  train_step.run(feed_dict={x: batch[0], y_: batch[1]})
  
#evaluate model; should return an accuracy of roughly 92%
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

#import custom number to test it against our model
import cv2
new_number = cv2.imread('number.png',0)

#divide by 255 to create series of 1's and 0's that matches MNIST format
new_number_adjusted = 1 - (new_number / 255)

#reshape image to a single column of size 784
new_number_adjusted = new_number_adjusted.reshape((784,))

#test the number against the model
feed_dict = {x: [new_number_adjusted]}
classification = sess.run(y, feed_dict)

#print Softmax Regression scores
print(classification)

#evaluate and return index with the highest score
import numpy as np
print(np.argmax(y.eval(feed_dict))