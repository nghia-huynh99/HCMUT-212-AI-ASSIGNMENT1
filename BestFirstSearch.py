from itertools import combinations
from queue import PriorityQueue


class State:
    size = 0
    sumOfRow = None
    sumOfCol = None

    def __init__(self, board, currentIndex, size=0, sumOfRow=None, sumOfCol=None):
        self.board = board
        self.currentIndex = currentIndex
        self.priority = self.__evaluate()
        if (size != 0) & (sumOfRow is not None) & (sumOfCol is not None):
            State.size = size
            State.sumOfRow = sumOfRow
            State.sumOfCol = sumOfCol

    def __lt__(self, other):
        if other is None:
            return False
        return self.priority < other.priority

    def __sumIndex(self, List):
        s = 0
        for i in range(self.size):
            s += List[i] * (i + 1)
        return s

    def __column(self, index):
        return [row[index] for row in self.board]

    def isGoal(self):
        for i in range(self.size):
            if self.__sumIndex(self.__column(i)) != self.sumOfCol[i]:
                return False
        return True

    def isValid(self):
        for i in range(self.size):
            if self.__sumIndex(self.__column(i)) > self.sumOfCol[i]:
                return False
        return True

    def __evaluate(self):
        currentColSum = 0
        for i in range(State.size):
            currentColValue = self.__sumIndex(self.__column(i))
            target = State.sumOfCol[i]
            if currentColValue > target / 2:
                currentColSum += currentColValue / target
            else:
                currentColSum += (target - currentColValue) / target
        return (State.size - self.currentIndex) / (currentColSum + 0.1)

    def __genPossibleMoves(self, target):
        index = [i for i in range(1, self.size + 1)]
        combine = []
        res = []
        for num in range(1, self.size + 1):
            combine += list(combinations(index, num))
        for item in combine:
            if sum(item) == target:
                r = []
                for i in range(1, self.size + 1):
                    if i in item:
                        r.append(1)
                    else:
                        r.append(0)
                res.append(r)
        return res

    def genNextState(self):
        res = []
        moveList = self.__genPossibleMoves(State.sumOfRow[self.currentIndex + 1])
        for move in moveList:
            newboard = self.board.copy()
            newboard[self.currentIndex + 1] = move
            res.append(State(newboard, self.currentIndex + 1))
        return res


class BestFirstSearch:
    def __init__(self, size, sumOfRow, sumOfCol):
        self.size = size
        self.board = self.__initBoard()
        self.sumOfRow = sumOfRow
        self.sumOfCol = sumOfCol

    def __initBoard(self):
        return [[0 for j in range(self.size)] for i in range(self.size)]

    def solve(self):
        numState = 0
        initState = State(self.board, -1, self.size, self.sumOfRow, self.sumOfCol)
        stateList = PriorityQueue()
        stateList.put(initState)
        while True:
            numState += 1
            if stateList.empty():
                return False, numState
            state = stateList.get()
            if state.isGoal():
                self.board = state.board
                return True, numState
            nextState = state.genNextState()
            for item in nextState:
                if item.isValid():
                    stateList.put(item)
