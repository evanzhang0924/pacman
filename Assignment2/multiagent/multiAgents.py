from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions. X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # This is the coordinates of pacman
        # print(newPos)
        # This is the boolean square of food
        # print(newFood)
        # list of ghost states
        # print(newGhostStates)

        # get two lists of food and capsules
        foodList = prevFood.asList()
        capsulesPos = currentGameState.getCapsules()
        # get ghost position
        ghostPos = [newGhostState.getPosition() for newGhostState in newGhostStates]

        evaFunc = currentGameState.getScore()

        # create a list that stores the manhattan distance of every food or capsule to pacman
        foodDist = list()
        for i in foodList:
            foodDist.append(manhattanDistance(i, newPos))
        for i in capsulesPos:
            foodDist.append(manhattanDistance(i, newPos))

        # create a list that stores the manhattan distance of every ghost to pacman
        ghostDist = list()
        for i in ghostPos:
            ghostDist.append(manhattanDistance(i, newPos))

        evaFunc += 1.0 * min(ghostDist) / 2
        if len(foodDist) == 0:
            return evaFunc
        else:
            return evaFunc - min(foodDist)
        

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        agentNum = gameState.getNumAgents()
        utilityValue = []
        actions = gameState.getLegalActions(0)

        # start minimax
        for action in actions: 
            utilityValue.append(self.minValue(gameState.generateSuccessor(0, action), 1, self.depth, 1, agentNum - 1))

        maxUtilityValue = max(utilityValue)
        thisIndex = utilityValue.index(maxUtilityValue)

        return actions[thisIndex]
    # this is the max value function, which pacman should call
    def maxValue(self, gameState, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose() or currentDepth == grossDepth:
            return self.evaluationFunction(gameState)

        utilityValue = float("-inf")
        for action in gameState.getLegalActions(currentAgentIndex):
            utilityValue = max(utilityValue, self.minValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth + 1, grossDepth, 1, lastAgentIndex))
        return utilityValue
    # this is the min value function, which ghost should call
    def minValue(self, gameState, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        utilityValue = float("inf")
        # maybe there're more than 1 ghost
        if currentAgentIndex == lastAgentIndex:
            for action in gameState.getLegalActions(currentAgentIndex):
                utilityValue = min(utilityValue, self.maxValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth, grossDepth, 0, lastAgentIndex))
        else:
            for action in gameState.getLegalActions(currentAgentIndex):
                utilityValue = min(utilityValue, self.minValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth, grossDepth, currentAgentIndex + 1, lastAgentIndex))
        return utilityValue




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined() 

        # this question is quite similar to the previous one, just add two variables to store the temp value
        agentNum = gameState.getNumAgents()
        (utilityValue, actions) = self.maxValue(gameState, float("-inf"), float("inf"), 0, self.depth, 0, agentNum - 1)
        maxUtilityValue = max(utilityValue)
        thisIndex = utilityValue.index(maxUtilityValue)

        return actions[thisIndex]

    def maxValue(self, gameState, alpha, beta, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose() or currentDepth == grossDepth:
            return self.evaluationFunction(gameState)

        value = float("-inf")
        if currentDepth == 0:
            utilityValue, actions = [], []

            for action in gameState.getLegalActions(currentAgentIndex):
                value = max(value, self.minValue(gameState.generateSuccessor(currentAgentIndex, action), alpha, beta, currentDepth + 1, grossDepth, 1, lastAgentIndex))
                utilityValue.append(value)
                actions.append(action)
                if value > beta:
                    return utilityValue, actions
                alpha = max(alpha, value)
            return utilityValue, actions

        else:
            for action in gameState.getLegalActions(currentAgentIndex):
                value = max(value, self.minValue(gameState.generateSuccessor(currentAgentIndex, action), alpha, beta, currentDepth + 1, grossDepth, 1, lastAgentIndex))
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value

    def minValue(self, gameState, alpha, beta, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        utilityValue = float("inf")
        if currentAgentIndex == lastAgentIndex:
            for action in gameState.getLegalActions(currentAgentIndex):
                utilityValue = min(utilityValue, self.maxValue(gameState.generateSuccessor(currentAgentIndex, action), alpha, beta, currentDepth, grossDepth, 0, lastAgentIndex))
                if utilityValue < alpha:
                    return utilityValue
                beta = min(beta, utilityValue)
            return utilityValue
        else:
            for action in gameState.getLegalActions(currentAgentIndex):
                utilityValue = min(utilityValue, self.minValue(gameState.generateSuccessor(currentAgentIndex, action), alpha, beta, currentDepth, grossDepth, currentAgentIndex + 1, lastAgentIndex))
                if utilityValue < alpha:
                    return utilityValue
                beta = min(beta, utilityValue)
            return utilityValue



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
        # util.raiseNotDefined()

        # this question is quite similar to the previous one, just change the minValue function
        # to the mean function
        agentsNum = gameState.getNumAgents()
        agentsAction = gameState.getLegalActions(0)
        values = []
        for i in agentsAction:
            values.append(self.meanValue(gameState.generateSuccessor(0, i), 1, self.depth, 1,  agentsNum - 1))
            maxValue = max(values)
        maxIndex = values.index(maxValue)

        return agentsAction[maxIndex]

    def maxValue(self, gameState, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose() or currentDepth == grossDepth:
            return self.evaluationFunction(gameState)

        value = float("-inf")
        for action in gameState.getLegalActions(currentAgentIndex):
            value = max(value, self.meanValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth + 1, grossDepth, 1, lastAgentIndex))
        return value

    def meanValue(self, gameState, currentDepth, grossDepth, currentAgentIndex, lastAgentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        value = []
        if currentAgentIndex == lastAgentIndex:
            for action in gameState.getLegalActions(currentAgentIndex):
                value.append(self.maxValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth, grossDepth, 0, lastAgentIndex))
            return 1.0 * sum(value) / len(value)
        else:
            for action in gameState.getLegalActions(currentAgentIndex):
                value.append(self.meanValue(gameState.generateSuccessor(currentAgentIndex, action), currentDepth, grossDepth, currentAgentIndex + 1, lastAgentIndex))
            return 1.0 * sum(value) / len(value)

    


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # this question is quite similar to the first question
    currentFoodGrid = currentGameState.getFood()
    foodList = currentFoodGrid.asList()
    capsulesPos = currentGameState.getCapsules()
    pacPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    ghostPos = [ghostState.getPosition() for ghostState in ghostStates]

    evaFunc = currentGameState.getScore()
    foodDist = list()
    for i in foodList:
        foodDist.append(manhattanDistance(i, pacPos))
    for i in capsulesPos:
        foodDist.append(manhattanDistance(i, pacPos))

    ghostDist = list()
    for i in ghostPos:
        ghostDist.append(manhattanDistance(i, pacPos))

    evaFunc += 1.0 * min(ghostDist) / 2

    if len(foodDist) == 0:
        return evaFunc
    else:
        return evaFunc - min(foodDist)


# Abbreviation
better = betterEvaluationFunction

