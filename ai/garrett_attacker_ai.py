import riskengine
import riskgui
import random
from aihelper import *
from turbohelper import *
from risktools import *

#This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):


    """This is the main AI function.  It should return a valid AI action for this state."""
    
    #Get the possible actions in this state
    myaction = None
    actions = getAllowedActions(state)
    myaction = random.choice(actions)

    """ Picks the first 35 territories """
    if state.turn_type == 'PreAssign':
        myaction = preAssign(state)
        #print "Armies: ", state.players[state.current_player].free_armies

    """ Place additional 15 armies anywhere on the map """
    if state.turn_type == 'PrePlace'or state.turn_type == 'Place':
        myaction = place(state)
        #print "Armies: ", state.players[state.current_player].free_armies

    if state.turn_type == 'Attack':
        myaction = toAttack(state)

    if state.turn_type == 'Occupy':
        myaction, my_action_value = moveUnits(state, state.last_attacker)
    if state.turn_type == 'Fortify':
        myaction = random.choice(actions)
   
    # print "state: ", state.turn_type
   
    return myaction

def preAssign(state):

    best_action = None
    best_action_value = None
    actions = getPreAssignActions(state)


    if state.players[state.current_player].free_armies >= 30:
        for a in actions:
        
            if str(a.to_territory) == "Laos":
                action_value = 7

            elif str(a.to_territory) == "Brazil":
                action_value = 6

            elif str(a.to_territory) == "Chile":
                action_value = 5
         
            elif str(a.to_territory) == "Iceland":
                action_value = 4
          
            elif str(a.to_territory)== "Alaska":
                action_value = 3
           
            elif str(a.to_territory) == "Eastern Australia":
                action_value = 2
         
            elif str(a.to_territory) == "Greenland":
                action_value = 1

            else:
                action_value = 0

            monopoly_action = checkMonopoly(state, a.to_territory)
            if monopoly_action > 0:
                action_value = monopoly_action
            
            if best_action_value is None or action_value > best_action_value:
                best_action = a
                best_action_value = action_value
                #print "Update Action: ", best_action_value         

    elif state.players[state.current_player].free_armies > 22:
        for a in actions:
            
            if str(a.to_territory)== "Alaska":
                action_value = 10
         
            elif str(a.to_territory) == "Eastern Australia":
                action_value = 9
           
            elif str(a.to_territory) == "Mexico":
                action_value = 8
        
            elif str(a.to_territory) == "Western Africa":
                action_value = 7
             
            elif str(a.to_territory) == "Western Austrialia":
                action_value = 6
             
            elif str(a.to_territory) == "Columbia":
                action_value = 5
              
            elif str(a.to_territory) == "Madagascar":
                action_value = 4
               
            elif str(a.to_territory) == "Indonesia":
                action_value = 3
          
            elif str(a.to_territory) == "South Africa":
                action_value = 2
            
            elif str(a.to_territory) == "Kamchatka":
                action_value = 1
                   
            else:
                action_value = 0

            monopoly_action = checkMonopoly(state, a.to_territory)
            if monopoly_action > 0:
                action_value = monopoly_action
          
            if best_action_value is None or action_value > best_action_value:
                best_action = a
                best_action_value = action_value
                #print "Update Action: ", best_action_value
                
        #print "Best Action: ", best_action.to_territory
    else:
        bestPer = 0.0
        for a in actions:
            terrPer = checkPercentage(state, a.to_territory)
            monopoly_action = checkMonopoly(state, a.to_territory)
            if monopoly_action > 0:
                terrPer = monopoly_action

            if bestPer == 0.0 or terrPer > bestPer:
                best_action = a
                bestPer= terrPer  

        #print "Best Action: ", best_action.to_territory
        #print "Best Action Value: ", bestPer

    return best_action

def place(state):

    bestPlace = None
    best_place_value = None
    actions = getPrePlaceActions(state)

    if state.players[state.current_player].free_armies >= 0:
        for a in actions:
            neighNum = neighborAppeal(state, a.to_territory)
            if neighNum != 0 or neighNum != -1:
                monopoly_check = checkMonopoly(state, a.to_territory)
                units, unitValue = moveUnits(state, a.to_territory)
                neighNum += monopoly_check + unitValue

            if bestPlace == None or neighNum > best_place_value:
                bestPlace = a
                best_place_value = neighNum

    return bestPlace  

def toAttack(state):
    best_action = None
    best_action_value = None
    actions = getAttackActions(state)
    
    for a in actions:
        action_value = 0
        myTerritory = None
        eTerritory = None
        myTerr = a.from_territory
        enemyTerr = a.to_territory

        if myTerr != None and enemyTerr != None:

            myTerritory = state.board.territories[state.board.territory_to_id[myTerr]].id
            eTerritory = state.board.territories[state.board.territory_to_id[enemyTerr]].id

            #print "My armies: ", state.armies[myTerritory]
            #print "Their armies: ", state.armies[eTerritory]
            
            if state.armies[myTerritory] > state.armies[eTerritory]:
                action_value = (state.armies[myTerritory] - state.armies[eTerritory]) * 10
            else:
                action_value = -100
            if state.armies[eTerritory] == 1:
                action_value += 100
                

            monopoly_check = checkMonopoly(state, enemyTerr)
            action_value += monopoly_check

            myNeighbor = neighborAppeal(state, myTerr)
            enemyNeighbor = neighborAppeal(state, enemyTerr)
            neAppeal = myNeighbor - enemyNeighbor
            action_value += neAppeal
            #print myTerr, " attack ", enemyTerr, "appeal: ", action_value

            if best_action_value is None or action_value > best_action_value:
                best_action = a
                best_action_value = action_value
                #print best_action.from_territory, " attack is best :", best_action.to_territory

    if best_action == None:
        actions = getAllowedActions(state)
        best_action = random.choice(actions)
    """
    if best_action_value < 0:
        fortifyAction = None
        fortifyActionValue = None
        state.turn_type = 'Fortify'
        actions = getFortifyActions(state)
        for action in actions:
            appeal = 0
            action = None
            if a.from_territory != None:
                action, appeal = moveUnits(state, a.from_territory)

            if fortifyAction == None or appeal > fortifyActionValue:
                fortifyAction = action
                fortifyActionValue = appeal

        return fortifyAction"""

    return best_action

def isOurTerritory(state, territory):
    ourID = state.current_player

    if state.owners[territory.id] == ourID:
        return True
    return False

def isTheirTerritory(state, territory):
    ourID = state.current_player

    if state.owners[territory.id] != ourID and state.owners[territory.id] != None:
        return True
    return False

def moveUnits(state, territory):
    best_action = None
    best_action_value = None
    movTroops = 0
    troopCount = 0
    check1 = None
    check2 = None
    bestTroopCount = None
    terrProp = None

    for c in state.board.continents:
        for t in state.board.continents[c].territories:
            if territory == state.board.territories[t].name or territory == state.board.territories[t].id:
                terrProp = t
    territory = state.board.territories[terrProp]
    neighbors = territory.neighbors
    
    for a in getAllowedActions(state):
        appeal = 0
        if a.to_territory != None:
            check1 = neighborAppeal(state, state.board.territories[state.board.territory_to_id[a.to_territory]].name) 
        if a.from_territory != None:
            check2 = neighborAppeal(state, state.board.territories[state.board.territory_to_id[a.from_territory]].name) 
        if check1 != 0 or check2 != -1:
            if a.from_territory == territory:
                currchoke = chokehold(state, a.from_territory)
                if currchoke != None:
                    appeal += -200
                newchoke = chokehold(state, a.to_territory)
                if newchoke != None:
                    appeal += 150
                for neighbor in neighbors:
                    if neighbor != None:
                        if isTheirTerritory(state, state.board.territories[neighbor]):
                            currTroops = fortifyTroops(state, state.board.territories[neighbor])
                            if currTroops != 1:
                                enemyTroops += currTroops
                
                troopCount = a.troops
                if enemyTroops == 0:
                    movTroops = state.armies[terrProp] - 1
                elif enemyTroops < 2:
                    movTroops = state.armies[terrProp] - 2
                else: 
                    movTroops = state.armies[terrProp] - 3

        #print "Troop count: ", troopCount
        #print "Troops to move: ", movTroops
        if movTroops < troopCount:
            troopCount = 0

        if best_action == None or appeal > best_action_value or troopCount > bestTroopCount:
            best_action = a
            best_action_value = appeal
            bestTroopCount = troopCount


        #if neighborAppeal(state, oldTerr) == 0:
    return best_action, best_action_value

def neighborAppeal(state, territory):

    tAppeal = 0
    iTerr = 0
    tTerr = 0
    uTerr = 0
    troops = 0
    terrProp = None

    for c in state.board.continents:
        for t in state.board.continents[c].territories:
            if territory == state.board.territories[t].name:
                terrProp = t
    
    for neighbor in state.board.territories[terrProp].neighbors:
        if isOurTerritory(state, state.board.territories[neighbor]):
             iTerr +=1
        elif isTheirTerritory(state, state.board.territories[neighbor]):
            tTerr += 1
            troops += fortifyTroops(state, state.board.territories[neighbor])
        else:
            uTerr += 1

    totalNeighbor = iTerr + tTerr + uTerr
    if iTerr == totalNeighbor:
        return 0
    elif tTerr == totalNeighbor:
        return -1
    elif (totalNeighbor - iTerr) <= 2:
        tAppeal = 10
    elif (totalNeighbor - iTerr) <= 1:
        tAppeal = 20
    else:
        tAppeal = 5

    percentIncrease = checkPercentage(state, territory)
    tAppeal = ((tAppeal * percentIncrease)+ troops) / state.armies[terrProp]   

    return tAppeal


def fortifyTroops(state, territory):
    troops = state.armies[territory.id]
    if isTheirTerritory(state, territory):
        if troops > 1:
            appeal = troops * 30
        else:
            appeal = 0
    else:
        if troops > 2:
            appeal = -troops * 20
        else:
            appeal = 20

    return appeal

def chokehold(state, territory):
    joinedContinent = None
    best_join = None
    best_join_value = None


    for a in state.board.continents:
        for b in state.board.continents[a].territories:
            if territory == state.board.territories[b].name:
                continent = b

    neighbors = state.board.territories[territory].neighbors
    for neighbor in neighbors:
        appeal = 0
        for c in state.board.continents:
            for d in state.board.continents[c].territories:
                if neighbor == state.board.territories[d].name:
                    nContinent = c
                if nContinent != continent:
                    joinedContinent = d
                if isTheirTerritory(state, d):
                    appeal = checkMonopoly(state, d)
                    check = checkPercentage(state, d)
                    appeal += check
                if best_join == None or appeal > best_join_value:
                    best_join = d
                    best_join_value = appeal

    return best_join      

def checkPercentage(state, territory):
    iOwn = 0
    tOwn = 0
    uOwn = 0
    total = 0
    iPer = 0.0
    tPer = 0.0
    uPer = 0.0
    totalPer = 0.0

    for c in state.board.continents:
        for t in state.board.continents[c].territories:
            if territory == state.board.territories[t].name:
                continent = c
 
    for t in state.board.continents[continent].territories:
        if isOurTerritory(state, state.board.territories[t]):
            iOwn += 1
        elif isTheirTerritory(state, state.board.territories[t]):
            tOwn += 1 
        else:
            uOwn += 1

    num = iOwn + tOwn + uOwn
    if iOwn == num:
        return 0
    subtotal = iOwn + (num - tOwn) + (num - uOwn)  
    total = subtotal * 10
    totalPer = total / num
    return totalPer


def checkMonopoly(state, territory): 

    Owned = 0
    Appeal = 0
    notOwned = 0
    theyOwn = 0
    continent = None

    for c in state.board.continents:
        
        for t in state.board.continents[c].territories:
            if territory == state.board.territories[t].name:
                continent = c
    
    for t in state.board.continents[continent].territories:
        if isOurTerritory(state,state.board.territories[t]):
            Owned += 1
         
        elif isTheirTerritory(state, state.board.territories[t]):
            theyOwn += 1
       
        else:
            notOwned += 1
        
    if len(state.board.continents[continent].territories) == (Owned + 1) or len(state.board.continents[continent].territories) == (theyOwn + 1) or len(state.board.continents[continent].territories) == (theyOwn + Owned + 1):
        Appeal += 50 
    if len(state.board.continents[continent].territories) == (Owned + 2):
        Appeal += 25
    if (len(state.board.continents[continent].territories) == theyOwn):
        Appeal += 200    

    return Appeal

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

