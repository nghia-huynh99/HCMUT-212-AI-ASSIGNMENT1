import pygame
import time
import os
from settings import *
from Backtracking import *
from BestFirstSearch import *
from Maps import *
import tracemalloc

assets_path = os.getcwd() + "\\Assets"
os.chdir(assets_path)
leftArrow = pygame.image.load(os.getcwd() + '\\leftArrow.png')
leftArrow = pygame.transform.scale(leftArrow, (50, 50))
rightArrow = pygame.image.load(os.getcwd() + '\\rightArrow.png')
rightArrow = pygame.transform.scale(rightArrow, (50, 50))
upArrow = pygame.image.load(os.getcwd() + '\\upArrow.png')
upArrow = pygame.transform.scale(upArrow, (15, 15))
downArrow = pygame.image.load(os.getcwd() + '\\downArrow.png')
downArrow = pygame.transform.scale(downArrow, (15, 15))
background = pygame.image.load(os.getcwd() + '\\background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Kakurasu Puzzle')
        self.running = True
        self.state = "init"
        self.listAlgorithm = ["Backtracking", "Best First Search"]
        self.algorithmIdx = 0
        self.numOfMap = getNumOfMap()
        self.mapIdx = 0
        self.map = loadMaps(self.mapIdx)
        self.solution = ()

    def run(self):
        while self.running:
            if self.state != "waiting":
                self.window.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.state == "init":
                        if self.mapIdx < self.numOfMap - 1:
                            self.mapIdx += 1
                        else:
                            self.mapIdx = 0
                        self.map = loadMaps(self.mapIdx)
                    if event.key == pygame.K_LEFT and self.state == "init":
                        if self.mapIdx > 0:
                            self.mapIdx -= 1
                        else:
                            self.mapIdx = self.numOfMap - 1
                        self.map = loadMaps(self.mapIdx)
                    if event.key == pygame.K_UP and self.state == "init":
                        if self.algorithmIdx > 0:
                            self.algorithmIdx -= 1
                        else:
                            self.algorithmIdx = len(self.listAlgorithm) - 1
                    if event.key == pygame.K_DOWN and self.state == "init":
                        if self.algorithmIdx < len(self.listAlgorithm) - 1:
                            self.algorithmIdx += 1
                        else:
                            self.algorithmIdx = 0
                    if event.key == pygame.K_RETURN:
                        if self.state == "init":
                            self.state = "execute"
                        if self.state == "done":
                            self.state = "init"
            if self.state == "init":
                self.startScreen()
            if self.state == "execute":
                self.executeScreen()
                pygame.display.update()
                self.state = "waiting"
            if self.state == "waiting":
                self.solution = ()
                self.execute()
                self.state = "done"
            if self.state == "done":
                self.solutionScreen()
            pygame.display.update()
        pygame.quit()

    def execute(self):
        sumOfRow, sumOfCol = self.map
        if self.algorithmIdx == 0:
            game = Backtracking(len(sumOfRow), sumOfRow, sumOfCol)
            tracemalloc.start()
            start = time.time()
            success, stateCount = game.solve()
            end = time.time()
            memoryUse = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            self.solution = (success, end - start, stateCount, memoryUse, game.board)
        else:
            game = BestFirstSearch(len(sumOfRow), sumOfRow, sumOfCol)
            tracemalloc.start()
            start = time.time()
            success, stateCount = game.solve()
            end = time.time()
            memoryUse = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            self.solution = (success, end - start, stateCount, memoryUse, game.board)

    def drawRectangle(self, color, left, top, width, height, filled=False):
        if not filled:
            pygame.draw.rect(self.window, color, (left, top, width, height), 2)
        else:
            pygame.draw.rect(self.window, color, (left, top, width, height))

    def drawLine(self, color, start, end):
        pygame.draw.line(self.window, color, start, end, 2)

    def drawText(self, text, size, color, position, isCenter=True):
        fontSize = pygame.font.Font('gameFont.ttf', size)
        Text = fontSize.render(text, True, color)
        if isCenter:
            Rect = Text.get_rect(center=position)
        else:
            Rect = Text.get_rect(topleft=position)
        self.window.blit(Text, Rect)

    def drawBoard(self, size, pos):
        mapSize = len(self.map[0])
        cellEdge = size / mapSize
        self.drawRectangle(BLACK, pos[0], pos[1], size, size)

        # draw grid
        for i in range(mapSize):
            self.drawLine(BLACK, (pos[0] + i * cellEdge, pos[1]), (pos[0] + i * cellEdge, pos[1] + size))
            self.drawLine(BLACK, (pos[0], pos[1] + i * cellEdge), (pos[0] + size, pos[1] + i * cellEdge))

        # draw index number
        for i in range(mapSize):
            self.drawText(str(i + 1), 20, GREY, (pos[0] - 20, pos[1] + i * cellEdge + cellEdge / 2))
        for i in range(mapSize):
            self.drawText(str(i + 1), 20, GREY, (pos[0] + i * cellEdge + cellEdge / 2, pos[1] - 20))

        # draw target number
        for i in range(mapSize):
            self.drawText(str(self.map[0][i]), int(cellEdge / 1.5), BLACK,
                          (pos[0] + size + 20, pos[1] + i * cellEdge + cellEdge / 2))
        for i in range(mapSize):
            self.drawText(str(self.map[1][i]), int(cellEdge / 1.5), BLACK,
                          (pos[0] + i * cellEdge + cellEdge / 2, pos[1] + size + 20))

    def startScreen(self):
        self.drawText('Kakurasu', 60, BLACK, (300, 50))
        self.drawText('Choose the Map and Algorithm.', 20, BLACK, (300, 90))
        self.drawText('Then press Enter to start.', 20, BLACK, (300, 110))
        self.drawText('Map.' + str(self.mapIdx + 1), 30, BLACK, (300, 150))
        self.window.blit(leftArrow, (80, 320))
        self.window.blit(rightArrow, (470, 320))
        self.drawText('Algorithm', 24, BLACK, (300, 510))
        self.window.blit(upArrow, (370, 500))
        self.window.blit(downArrow, (370, 512))
        self.drawText(str(self.listAlgorithm[self.algorithmIdx]), 28, BLACK, (300, 540))
        self.drawBoard(BOARD_SELECT_SIZE, gridSelectPos)

    def executeScreen(self):
        self.drawText('Kakurasu', 60, BLACK, (300, 50))
        self.drawText('Map is being solved. Please wait.', 20, BLACK, (300, 110))
        self.drawText('Map.' + str(self.mapIdx + 1), 30, BLACK, (300, 150))
        self.drawText('Algorithm', 24, BLACK, (300, 510))
        self.drawText(str(self.listAlgorithm[self.algorithmIdx]), 28, BLACK, (300, 540))
        self.drawBoard(BOARD_SELECT_SIZE, gridSelectPos)

    def solutionScreen(self):
        self.drawText('Kakurasu', 60, BLACK, (300, 50))
        self.drawText('Map.' + str(self.mapIdx + 1) + ' Solution', 28, BLACK, (300, 100))
        self.drawText('Time: ' + str(round(self.solution[1], 5)) + 's', 24, BLACK, (70, 490), isCenter=False)
        self.drawText('States: ' + str(self.solution[2]), 24, BLACK, (70, 520), isCenter=False)
        self.drawText('Memory: ' + str(self.solution[3]) + 'bytes', 24, BLACK, (300, 490), isCenter=False)
        self.drawText(str(self.listAlgorithm[self.algorithmIdx]), 28, BLACK, (300, 460))
        self.drawText('Enter to return.', 20, BLACK, (300, 570))

        board = self.solution[4]
        cellEdge = BOARD_SIZE / len(board)
        self.drawBoard(BOARD_SIZE, gridSoluPos)
        for i in range(len(board)):
            top = gridSoluPos[1] + i * cellEdge + 5
            for j in range(len(board)):
                if board[i][j] == 1:
                    left = gridSoluPos[0] + j * cellEdge + 5
                    self.drawRectangle(BLACK, left, top, cellEdge - 8, cellEdge - 8, filled=True)
