from nn_neuralnet import NNBuild
from nn_neuralnet import NNRun
from nn_neuralnet import NNTrain
from nn_util import Clear
import pandas as pd
import numpy as np
import advantage
from advantage import TypeAdvantage
from advantage import types
from nn_util import ResetTensorflow
from nn_util import CompilePokemon
from nn_util import CompileTeamData
import tensorflow as tf
import math
import random
from nn_util import Clear
from nn_util import DisplayPokemon


#agent class to play with
class Agent():
    #initialization
    def __init__(self, name):
        self.name = name
    
    #The action it should use given the current state
    def getAction(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        #Uses the attack corresponding to the higher stat (Physical if Attack, Special if Sp. Attack)
        return 0 if team[current][6] > team[current][8] else 1 
    
    #If it should switch given the battle's current state
    def getSwitch(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        return current + 1
		

#class to manage if user wants to battle
class Player(Agent):
    #initialization
    def __init__(self, name):
        Agent.__init__(self, name)
    
    #gets action user wants to use
    def getAction(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        #prints options
        print("What should ", team[current][1], "do?")
        print("0 - Physical Attack")
        print("1 - Special Attack")
        print("2 - Switch Pokemon")
        print("3 - Display Pokemon")
        action = input(": ")
        #displays information
        while not action.isdigit() or action == "3":
            if action == "3":
                print("~~~~~~~Your Team~~~~~~~")
                DisplayPokemon(team, health)
                print("~~~~~~~Enemy Team~~~~~~~")
                DisplayPokemon(enemyteam, enemyhealth)
            else:
                print("Action ", action, " is invalid!")
            print("What should", team[current][1], "do?")
            print("0 - Physical Attack")
            print("1 - Special Attack")
            print("2 - Switch Pokemon")
            action = input(": ")
        Clear()
        return int(action) 
    
    #gets information to switch pokemon from the user
    def getSwitch(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        print("Bring out which Pokemon?")
        print("0 - ", team[0][1], " %FAINTED%" if health[0] <= 0 else "", "*CURRENT*" if current == 0 else "")
        print("1 - ", team[1][1], " %FAINTED%" if health[1] <= 0 else "", "*CURRENT*" if current == 1 else "")
        print("2 - ", team[2][1], " %FAINTED%" if health[2] <= 0 else "", "*CURRENT*" if current == 2 else "")
        print("3 - ", team[3][1], " %FAINTED%" if health[3] <= 0 else "", "*CURRENT*" if current == 3 else "")
        print("4 - ", team[4][1], " %FAINTED%" if health[4] <= 0 else "", "*CURRENT*" if current == 4 else "")
        print("5 - ", team[5][1], " %FAINTED%" if health[5] <= 0 else "", "*CURRENT*" if current == 5 else "")
        switch = input(": ")
        while (not switch.isdigit()) or health[int(switch)] <= 0 or switch == current:
            print("Invalid selection!")
            print("Bring out which Pokemon?")
            print("0 - ", team[0][1], " %FAINTED%" if health[0] <= 0 else "", "*CURRENT*" if current == 0 else "")
            print("1 - ", team[1][1], " %FAINTED%" if health[1] <= 0 else "", "*CURRENT*" if current == 1 else "")
            print("2 - ", team[2][1], " %FAINTED%" if health[2] <= 0 else "", "*CURRENT*" if current == 2 else "")
            print("3 - ", team[3][1], " %FAINTED%" if health[3] <= 0 else "", "*CURRENT*" if current == 3 else "")
            print("4 - ", team[4][1], " %FAINTED%" if health[4] <= 0 else "", "*CURRENT*" if current == 4 else "")
            print("5 - ", team[5][1], " %FAINTED%" if health[5] <= 0 else "", "*CURRENT*" if current == 5 else "")
            switch = input(": ")
        return int(switch)

class NNAgent(Agent):
    #initialization
    def __init__(self, name, team_layers, action_layers, switch_layers, autoencoder=None):
        Agent.__init__(self, name)
        self.ae = autoencoder
        self.t_layers = team_layers
        self.a_layers = action_layers
        self.s_layers = switch_layers
        self.a_trained = False
        self.s_trained = False
        self.t_trained = False
        self.t_data = []
        
        self.t_loc = "./networks/" + self.name + "_choose"
        self.a_loc = "./networks/" + self.name + "_action"
        self.s_loc = "./networks/" + self.name + "_switch"
    
    #The action it should use given the current state
    def getAction(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        if self.ae and self.ae.p_layers:
            data = self.ae.run(np.array(CompileTeamData(team, health) + CompileTeamData(enemyteam, enemyhealth)), 
                               np.array([current, enemycurrent]).reshape(-1,1))
        else:
            data = np.hstack((np.array(CompileTeamData(team, health)).flatten(), np.array([current])))
            data = np.hstack((data, np.array(CompileTeamData(enemyteam, enemyhealth)).flatten(), np.array([enemycurrent])))
            data = data.reshape(1,-1)
        
        X, T, training_op, softmax, logits, accuracy = NNBuild(self.a_layers)
        
        options = NNRun(data, X, softmax, load=self.a_loc if self.a_trained else None)
        
        #can't choose to switch if there is only 1 pokemon left
        if sum(health > 0) <= 1:
            return np.argmax(options[:1])
        return np.argmax(options)
    
    #If it should switch given the battle's current state
    def getSwitch(self, current, enemycurrent, team, enemyteam, health, enemyhealth):
        if self.ae and self.ae.p_layers:
            data = self.ae.run(np.array(CompileTeamData(team, health) + CompileTeamData(enemyteam, enemyhealth)), 
                               np.array([current, enemycurrent]).reshape(-1,1))
        else:
            data = np.hstack((np.array(CompileTeamData(team, health)).flatten(), np.array([current])))
            data = np.hstack((data, np.array(CompileTeamData(enemyteam, enemyhealth)).flatten(), np.array([enemycurrent])))
            data = data.reshape(1,-1)
        
        X, T, training_op, softmax, logits, accuracy = NNBuild(self.s_layers)
        
        options = NNRun(data, X, softmax, load=self.s_loc if self.s_trained else None)[0]
        options = np.argsort(options)
        maxi = 0
        while health[options[maxi]] <= 0 or options[maxi] == current:
            maxi += 1
        return options[maxi]
        
    
    def getTeam(self, data):
        if self.ae and self.ae.p_layers:
            data = self.ae.runPokemon(data)
            
        X, T, training_op, softmax, logits, accuracy = NNBuild(self.t_layers)
        
        
        ones = np.ones(data.shape[0]).reshape(-1,1)
        
        data0 = np.hstack((data, np.zeros(data.shape[0]).reshape(-1,1)))
        data1 = np.hstack((data, ones))
        ones += np.ones(data.shape[0]).reshape(-1,1)
        data2 = np.hstack((data, ones))
        ones += np.ones(data.shape[0]).reshape(-1,1)
        data3 = np.hstack((data, ones))
        ones += np.ones(data.shape[0]).reshape(-1,1)
        data4 = np.hstack((data, ones))
        ones += np.ones(data.shape[0]).reshape(-1,1)
        data5 = np.hstack((data, ones))
        
        
        choices0 = NNRun(data0, X, logits, load= self.t_loc if self.t_trained else None)
        choices1 = NNRun(data1, X, logits, load= self.t_loc if self.t_trained else None)
        choices2 = NNRun(data2, X, logits, load= self.t_loc if self.t_trained else None)
        choices3 = NNRun(data3, X, logits, load= self.t_loc if self.t_trained else None)
        choices4 = NNRun(data4, X, logits, load= self.t_loc if self.t_trained else None)
        choices5 = NNRun(data5, X, logits, load= self.t_loc if self.t_trained else None)
        
        choice0 = np.argmax(choices0)
        choice1 = np.argmax(choices1)
        choice2 = np.argmax(choices2)
        choice3 = np.argmax(choices3)
        choice4 = np.argmax(choices4)
        choice5 = np.argmax(choices5)
        
        return [choice0, choice1, choice2, choice3, choice4, choice5]
    
    def trainTeam(self, team, effectiveness, epochs=10000, effmod=0.01):
        data = team
        if self.ae and self.ae.p_layers:
            data = self.ae.runPokemon(data)
        
        
        Xtrain = np.hstack((data, np.arange(6).reshape(-1,1)))
        
        print(Xtrain)
        
        X, T, training_op, softmax, logits, accuracy = NNBuild(self.t_layers)
        Ttrain = NNRun(Xtrain, X, logits, load= self.t_loc if self.t_trained else None)
        
        print(Ttrain)
        print(np.array(effectiveness) * effmod)
        Ttrain += (np.array(effectiveness) * effmod).reshape(-1,1)
        
        Ttrain = Ttrain.flatten()
        print(Ttrain)
        
        NNTrain(Xtrain, Ttrain, X, T, training_op, accuracy, epochs=epochs, load= self.t_loc if self.t_trained else None, save= self.t_loc)
        self.t_trained = True