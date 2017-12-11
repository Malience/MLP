import tensorflow as tf
import numpy as np
from nn_util import ResetTensorflow
from nn_util import Selu

def AEBuild(inputs, hidden, learning_rate = 0.01, l2_reg = 0.00005):
    ResetTensorflow(80)

    activation = Selu
    regularizer = tf.contrib.layers.l2_regularizer(l2_reg)
    initializer = tf.contrib.layers.variance_scaling_initializer()

    X = tf.placeholder(tf.float32, shape=[None, inputs])

    weights1_init = initializer([inputs, hidden])

    weights1 = tf.Variable(weights1_init, dtype=tf.float32, name="weights1")
    weights2 = tf.transpose(weights1, name="weights2")

    biases1 = tf.Variable(tf.zeros(hidden), name="biases1")
    biases2 = tf.Variable(tf.zeros(inputs), name="biases2")

    hidden1 = activation(tf.matmul(X, weights1) + biases1)
    outputs = tf.matmul(hidden1, weights2) + biases2

    reconstruction_loss = tf.reduce_mean(tf.square(outputs - X))
    reg_loss = regularizer(weights1)
    loss = reconstruction_loss + reg_loss

    optimizer = tf.train.AdamOptimizer(learning_rate)
    training_op = optimizer.minimize(loss)
    
    return X, hidden1, training_op, loss

def AETrain(train, test, X, training_op, loss, epochs=10000, load=None, save=None):
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        init.run()
        if load: 
            saver.restore(sess, load)
        for epoch in range(epochs):
            sess.run(training_op, feed_dict={X: train})
            if epoch % 1000 == 0:
                acc_train = loss.eval({X: train})
                acc_test = loss.eval({X: test})
                print("Epoch", epoch, "Train =", acc_train, "Test =", acc_test)
        if save:
            saver.save(sess, save)
        acc_train = loss.eval({X: train})
        acc_test = loss.eval({X: test})
        #print accuracies
        print("Train Accuracy: ", acc_train)
        print("Test Accuracy: ", acc_test)
        
def AERun(data, X, hidden, load=None):
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        init.run()
        if load: 
            saver.restore(sess, load)
        return hidden.eval({X: data})
    
class PokeEncoder():
    def __init__(self, name, pokemon_layers=None, team_layers=None, matchup_layers=None):
        self.name = name
        self.p_layers = pokemon_layers
        self.t_layers = team_layers
        self.m_layers = matchup_layers
        self.poke_loc = "./networks/" + name + "_poke.ckpt"
        self.team_loc = "./networks/" + name + "_team.ckpt"
        self.match_loc = "./networks/" + name + "_match.ckpt"
    
    def transferWeights(self, loc):
        poke_loc = "./networks/" + loc + "_poke.ckpt"
        team_loc = "./networks/" + loc + "_team.ckpt"
        match_loc = "./networks/" + loc + "_match.ckpt"
        
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        with tf.Session() as sess:
            init.run()
            saver.restore(sess, self.poke_loc)
            saver.save(sess, poke_loc)
            saver.restore(sess, self.tean_loc)
            saver.save(sess, team_loc)
            saver.restore(sess, self.match_loc)
            saver.save(sess, match_loc)
    
    def trainPokemon(self, Xtrain, Xtest, save=False, load=False, epochs=10000, learning_rate=0.1):
        if load: #I shouldn't have to say this...
            load = self.poke_loc
        if save:
            save = self.poke_loc
        X, hidden, training_op, loss = AEBuild(self.p_layers[0], self.p_layers[1])
        AETrain(Xtrain, Xtest, X, training_op, loss, epochs=epochs, load=load, save=save)
    
    def runPokemon(self, data):
        X, hidden, training_op, loss = AEBuild(self.p_layers[0], self.p_layers[1])
        return AERun(data, X, hidden, self.poke_loc)
        
    
    def trainTeam(self, Xtrain, Xtest, save=False, load=False, epochs=10000, learning_rate=0.1):
        if load: #I shouldn't have to say this...
            load = self.team_loc
        if save:
            save = self.team_loc
        X, hidden, training_op, loss = AEBuild(self.t_layers[0], self.t_layers[1])
        AETrain(Xtrain, Xtest, X, training_op, loss, epochs=epochs, load=load, save=save)
    
    def runTeam(self, data):
        X, hidden, training_op, loss = AEBuild(self.t_layers[0], self.t_layers[1])
        return AERun(data, X, hidden, self.team_loc)
        
        
        
    def trainMatchup(self, Xtrain, Xtest, save=False, load=False, epochs=10000, learning_rate=0.1):
        if load: #I shouldn't have to say this...
            load = self.match_loc
        if save:
            save = self.match_loc
        X, hidden, training_op, loss = AEBuild(self.m_layers[0], self.m_layers[1])
        AETrain(Xtrain, Xtest, X, training_op, loss, epochs=epochs, load=load, save=save)
    
    def runMatchup(self, data):
        X, hidden, training_op, loss = AEBuild(self.m_layers[0], self.m_layers[1])
        return AERun(data, X, hidden, self.match_loc)
    
    def run(self, pokemon, currents):
        teams = self.runPokemon(pokemon)
        teams = teams.reshape(-1, self.t_layers[0] - 1)
        
        teams = np.hstack((teams, currents))

        matchups = self.runTeam(teams)
        matchups = matchups.reshape(-1, self.m_layers[0])

        return self.runMatchup(matchups)
    
    def halfRun(self, teams):
        matchups = self.runTeam(teams)
        matchups = matchups.reshape(-1, self.m_layers[0])

        return self.runMatchup(matchups)
        