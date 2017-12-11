from nn_neuralnet import NNBuild
from nn_neuralnet import NNRun
from nn_neuralnet import NNTrain
from nn_util import Clear


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
