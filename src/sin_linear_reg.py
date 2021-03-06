# The example is based on the
# https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/2_BasicModels/linear_regression.py
# implementation of linear regression.

from __future__ import print_function

import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
import math
import random
rng = numpy.random

# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50


# Training Data
def source_func(x):
    bi = 5
    w = 2
    w_sin = 3
    random_top = 10

    return round(w * x + bi + w_sin * math.sin(x) + random.uniform(0, random_top), 3)

X_s = range(1, 20)
Y_s = [source_func(x) for x in X_s]

train_X = numpy.asarray(X_s)
train_Y = numpy.asarray(Y_s)

n_samples = train_X.shape[0]

# tf Graph Input
X = tf.placeholder("float")
Y = tf.placeholder("float")

# Set model weights
W = tf.Variable(rng.randn(), name="weight")
W_sin = tf.Variable(rng.randn(), name="sin_weight")
b = tf.Variable(rng.randn(), name="bias")

# Construct a linear model
pred = tf.add(tf.add(tf.multiply(X, W), b), tf.multiply(W_sin, tf.sin(X)))

# Mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
# Gradient descent
#  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                "W=", sess.run(W), "b=", sess.run(b), "W_sin=", sess.run(W_sin))

    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    # Graphic display
    plt.plot(train_X, train_Y, 'ro', label='Original data')
    plt.plot(train_X, sess.run(W) * train_X + sess.run(b) + numpy.sin(train_X) * sess.run(W_sin), label='Fitted line')
    plt.legend()
    plt.show()
