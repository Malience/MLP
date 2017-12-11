import tensorflow as tf
import numpy as np
from IPython.display import clear_output

def Clear():
    clear_output()

#resets tensor flow
def ResetTensorflow(seed):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)
    
#selu method    
def Selu(z, scale=1.0507009873554804934193349852946, alpha=1.6732632423543772848170429916717):
    return scale * tf.where(z >= 0.0, z, alpha * tf.nn.elu(z))
	
	#enumerates sent team
def EnumerateTeam(team, health, current):
    teamcompiled = []
    for i in range(6):
        poke = CompilePokemon(team[i])
        poke[2] *= health[i] ##Normalize health
        teamcompiled += poke
    teamcompiled += [current]
    return teamcompiled
    
#sample enumeration    
def EnumerateSamples(numSamples=10000):
    teams = []
    for i in range(numSamples):
        teams.append(EnumerateTeam(np.random.randint(1, TOTAL_POKEMON + 1, (6)), 
                                   np.random.random((6)), 
                                   np.random.randint(0, 6)))
    return teams
    
def EnumerateMatchups(teams):
    return