from nn_util import Selu
import tensorflow as tf
import numpy as np
from nn_util import ResetTensorflow

def NNBuild(layers, learning_rate=0.01):
    ResetTensorflow(100)

    # inputs for training
    X = tf.placeholder(tf.float32, shape=(None, layers[0]))
    T = tf.placeholder(tf.int64, shape=(None))

    # neural network building 
    h = [tf.layers.dense(X, layers[0], activation=Selu, name="h0")]
    for i in range(1, len(layers)):
        h.append(tf.layers.dense(h[i-1], layers[i], activation=Selu, name="h" + str(i)))
    logits = tf.layers.dense(h[len(layers)-1], layers[len(layers)-1], name="out")

    softmax = tf.nn.softmax(logits)
    xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=T, logits=logits)
    loss = tf.reduce_mean(xentropy, name="loss")

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    training_op = optimizer.minimize(loss)

    correct = tf.nn.in_top_k(logits, T, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
    
    return X, T, training_op, softmax, logits, accuracy

    
def NNTrain(Xtrain, Ttrain, X, T, training_op, accuracy, epochs=10000, load=None, save=None):
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        init.run()
        
        if load: 
            saver.restore(sess, load)
        for epoch in range(epochs):
            if epoch % 1000 == 0:
                acc_train = accuracy.eval({X: Xtrain, T: Ttrain})
                print("Epoch", epoch, "Train =", acc_train)
            sess.run([loss, training_op], {X: Xtrain, T: Ttrain})
        if save:
            saver.save(sess, save)
        acc_train = accuracy.eval({X: Xtrain, T: Ttrain})
        print("Train Accuracy: ", acc_train)

def NNRun(data, X, softmax, load=None):
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        init.run()
        if load: 
            saver.restore(sess, load)
        return softmax.eval({X: data})