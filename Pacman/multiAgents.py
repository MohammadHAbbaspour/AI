# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
from pacman import GameState
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()   # getting the score of successor of current game state.
        capsules_positions = currentGameState.getCapsules()     # getting the capsules positions
        food_positions_list = newFood.asList()   # getting the food positions as list
        minGhostDistance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])    # getting the minimum distance of ghost from pacman
        for ghost_timer in newScaredTimes:  # checking if ghost is scared or not
            if ghost_timer > 0:
                score += 500    # if ghost is scared then add 500 to score
        if minGhostDistance <= 1:   # checking if ghost is near to pacman or not
            return float('-inf')    
        if len(food_positions_list) == 0:   # checking if there is no food left
            return float('inf')    # if there is no food left then return infinity
        elif len(food_positions_list) < len(currentGameState.getFood().asList()):   # checking if food is eaten or not
            score += 5  # if food is eaten then add 5 to score
        else:
            minFoodDistance = min([manhattanDistance(newPos, food) for food in food_positions_list])    # getting the minimum distance of food from pacman
            score -= 5 * minFoodDistance        # subtracting 5 times minimum distance of food from pacman from score
        if len(capsules_positions) != 0:    # checking if there is any capsule left or not
            minCapsuleDistance = min([manhattanDistance(newPos, capsule) for capsule in capsules_positions])    # getting the minimum distance of capsule from pacman
            if minCapsuleDistance == 0: # checking if capsule is eaten or not
                score += 100    # if capsule is eaten then add 100 to score
        if action == Directions.STOP:   # checking if pacman is stopped or not
            score -= 1
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        def terminal_state(gameState: GameState):
            if gameState.isWin() or gameState.isLose(): # checking if game is won or lost
                return True
            return False

        def pacman_value(gameState: GameState, agentIdx, depth):
            self.nodesCount += 1
            if terminal_state(gameState):   
                return self.evaluationFunction(gameState)   
            if depth == self.depth: # checking if depth is reached or not
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)  # getting the legal actions of pacman
            (max_score, action) = max([(ghost_value(gameState.generateSuccessor(agentIdx, act), 1, depth), act)
                                        for act in legalActions], 
                                        key = lambda x : x[0])  # getting the maximum score and action
            if depth == 0:  
                return action   
            return max_score 

        def ghost_value(gameState: GameState, agentIdx, depth):
            self.nodesCount += 1
            agentIdx = agentIdx % gameState.getNumAgents()  # getting the index of agent(0<= agentIdx < numAgents)
            if terminal_state(gameState):
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)  # getting the legal actions of ghost
            if depth == self.depth: # checking if depth is reached or not
                return self.evaluationFunction(gameState)
            if agentIdx + 1 == gameState.getNumAgents():    # checking if next agent is pacman or not
                min_score = min([pacman_value(gameState.generateSuccessor(agentIdx, act), 0, depth + 1) for act in legalActions])   # getting the minimum score
            else:   # if next agent is ghost
                min_score = min([ghost_value(gameState.generateSuccessor(agentIdx, act), agentIdx+1, depth) for act in legalActions])   # getting the minimum score
            return min_score

        return pacman_value(gameState, 0, 0)    # returning the action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        def terminal_state(gameState: GameState):   
            if gameState.isWin() or gameState.isLose(): # checking if game is won or lost
                return True
            return False

        def pacman_value(gameState: GameState, agentIdx, depth, alpha, beta):
            self.nodesCount += 1
            if terminal_state(gameState):
                return self.evaluationFunction(gameState)
            if depth == self.depth: # checking if depth is reached or not
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)  # getting the legal actions of pacman
            max_score = float('-inf')   # initializing the maximum score
            action = Directions.STOP    # initializing the action
            for act in legalActions:
                score = ghost_value(gameState.generateSuccessor(agentIdx, act), 1, depth, alpha, beta)  # getting the score of ghost(minimum score)
                (max_score, action) = (score, act) if max_score < score else (max_score, action)    # updating the maximum score and action
                if max_score > beta:    
                    return max_score
                alpha = max(alpha, max_score)   # updating the alpha
            if depth == 0:
                return action   # if we are in the root node, we return the action else return the value of action
            return max_score

        def ghost_value(gameState: GameState, agentIdx, depth, alpha, beta):
            self.nodesCount += 1
            agentIdx = agentIdx % gameState.getNumAgents()  # getting the index of agent(0<= agentIdx < numAgents)
            if terminal_state(gameState):
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)  # getting the legal actions of ghost
            min_score = float('inf')    # initializing the minimum score
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            for act in legalActions:
                if agentIdx + 1 == gameState.getNumAgents():    # checking if next agent is pacman or not
                    score = pacman_value(gameState.generateSuccessor(agentIdx, act), 0, depth + 1, alpha, beta) # getting the score of pacman(maximum score)
                else:
                    score = ghost_value(gameState.generateSuccessor(agentIdx, act), agentIdx+1, depth, alpha, beta) # getting the score of ghost(minimum score)
                min_score = min(min_score, score)   # updating the minimum score
                if min_score < alpha:
                    return min_score
                beta = min(beta, min_score) # updating the beta
            return min_score

        return pacman_value(gameState, 0, 0, float('-inf'), float('inf'))   # returning the action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def terminal_state(gameState: GameState):
            if gameState.isWin() or gameState.isLose():
                return True
            return False

        def pacman_value(gameState: GameState, agentIdx, depth):
            if terminal_state(gameState):
                return self.evaluationFunction(gameState)
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)
            (max_score, action) = max([(ghost_value(gameState.generateSuccessor(agentIdx, act), 1, depth), act)
                                        for act in legalActions], 
                                        key = lambda x : x[0])  # getting the maximum score and action
            if depth == 0:
                return action
            return max_score

        def ghost_value(gameState: GameState, agentIdx, depth):
            agentIdx = agentIdx % gameState.getNumAgents()
            if terminal_state(gameState):
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIdx)  # getting the legal actions of ghost
            length = len(legalActions)  # getting the length of legal actions
            if depth == self.depth: # checking if depth is reached or not
                return self.evaluationFunction(gameState)
            if agentIdx + 1 == gameState.getNumAgents():    # checking if next agent is pacman or not
                min_score = sum([pacman_value(gameState.generateSuccessor(agentIdx, act), 0, depth + 1) / length for act in legalActions])  # getting the mathematical expectation
            else:
                min_score = sum([ghost_value(gameState.generateSuccessor(agentIdx, act), agentIdx+1, depth) / length for act in legalActions])  # getting the mathematical expectation
            return min_score

        return pacman_value(gameState, 0, 0)    # returning the action


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()  # getting the position of pacman
    food = currentGameState.getFood()   # getting the food
    ghostStates = currentGameState.getGhostStates() # getting the ghost states
    newScaredTimes = [
        ghostState.scaredTimer for ghostState in ghostStates]

    score = currentGameState.getScore() # getting the score
    capsules_positions = currentGameState.getCapsules() # getting the capsules positions
    food_positions_list = food.asList() # getting the food positions list
    minGhostDistance = min([manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates])  # getting the minimum distance of ghost from pacman
    for ghost_timer in newScaredTimes:
        if ghost_timer > 0:
            score += 500    # increasing the score if ghost is scared
    if minGhostDistance <= 2:
        return float('-inf')    # returning the minimum score if ghost is too close to pacman
    if len(food_positions_list) == 0:
        return float('inf') # returning the maximum score if there is no food left(means pacman has won)
    elif len(food_positions_list) < len(currentGameState.getFood().asList()):
        score += 5  # increasing the score if food is eaten
    else:
        minFoodDistance = min([manhattanDistance(pos, food) for food in food_positions_list])   # getting the minimum distance of food from pacman
        score += 5/minFoodDistance      # increasing the score if food is closer to pacman(because the minFoodDistance has opposite effect)
    if len(capsules_positions) != 0:    # checking if there is any capsule left or not
        minCapsuleDistance = min([manhattanDistance(pos, capsule) for capsule in capsules_positions])   # getting the minimum distance of capsule from pacman
        if minCapsuleDistance == 0: 
            score += 100    # increasing the score if capsule is eaten
        else:
            score += 100/minCapsuleDistance # increasing the score if capsule is closer to pacman(because the minCapsuleDistance has opposite effect)
    return score


# Abbreviation
better = betterEvaluationFunction
