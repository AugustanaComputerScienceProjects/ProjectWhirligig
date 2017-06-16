# -*- coding: utf-8 -*-

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

sess = tf.InteractiveSession()

ROWS = 40
COLS = 60
TILE_SIZE = 28

blank_image = np.zeros((TILE_SIZE*ROWS,TILE_SIZE*COLS), np.float32)

def TRAIN_SIZE(num):
    print ('Total Training Images in Dataset = ' + str(mnist.train.images.shape))
    print ('--------------------------------------------------')
    x_train = mnist.train.images[:num,:]
    print ('x_train Examples Loaded = ' + str(x_train.shape))
    y_train = mnist.train.labels[:num,:]
    print ('y_train Examples Loaded = ' + str(y_train.shape))
    print('')
    return x_train, y_train

def TEST_SIZE(num):
    print ('Total Test Examples in Dataset = ' + str(mnist.test.images.shape))
    print ('--------------------------------------------------')
    x_test = mnist.test.images[:num,:]
    print ('x_test Examples Loaded = ' + str(x_test.shape))
    y_test = mnist.test.labels[:num,:]
    print ('y_test Examples Loaded = ' + str(y_test.shape))
    return x_test, y_test

def display_digit(num):
    print(y_train[num])
    label = y_train[num].argmax()
    image = x_train[num].reshape([28,28])
    plt.title('Example: %d  Label: %d' % (num, label))
    plt.imshow(image, cmap=plt.get_cmap('gray_r'))
    plt.show()
    
x_train, y_train = TRAIN_SIZE(55000)
    
def populate_blank_img():
    count = 0
    #for x in range(0,400):
        #blank_image[(TILE_SIZE*x_inc):(TILE_SIZE*y_inc), (index*TILE_SIZE):(TILE_SIZE*(index+1))] = x_train[count].reshape([TILE_SIZE, TILE_SIZE])
        #count += 1
        #index += 1
        #if (x+1)%20:
            #x_inc += 1
            #y_inc += 1
        #if index == 19:
            #index = 0
    for y in range(0,ROWS):
        for x in range(0,COLS):
            blank_image[(TILE_SIZE*y):(TILE_SIZE*(y+1)), (TILE_SIZE*x):(TILE_SIZE*(x+1))] = x_train[count].reshape([TILE_SIZE,TILE_SIZE])
            count += 1
    cv2.imshow('MNIST', blank_image), cv2.waitKey(0)
    
populate_blank_img()
cv2.destroyAllWindows()

#display_digit(0)
#display_digit(1)
#display_digit(2)
