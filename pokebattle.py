#imports
import pandas as pd
import numpy as np
import advantage
from advantage import TypeAdvantage
from advantage import types
from nn_util import ResetTensorflow
from nn_util import CompilePokemon
from nn_util import CompileTeamData
from nn_util import createTeam
from nn_util import DisplayPokemon
import tensorflow as tf
import math
import random
from nn_util import Clear

#Actions
#0 - Physical Attack
#1 - Special Attack
#2 - Switch Pokemon

#Battle manager
def PokeBattle(team1, team2, agent1, agent2, verbose=True):
    team1 = createTeam(team1)
    team2 = createTeam(team2)
    health1 = np.array([team1[0][5], team1[1][5], team1[2][5], team1[3][5], team1[4][5], team1[5][5]]) * 2 + 110
    health2 = np.array([team2[0][5], team2[1][5], team2[2][5], team2[3][5], team2[4][5], team2[5][5]]) * 2 + 110
    current1 = current2 = 0
    won = -1
    action1=0
    action2=0
    damageswing = [0,0]
    effectiveness = [[0,0,0,0,0,0], [0,0,0,0,0,0]]
    rounds = 0
    tdata = []
    actions = []
    currents = []
    swings = []
    
    #calculate damage
    def Damage(Attacker, Defender, SP):
        return (84 * (Attacker[8 if SP else 6] * 2 + 5) / (Defender[8 if SP else 6] * 2 + 5) + 2) * TypeAdvantage(Attacker[2], Attacker[3], Defender[2], Defender[3])
    #for using an attack and updating health variables
    def Attack(atk):
        #global damageswing
        if atk == 1:
            damage = Damage(team1[current1], team2[current2], action1 == 1)
            effectiveness[0][current1] += damage
            effectiveness[1][current2] -= damage
            damageswing[0] = damage
            #damageswing += damage
            if verbose:
                print(team1[current1][1], "used ", "Attack" if action1 == 0 else "SP. Attack", " against", 
                      team2[current2][1], "for ", damage, " damage!")
            health2[current2] -= damage
            if health2[current2] <= 0:
                health2[current2] = 0
                if verbose: 
                    print(team2[current2][1], "has fainted!")
            return damage
        elif atk == 2:
            damage = Damage(team2[current2], team1[current1], action2 == 1)
            effectiveness[1][current2] += damage
            effectiveness[0][current1] -= damage
            damageswing[1] = damage
            #damageswing -= damage
            if verbose:
                print(team2[current2][1], "used ", "Attack" if action2 == 0 else "SP. Attack", " against", 
                      team1[current1][1], "for ", damage, " damage!")
            health1[current1] -= damage
            #Pokemon fainted
            if health1[current1] <= 0:
                health1[current1] = 0
                if verbose: 
                    print(team1[current1][1], "has fainted!")
            #Information taken from the perspective of player        
            return -damage 
    
    #compiles team data
    def CompileData(team):
        data = []
        #compiles team 1 first then team 2
        if team == 1:
            data += CompileTeamData(team1, health1) + CompileTeamData(team2, health2)
        #compiles team 2 first then team 1
        else:
            data += CompileTeamData(team2, health2) + CompileTeamData(team1, health1)
        return data
                              
            
    #def 
    #for playing multiple games
    while won < 0 and rounds < 100:
        damageswing = [0,0]
        currents += [current1] + [current2] + [current2] + [current1]
        if verbose:
            print()
        action1 = agent1.getAction(current1, current2, team1, team2, health1, health2)
        action2 = agent2.getAction(current2, current1, team2, team1, health2, health1)
        #swap Pokemon (team 1)
        if action1 == 2:
            current1 = agent1.getSwitch(current1, current2, team1, team2, health1, health2)
            if verbose: 
                print(agent1.name, "has swapped out for", team1[current1][1], "!")
        #swap Pokemon (team 2)
        if action2 == 2:
            current2 = agent2.getSwitch(current2, current1, team2, team1, health2, health1)
            if verbose: 
                print(agent2.name, "has swapped out for", team2[current2][1], "!")
        
        if action1 != 2 and action2 != 2:
            if team1[current1][10] > team2[current2][10] or (team1[current1][10] == team2[current2][10] and bool(random.getrandbits(1))):
                Attack(1)
                if health2[current2] > 0:
                    Attack(2)
            else:
                Attack(2)
                if health1[current1] > 0:
                    Attack(1)
        
        elif action1 != 2:
            Attack(1)
        elif action2 != 2:
            Attack(2)
        
        #Pokemon fainted
        if health1[current1] <= 0:
            if sum(health1) <= 0:
                won = 2
            else:
                current1 = agent1.getSwitch(current1, current2, team1, team2, health1, health2)
                if verbose: 
                    print(agent1.name, "has swapped out for", team1[current1][1], "!")
        if health2[current2] <= 0:
            if sum(health2) <= 0:
                won = 1
            else:
                current2 = agent2.getSwitch(current2, current1, team2, team1, health2, health1)
                if verbose: 
                    print(agent2.name, "has swapped out for", team2[current2][1], "!")
                    
        tdata += CompileData(1) + CompileData(2)
        actions += [action1] + [action2]
        swings += [damageswing[0] - damageswing[1]] + [damageswing[1] - damageswing[0]]
        
        rounds += 1
    print(agent1.name if won == 1 else agent2.name, "has won!")
    return tdata, currents, actions, swings, effectiveness, won