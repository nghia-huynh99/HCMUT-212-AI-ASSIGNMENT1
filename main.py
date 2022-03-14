from itertools import combinations


def initBoard(size):
    return [[0 for j in range(size)] for i in range(size)]


def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print()


def sumIndex(line):
    s = 0
    for i in range(len(line)):
        s += line[i] * (i + 1)
    return s


def extractColumn(matrix, index):
    return [row[index] for row in matrix]


def clear(size):
    return [0 for i in range(size)]


def isSafe(board, colsum):
    for i in range(len(board)):
        if sumIndex(extractColumn(board, i)) > colsum[i]:
            return False
    return True


def genPossibleMoves(rowsize, target):
    index = []
    combine = []
    res = []
    for i in range(1, rowsize + 1):
        index.append(i)
    for num in range(1, rowsize + 1):
        combine += list(combinations(index, num))
    for item in combine:
        if sum(item) == target:
            r = []
            for i in range(1, rowsize + 1):
                if i in item:
                    r.append(1)
                else:
                    r.append(0)
            res.append(r)
    return res


def blindSearch(board, rowsum, colsum, index=0):
    success = False
    if index == len(board):
        return True, board
    else:
        moveList = genPossibleMoves(len(board), rowsum[index])
        for move in moveList:
            board[index] = move
            if isSafe(board, colsum):  # check if new row makes sum of each column exceed the given sum or doesn't
                flag, board = blindSearch(board, rowsum, colsum, index + 1)
                if not flag:
                    board[index] = clear(len(board))
                else:
                    return True, board
            else:
                board[index] = clear(len(board))
        return success, board


if __name__ == "__main__":
    board = initBoard(5)

    # 4 x 4 easy
    # rowsum = [8, 3, 4, 9]
    # colsum = [1, 4, 7, 8]
    # rowsum = [9, 3, 7, 8]
    # colsum = [9, 6, 5, 8]

    # 4 x 4 hard
    # rowsum = [6, 9, 3, 5]
    # colsum = [7, 6, 2, 7]
    # rowsum = [5, 7, 5, 4]
    # colsum = [7, 5, 7, 3]

    # 5 x 5 easy
    # rowsum = [12, 11, 9, 8, 13]
    # colsum = [11, 9, 11, 9, 12]
    # rowsum = [7, 4, 3, 6, 6]
    # colsum = [5, 4, 4, 7, 5]

    # 5 x 5 hard
    # rowsum = [9, 2, 9, 3, 10]
    # colsum = [5, 5, 7, 9, 6]
    rowsum = [9, 7, 6, 14, 11]
    colsum = [8, 14, 12, 5, 12]

    success, board = blindSearch(board, rowsum, colsum)
    print(success)
    printBoard(board)
