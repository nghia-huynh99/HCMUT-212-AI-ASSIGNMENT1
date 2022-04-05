from itertools import combinations


class Backtracking:
    def __init__(self, size, sumOfRow, sumOfCol):
        self.size = size
        self.board = self.__initBoard()
        self.sumOfRow = sumOfRow
        self.sumOfCol = sumOfCol

    def __initBoard(self):
        return [[0 for j in range(self.size)] for i in range(self.size)]

    def __sumIndex(self, List):
        s = 0
        for i in range(self.size):
            s += List[i] * (i + 1)
        return s

    def __column(self, index):
        return [row[index] for row in self.board]

    def __isValid(self):
        for i in range(self.size):
            if self.__sumIndex(self.__column(i)) > self.sumOfCol[i]:
                return False
        return True

    def __clear(self, index):
        for i in range(self.size):
            self.board[index][i] = 0

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

    def solve(self, index=0, numState=0):
        if index == self.size:
            return True, numState
        moveList = self.__genPossibleMoves(self.sumOfRow[index])
        for move in moveList:
            self.board[index] = move
            if self.__isValid():
                success, numState = self.solve(index + 1, numState + 1)
                if success:
                    return True, numState
        self.__clear(index)
        return False, numState
