import riskengine
import riskgui
import random
from aihelper import *
from risktools import *
from turbohelper import *


# This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""

    # if time_left is not None:
    # Decide how much time to spend on this decision

    # Get the possible actions in this state
    actions = getAllowedActions(state)

    print('Heuristic AI : Player', state.players[state.current_player].name, 'considering', len(actions), 'actions, with time left: ',time_left)

    # To keep track of the best action we find
    best_action = None
    best_action_value = None

    # Evaluate each action
    for a in actions:

        # Simulate the action, get all possible successors
        successors, probabilities = simulateAction(state, a)

        # Compute the expected heuristic value of the successors
        current_action_value = 0.0

        for i in range(len(successors)):
            # Each successor contributes its heuristic value * its probability to this action's value
            current_action_value += (heuristic(successors[i]) * probabilities[i])

        # Store this as the best action if it is the first or better than what we have found
        if best_action_value is None or current_action_value > best_action_value:
            best_action = a
            best_action_value = current_action_value

    # Return the best action
    return best_action


def heuristic(state):
    """Returns a number telling how good this state is"""

    #Go through all territory evaluations and determine state based on their attractiveness
    h = 1000
    for t in state.board.territories:
        h -= evalTerritory(state, t)
       

    return h


def evalContinent(state):
    return 0


def evalTerritory(state, territoryID):
    """
    This ranks territories on how important they are to the AI
    If this is our territory we want to protect it.
    If this is an enemies territory we want to claim it.

    :type state: RiskState
    :type territoryID: int
    """

    # This is the variable containing how much appeal this territory has to our agent.
    tAppeal = 0

    # figure out what continent the territory is in..
    continent = None

    """
    for cont in state.board.continents:

        if territoryID in cont.territories:
            #assert isinstance(cont, RiskContinent)
            continent = cont
    """

    # figure out importance of continent..
    territory = state.board.territories[territoryID.id]

    # Figure out how many neighbors it has that are not our territories, and the size of their armies.
    # This is good for Fortifying!!!

    # Grab all our neighbors
    neighbors = territory.neighbors

    # Go through each neighbor and look at their armies.
    for neighbor in neighbors:

        if state.board.territories != None:

            # if the neighbor is ours the appeal is greater the more armies we have surrounding this territory
            if isOurTerritory(state, state.board.territories[neighbor]):
                tAppeal += state.armies[neighbor]
            else:
                tAppeal -= state.armies[neighbor]

    # 2nd Appeal
    # Prioritizing Attacking Continents Rules
    # Don't Spread to Thin!
    # 

    # Monopoly check on continent it's contained in.

    # If this territory is completely surrounded by our own territories, we don't need to bother with it
    #tAppeal = 0

    return tAppeal




def isOurTerritory(state, territory):
    ourID = state.current_player

    if state.owners[territory.id] == ourID:
        return True
    return False
# Stuff below this is just to interface with Risk.pyw GUI version
# DO NOT MODIFY


def aiWrapper(function_name, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    print('AI Wrapper created state. . . ')
    game_state.print_state()
    action = getAction(game_state)
    return translateAction(game_state, action)


def Assignment(player):
    # Need to Return the name of the chosen territory
    return aiWrapper('Assignment')


def Placement(player):
    # Need to return the name of the chosen territory
    return aiWrapper('Placement')


def Attack(player):
    # Need to return the name of the attacking territory, then the name of the defender territory
    return aiWrapper('Attack')


def Occupation(player, t1, t2):
    # Need to return the number of armies moving into new territory
    occupying = [t1.name, t2.name]
    aiWrapper('Occupation', occupying)


def Fortification(player):
    return aiWrapper('Fortification')
