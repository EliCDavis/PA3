import riskengine
import riskgui
import random
from aihelper import *
from turbohelper import *
from risktools import *
from pa2_learn_d_tree import *

myDTree = None

#This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""
    global myDTree
    
    if myDTree is None:
        print 'Loading DTree'
        myDTree = loadDTree('pa2_trees\Dataset_216918_attacker_ai_P1_attacker_ai_P2_20141107-085947_10.dtree')
        print 'Done.'
    
    #Get the possible actions in this state
    actions = getAllowedActions(state)
        
    #Select a Random Action
    myaction = random.choice(actions)
    
    if state.turn_type == 'PreAssign':
        myaction = pickAssign(state, actions)
        #print 'I chose the action: ', myaction
    if state.turn_type == 'Attack':
        myaction = actions[0]
    
    if state.turn_type == 'Place' or state.turn_type == 'Fortify' or state.turn_type == 'PrePlace':
        possible_actions = []

        for a in actions:
            if a.to_territory is not None:
                for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                    if state.owners[n] != state.current_player:
                        possible_actions.append(a)
                    
        if len(possible_actions) > 0:
            myaction = random.choice(possible_actions)
                    

    return myaction

def pickAssign(state, actions):
    
    #Set up the data instance to pass into the decision tree
    
    #Are we the first player?
    first_player = 0
    if state.current_player == 0:
        first_player = 1
        
    owners = state.owners[:]
    for t in range(len(owners)):
        if owners[t] == state.current_player:
            owners[t] = 1
        elif owners[t] is not None:
            owners[t] = 0
            
    owners.insert(0,first_player)
    
    best_v = -1
    best_a = None
    
    for a in actions:
        instance = owners[:]
        instance[state.board.territory_to_id[a.to_territory]+1] = 1
        av = evaluateAssignAction(instance, a)
        if av > best_v:
            best_v = av
            best_a = a
            #print '  Found best action: ', best_a
            #print '  With value: ', av
    
    return best_a
    
def evaluateAssignAction(instance, action):
    #Randomly complete the rest of the instance
    snones = []
    
    for t in range(len(instance)):
        if instance[t] is None:
            snones.append(t)
    #print 'SNONES: ', snones
    
    num_samples = 100
    action_value = 0
    
    for s in range(num_samples):
        new_owner = 0
        nones = snones[:]
    
        while len(nones) > 0:
            #print 'HOWDY!'
            nt = random.choice(nones)
            nones.remove(nt)
            instance[nt] = new_owner
            if new_owner == 0:
                new_owner = 1
            else:
                new_owner = 0
    
        #Randomly filled out instance, evaluate
        action_value  += myDTree.get_prob_of_win(instance)
        #print 'Action value: ', action_value
    
    return float(action_value) / float(num_samples)
    
#Stuff below this is just to interface with Risk.pyw GUI version
#DO NOT MODIFY
    
def aiWrapper(function_name, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    action = getAction(game_state)
    return translateAction(game_state, action)
            
def Assignment(player):
#Need to Return the name of the chosen territory
    return aiWrapper('Assignment')
     
def Placement(player):
#Need to return the name of the chosen territory
     return aiWrapper('Placement')

    
def Attack(player):
 #Need to return the name of the attacking territory, then the name of the defender territory    
    return aiWrapper('Attack')

   
def Occupation(player,t1,t2):
 #Need to return the number of armies moving into new territory      
    occupying = [t1.name,t2.name]
    aiWrapper('Occupation',occupying)
   
def Fortification(player):
    return aiWrapper('Fortification')

  