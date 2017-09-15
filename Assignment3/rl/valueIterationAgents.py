import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            nextValues = self.values.copy()
            for j in self.mdp.getStates():
                if self.mdp.isTerminal(j):
                    nextValues[j] = self.mdp.getReward(j, None, j)
                else:
                    nextValues[j] = self.getQValue(j, self.getAction(j))
            self.values = nextValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        TranStateList = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0.0
        for i in TranStateList:
            # this is the next state
            nextState = i[0] 
            # this is the transition mode: T(s, a, s'), which is exactly the probability
            probability = i[1]
            # the formulas from slide
            qValue += probability * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None

        # initialize a list to store the values
        values = [0.0 for i in range(len(actions))]
        for i in range(len(actions)):
            values[i] = self.computeQValueFromValues(state, actions[i])
        # V star is exactly maximum value of Q star, so here we return the action of max value
        theIndex = values.index(max(values))
        return actions[theIndex]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
