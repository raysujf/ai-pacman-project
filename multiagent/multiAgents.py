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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        result=0
        food=(newFood.asList())
        for i in food:
            distant=manhattanDistance(i,newPos)
            if distant<4:
                result+=4-distant
        ghost=currentGameState.getGhostPositions()
        for i in range(len(ghost)):
            distant=manhattanDistance(ghost[i],newPos)
            if newScaredTimes[i]:
                if distant<7:result+=10-distant
            elif manhattanDistance(ghost[i],newPos)<=1:
                result=-float("inf")
        if action=="Stop":
            result=-float("inf")

        return successorGameState.getScore()+result

        
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
        result=[]
        for action in gameState.getLegalActions(0):
            next_step=gameState.generateSuccessor(0,action)
            result.append((self.ghost(next_step,self.depth),action))
        return max(result)[1]

    def pacman(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        value=-float("inf")
        for action in gameState.getLegalActions(0):
            next_gameState=gameState.generateSuccessor(0,action)
            value=max(value,self.ghost(next_gameState,depth))
        return value
            

    def ghost(self, gameState, depth, index=1):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState)
        value=float("inf")
        for action in gameState.getLegalActions(index):
            next_gameState=gameState.generateSuccessor(index,action)
            if index!=gameState.getNumAgents()-1:
                value=min(value,self.ghost(next_gameState,depth,index+1))
            else:
                value=min(value,self.pacman(next_gameState,depth-1))
        return value
            

    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.result=[]

    def getAction(self, gameState):
        self.result=[]
        self.pacman(gameState,self.depth,float("-inf"),float("inf"))
        return max(self.result)[1]

    def pacman(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        value=-float("inf")
        for action in gameState.getLegalActions(0):
            next_gameState=gameState.generateSuccessor(0,action)
            val=self.ghost(next_gameState,depth,alpha,beta)
            value=max(value,val)
            if value>beta:
                return value
            alpha=max(alpha,value)
            if depth==self.depth:self.result.append((val,action))
        return value
            

    def ghost(self, gameState, depth, alpha, beta, index=1):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState)
        value=float("inf")
        for action in gameState.getLegalActions(index):
            next_gameState=gameState.generateSuccessor(index,action)
            if index!=gameState.getNumAgents()-1:
                value=min(value,self.ghost(next_gameState,depth,alpha,beta,index+1))
                if value<alpha:
                    return value
                beta=min(beta,value)
            else:
                value=min(value,self.pacman(next_gameState,depth-1,alpha,beta))
                if value<alpha:return value
                beta=min(beta,value)
        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        result=[]
        for action in gameState.getLegalActions(0):
            next_step=gameState.generateSuccessor(0,action)
            result.append((self.ghost(next_step,self.depth),action))
        return max(result)[1]

    def pacman(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        value=-float("inf")
        for action in gameState.getLegalActions(0):
            next_gameState=gameState.generateSuccessor(0,action)
            value=max(value,self.ghost(next_gameState,depth))
        return value
            

    def ghost(self, gameState, depth, index=1):
        if gameState.isLose() or gameState.isWin() or depth==0:
            return self.evaluationFunction(gameState)
        value=0
        num=len(gameState.getLegalActions(index))
        for action in gameState.getLegalActions(index):
            next_gameState=gameState.generateSuccessor(index,action)
            if index!=gameState.getNumAgents()-1:
                val=self.ghost(next_gameState,depth,index+1)
                value+=val/num
            else:
                val=self.pacman(next_gameState,depth-1)
                value+=val/num
        return value


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood().asList()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    result=currentGameState.getScore()
    food=[manhattanDistance(i,Pos) for i in Food]
    if food:result+=10/min(food)
    for i in food:
        if i<4:
            result+=4-i
    Ghost=currentGameState.getGhostPositions()
    for i in range(len(GhostStates)):
        distant=manhattanDistance(Ghost[i],Pos)
        if ScaredTimes[i]:
            result+=100/distant
        elif distant<=1:
            result-=1000
        else:result+=distant/10
    return result

# Abbreviation
better = betterEvaluationFunction
