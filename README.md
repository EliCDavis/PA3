# Overview

This project was Dr. Archibald's end of the year programming assignment where student's where to create their own risk playing agent that would battle other classmates.  My team's submitted AI was the [mod_heuristic_ai.py](https://github.com/EliCDavis/PA3/blob/master/ai/mod_heuristic_ai.py) which used the [heuristic_ai.py](https://github.com/EliCDavis/PA3/blob/master/ai/heuristic_ai.py) as a bases for building our strategy.  This project was provided by Dr. Archibald and is nessesary for running the AI.  A [Python Imaging Library](http://www.pythonware.com/products/pil/) is also nessesary for running (I have only had success on running this on Windows 7).

Below is our agent competing for first place in our classes tournament.

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/hU5TTK8yEck/0.jpg)](http://www.youtube.com/watch?v=hU5TTK8yEck)

## Setup
risk.pyw

This game is relatively simple to play. Double click to run it. There are a few phases in the game.
1.  In pregame you create players.  

To create players, go to the Player menu and choose "New Player." You can type in a name, or, alternatively, click on "Set AI" and find the AI program you wish to use. Click ok when you're done with that.

Once you've created enough players, you can choose to start the game by clicking on "Start Game" under the player menu

The rest of the game proceeds by clicking on territories for placement, attacking, and fortification.

play_risk_ai.py

This will play a game between specified AIS. It saves the resulting logfile out to the matches folder, with the logfile name including participating agent names and the time of the match.

Usage: python play_risk_ai.py AI_1_File.py AI_1_Name AI_2_File.py AI_2_Name number_of_games

This gives each player 10 minutes per match, and limits the match to 5000 actions.  The player that goes first will alternate each game.

risk_game_viewer

This will allow you to visually follow a match logfile.  

Usage: python risk_game_viewer.py LOGFILE.log

You can click next to step through the actions and states, or hit play to have it do it automatically.  The player and action information are displayed on the left of the screen. 

## About

The agent we constructed for this programming assignment was a modification of the given **heutistic_ai.py** file that ranks given states after executing a given action.  The AI executes a certain heuristic based on the given state that the AI is in.  Only 2 heuristics were constructed for 6 of the 7 different turn types the the agent is faced with.  The heuristic method was modified to take in the original state the the ai is given, as well as the state which results from simulating an action.  For the “Pre Assign” turn type we wrote our own method for generating an action to take place in that state instead of  the traditional heuristic of evaluating each state that results from picking a territory.  The reason for this is to allow for more control over the strategy we want to implement through our agent.

The **preAssign()** function determines the best territory to claim given the current state. It is broken up into three stages, because as the unclaimed territories become smaller. The values for those territories changes dramatically. The initial stage runs until five territories are claimed or until each player has 30 armies remaining. The second stage runs until 22 armies remain, and the final will select until no territories remain. In the first two stages, multiple territories are given an initial appeal value according to our belief of their strategic board value. Before the territory with the highest appeal value can be selected, the **checkMonopoly()** function is called. If a monopoly can be claimed or is two turns from being claimed, then the checkMonopoly()  function will claim a territory from that continent. To ensure this a large appeal is given to that territory. In the final stage, it is more difficult to determine what territories are available. Instead of given a value for each individual territory; we determine the value of territory by first calling the **checkPercentage()**  function. This obtains the number of territories owned and unowned by both players and compares it  to the total number of territories in the continent. The checkMonopoly()  function is called again to ensure that no monopolies can be claimed.
	
The **pre_place_heuristic()** method is used to evaluate a state’s worth that returns a value correlating to it’s appeal.  This heuristic is used when evaluating every turn type except for ‘Pre Assign’ type and ‘Attack’ type.  The main focus of the heuristic is to prioritize territories that are a front and have a higher chance to face battle.  The heuristic value increases with the number of armies that are on a territory that has a neighbor that is owned by the enemy.  There is no increase in value for armies on territories that have no enemy neighbors.  Therefor any action taken will be one that increases a territory’s army whose neighbor is an opponent.  Their is a special case in this heuristic in which we look for certain territories and check if they are considered ‘chokeholds’.   A choke hold is defined as a friendly territory on the outskirts of a cluster of friendly territories that touch enemy territories and only have one friendly neighbor.  The reason we look for these is because they are more likely to undergo battle than just a regular territory on the front.  Another reason for this definition is for special cases for defending certain regions from being broken into through the choke holds.  For example if we own the South American continent as well as Mexico, and the opponent owns all of the North American continent except for Mexico, then Mexico is our choke hold, and needs extra protection to keep from being broken into.  Notice chokeholds heuristic value is being multiplied by a constant and then cube rooted whereas a regular territory is having its heuristic only square rooted.  This is to make it so that adding troops to choke holds are more appealing than just regular territories at first, and so they will always be treated.  But as more troops are added to a certain territory the appeal is ever decreasing, and eventually adding troops to non-chokehold territories gives a greater appeal.  This way we’re not just avoiding adding troops to non-chokehold territories.  The other advantage to having the heuristic value nth rooted is so that we don’t just end up adding all our troops to one of our territories, and that they become more evenly distributed.

![Graph Example](http://i.imgur.com/zTxZGbW.png)

	
When it comes to the agent’s attack phase we have the agent begin looking at the board in a more offensive rather than defensive way in the **attack_heuristic()** method written.  To make sense of this, we get +1 for each army we have in our territory, but -2 for each army our opponent has in their territory.  Doing so gives enough incentive for us to make an attack more often than not.  Having this heuristic flipped (+2 for each army we have and -1 each they have) we go from winning ~80% games to ~10% games because more often than not we’re too afraid to lose a precious troop and will opt not to attack, and just allow ourselves to get whittled away by the enemy.  The agent’s aggressiveness is also reflected in its thirst for obtaining continent bonuses.  When it comes to evaluating a state the attack_heuristic gives -50 for each continent bonus our opponent has, and +100 for each continent bonus we have.  In the experience of playing risk our group has seen how much of an impact owning a single continent can make and removing some one’s continent bonus when it rolls around to be their turn again is extremely important.  When it comes to the attack phase it’s important for the agent to actually attack so these heuristics are helpful in making sure that things are attacked if possible, and that more important territories are attacked ( to claim continent or break opponent continent ).  Future improvements could be implemented to keep the agent from spreading units to thin, because at the moment theres never not a reason to attack.
	
## Things to Explore
One aspect we wish we drilled down in further was creating a system for evaluating each territory more in depth.  Most evaluation a territory gets is seeing how many armies it has and whether or not that territory is ours or the opponents.  One idea our group had in the very beginning was a sort of territory evaluation that takes into account other aspects of a territory that define it without context of ownership and armies, such as what continent it belonged to and how valuable is that continent compared to others.  This evaluation would also include things such as how many neighbors the territory has and where exactly the territory resides in a continent and the map itself.  This aspect of things sounds more of a learning problem than anything else, and with enough tuning it could greatly improve all aspects of the heuristics such as when it comes to placing troops and deciding what territories to attack.
	
Another idea for improvement would to be a search in our attack stage x amount of states deep to give the agent a strategy for a turn, or at least part of a turn.  That way we would be able to see the opportunity to claim a continent that’s only two territories away, or alternatively break our opponent’s continent bonus.
