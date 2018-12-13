import pygame as pg
import logic
import AI
from graphAPI import GraphAPI
#from sprites.WhackmanChar import WhackmanChar

FPS = 600

# The board
MAZE = [0] * 31

# Gameboard attributes
SCALE = 2
TILE = 10 * SCALE
WINDOWWIDTH = 28 * TILE
WINDOWHEIGHT = 31 * TILE

# Object attributes
COINRAD = int(TILE/10)
BIGCOINRAD = COINRAD*3
PLAYERSIZE = int(TILE/2)-2

# Sprite attributes
POS = (1, 1)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BLACK = (0,0,0)
GOLD = (255,223,0)
GREY = (125, 125, 125)
RED = (200, 50, 20)

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE[i] = []
            for c in l.strip():
                MAZE[i].append(c)

mazeGraph = GraphAPI()
def buildGraph(MAZE):
    for y,line in enumerate(MAZE):
        for x,unit in enumerate(line):
            if unit != '|':
                connectedPoints = []
                # above
                if logic.validateMove(MAZE, (x,y), (-1, 0)):
                    connectedPoints.append((x - 1, y))
                # right
                if logic.validateMove(MAZE, (x,y), (0, 1)):
                    connectedPoints.append((x, y + 1))
                # below
                if logic.validateMove(MAZE, (x,y), (1, 0)):
                    connectedPoints.append((x + 1, y))
                # left
                if logic.validateMove(MAZE, (x,y), (0, -1)):
                    connectedPoints.append((x, y - 1))
                mazeGraph.add((x,y), connectedPoints)


def drawBoard():
    global PLAYER
    global POS
    for y, l in enumerate(MAZE):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, GREY, (x * TILE, y * TILE, TILE-1, TILE-1), 4)
            # Coin
            elif c == 'O':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRAD)
            # Ghost spawn
            elif c == 'S':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
            # Empty tile
            elif c == 'N':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
            # Super food
            elif c == 'Q':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRAD)
            elif c == 'P':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), PLAYERSIZE)
                #PLAYER= (x, y)
                POS = (x, y)
            elif c == 'A':
                pg.draw.circle(SCREEN, (0,255,0), (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), PLAYERSIZE)


def main():
    pg.init()
    global SCREEN
    global PLAYER
    global POS
    ghost = (1, 1)
    ghostMoves = []
    #PLAYER = WhackmanChar('', 'P', (0,0), PLAYERSIZE, (10,60))
    moveDir = (0, 0)
    nextDir = (0, 0)
    POS = (0, 0)

    # slow down the move speed
    moveCounter = 0
    moveCounterMax = 10
    moveCounterGHOST = 0
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    readBoard()
    buildGraph(MAZE)

    while 1:
        drawBoard()
        
        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            quit()
            sys.exit()

        # Set next direction on key press
        if keyinput[pg.K_LEFT]:
            nextDir = LEFT
        elif keyinput[pg.K_RIGHT]:
            nextDir = RIGHT
        elif keyinput[pg.K_UP]:
            nextDir = UP
        elif keyinput[pg.K_DOWN]:
            nextDir = DOWN

        #Check if next direction is into wall
        if logic.validateMove(MAZE, POS, nextDir):
            moveDir = nextDir

        # Move the character
        if moveCounter == 0:
            POS = logic.makeMove(MAZE, POS, moveDir)
        moveCounter += 1

        # TEST: Move the 'ghost'    
        if moveCounterGHOST == 0:
            if len(ghostMoves) == 0:
                ghostMoves = AI.randomPath(ghost, MAZE, 50)
            currMove = ghostMoves.pop()
            ghost = logic.makeMoveGHOST(MAZE, ghost, (currMove[0]-ghost[0], currMove[1]-ghost[1]))
        moveCounterGHOST += 1
        
        #Reset moveCounter(speed control)
        if moveCounter > moveCounterMax:
            moveCounter = 0
        
        if moveCounterGHOST > moveCounterMax:
            moveCounterGHOST = 0

        pg.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()


#readBoard()
#print(AI.randomPath((1,29), MAZE, 10))