"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    # Initialize a frontier, and push the initial state into the frontier
    frontier = util.Stack()
    frontier.push([(problem.getStartState(), 'move', 0)])
    # Initialize a explored set to store the visited nodes
    exploredSet = set()

    # Check the content of frontier
    while not frontier.isEmpty():
        stateList = list()
        stateList = frontier.pop()
        # print (stateList)
        # What we focus on is the next state, not the (previous state + next state), so we should take the last element
        nextState = stateList[len(stateList) - 1]
        # Check the current state is goal or not
        if problem.isGoalState(nextState[0]):
            # Initial a path, which is the way to the goal state
            path = list()
            for eachMove in stateList:
                path.append(eachMove[1])
            # If the initial state is the goal state, there's no need to explore other nodes, so that's called special condition
            if len(path) == 1:
                return path[0]
            # This is the normal condition, we should convey the path except the first one, because we haven't define what's "move"
            else:
                return path[1:]
        # If this is a state which we don't visit, add it to the explored set(this is called GSA)
        if not nextState[0] in exploredSet:
            exploredSet.add(nextState[0])
            # Give me your child nodes
            for childState in problem.getSuccessors(nextState[0]):
                nextStateList = stateList[:]
                # we focus on the path, so we have to record the every move from the initial state to the current one
                nextStateList.append(childState)
                frontier.push(nextStateList)

    # Or maybe there's no way to the goal state
    else:
        return "There's no way."



def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # This question is almost same to the previous one, just change the data structure from stack to queue 
    # Initialize the frontier, which should be the queue structure
    frontier = util.Queue()
    frontier.push([(problem.getStartState(), 'move', 0)])
    exploredSet = set()

    while not frontier.isEmpty():
        stateList = list()
        stateList = frontier.pop()
        nextState = stateList[len(stateList) - 1]

        if problem.isGoalState(nextState[0]):
            path = list()
            for eachMove in stateList:
                path.append(eachMove[1])
        
            if len(path) == 1:
                return path[0]
            else:
                return path[1:]

        if not nextState[0] in exploredSet:
            exploredSet.add(nextState[0])
            for childState in problem.getSuccessors(nextState[0]):
                nextStateList = stateList[:]
                nextStateList.append(childState)
                frontier.push(nextStateList)
    else:
        return "There's no way."

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # This question is quite similar to the previous one
    # Initialize the frontier, which should be the priority queue structure
    frontier = util.PriorityQueue()
    frontier.push([(problem.getStartState(), 'move', 0)], 0)
    exploredSet = set()

    while not frontier.isEmpty():
        stateList = list()
        stateList = frontier.pop()
        nextState = stateList[len(stateList) - 1]

        if problem.isGoalState(nextState[0]):
            path = list()
            for eachMove in stateList:
                path.append(eachMove[1])
        
            if len(path) == 1:
                return path[0]
            else:
                return path[1:]

        if not nextState[0] in exploredSet:
            exploredSet.add(nextState[0])
            for childState in problem.getSuccessors(nextState[0]):
                nextStateList = stateList[:]
                nextStateList.append(childState)
                # Initialize a action list, which stores the cost of every next move
                actionList = list()
                for state in nextStateList[1:]:
                    actionList.append(state[1])
                # the data structure of priority queue needs two parameters, ont is item and other is cost
                frontier.push(nextStateList, problem.getCostOfActions(actionList))
    else:
        return "There's no way."


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # This question is quite similar to the previous one
    # Initialize the frontier, which should be the priority queue structure, but we have to add a heuristic function
    frontier = util.PriorityQueue()
    frontier.push([(problem.getStartState(), 'move', 0)], heuristic(problem.getStartState(), problem))
    exploredSet = set()

    while not frontier.isEmpty():
        stateList = list()
        stateList = frontier.pop()
        nextState = stateList[len(stateList) - 1]

        if problem.isGoalState(nextState[0]):
            path = list()
            for eachMove in stateList:
                path.append(eachMove[1])
        
            if len(path) == 1:
                return path[0]
            else:
                return path[1:]

        if not nextState[0] in exploredSet:
            exploredSet.add(nextState[0])
            for childState in problem.getSuccessors(nextState[0]):
                nextStateList = stateList[:]
                nextStateList.append(childState)
                # Initialize a action list, which stores the cost of every next move
                actionList = list()
                for state in nextStateList[1:]:
                    actionList.append(state[1])
                # the data structure of priority queue needs two parameters, ont is item and other is cost plus heuristic of current state
                frontier.push(nextStateList, problem.getCostOfActions(actionList) + heuristic(childState[0], problem))
    else:
        return "There's no way."


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
