import tensorflow as tf
import numpy as np
from IPython.display import clear_output
import advantage
from advantage import TypeAdvantage
from advantage import types


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
	
# compiles pokemon information
def CompilePokemon(pokemon):
    if not isinstance(pokemon, str):
        pokemon = getPoke(pokemon)
    poke = []
    poke.append(types[pokemon[2]])
    poke.append(types[pokemon[3]] if pokemon[3] == pokemon[3] else 0)
    poke.append(pokemon[5])
    poke.append(pokemon[6])
    poke.append(pokemon[7])
    poke.append(pokemon[8])
    poke.append(pokemon[9])
    poke.append(pokemon[10])
    return poke

#compiles team data along with health and current pokemon
def CompileTeamData(team, health):
    teamcompiled = []
    for i in range(6):
        poke = CompilePokemon(team[i][0])
        poke[2] *= health[i] / (poke[2] * 2 + 110) ##Normalize health
        teamcompiled.append(poke)
    return teamcompiled

def CompileTeam(team):
    teamcompiled = []
    for i in range(6):
        poke = CompilePokemon(team[i][0])
        teamcompiled.append(poke)
    return teamcompiled
	
import pandas as pd
#read in dataset
pokedex = pd.read_csv("Pokemon.csv")

#gets the pokemon from a sent id 
def getPoke(pokeid):
    return np.array(pokedex.loc[pokedex['#'] == pokeid])[0]

#gets the pokemon from a sent id (name)
def getPokeByName(pokeid):
    return np.array(pokedex.loc[pokedex['Name'] == pokeid])[0]

#create a team of six Pokemon
def createTeam(team):
    arr = []
    for i in range(6):
        arr.append(getPoke(int(team[i])) if team[i].isdigit() else getPokeByName(team[i]))
    return np.array(arr)

#displays Pokemon team along with stats
def DisplayPokemon(team, health):
    for i in range(6):
        s = str(i) + " - "
        s += str(team[i][1])
        s += "\tHP: " + (str(health[i]) if health[i] > 0 else "FNT")
        s += " ATK: " + str(team[i][6])
        s += " DEF: " + str(team[i][7])
        s += " SP. ATK: " + str(team[i][8])
        s += " SP. DEF: " + str(team[i][9])
        s += " SPD: " + str(team[i][10])
        s += "  Type " + str(team[i][2]) + " " + (str(team[i][3]) if team[i][3] == team[i][3] else "")
        print(s)