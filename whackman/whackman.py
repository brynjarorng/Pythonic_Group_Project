import pygame as pg
import logic
from sprites.whackmanChar import WhackmanChar

FPS = 150

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

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BLACK = (0,0,0)
GOLD = (255,223,0)
SILVER = (192, 192, 192)
GREY = (125, 125, 125)
RED = (200, 50, 20)
BLUE = (0, 25, 175)

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE[i] = []
            for c in l.strip():
                MAZE[i].append(c)

def drawBoard():
    global PLAYER1, PLAYER2
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
                PLAYER1.pos = (x, y)
            elif c == 'p':
                pg.draw.circle(SCREEN, SILVER, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), PLAYERSIZE)
                PLAYER2.pos = (x, y)

def main():
    pg.init()
    global SCREEN
    global PLAYER1, PLAYER2

    PLAYER1 = WhackmanChar('', 'P', (0,0), PLAYERSIZE, (10,60))
    PLAYER2 = WhackmanChar('', 'p', (0,0), PLAYERSIZE, (10,60))

    # slow down the move speed
    moveCounter = 0
    moveCounterMax = 10
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    readBoard()

    while 1:
        drawBoard()
        
        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            quit()
            sys.exit()

        # Set next direction on key press
        if keyinput[pg.K_LEFT]:
            PLAYER1.nextDir = LEFT
        elif keyinput[pg.K_RIGHT]:
            PLAYER1.nextDir = RIGHT
        elif keyinput[pg.K_UP]:
            PLAYER1.nextDir = UP
        elif keyinput[pg.K_DOWN]:
            PLAYER1.nextDir = DOWN

        if keyinput[pg.K_a]:
            PLAYER2.nextDir = LEFT
        elif keyinput[pg.K_d]:
            PLAYER2.nextDir = RIGHT
        elif keyinput[pg.K_w]:
            PLAYER2.nextDir = UP
        elif keyinput[pg.K_s]:
            PLAYER2.nextDir = DOWN

        #Check if next direction is into wall
        if logic.validateMove(MAZE, PLAYER1):
            PLAYER1.moveDir = PLAYER1.nextDir

        if logic.validateMove(MAZE, PLAYER2):
            PLAYER2.moveDir = PLAYER2.nextDir
        
        # Move the character
        if moveCounter == 0:
            PLAYER1.pos = logic.makeMove(MAZE, PLAYER1)
            PLAYER2.pos = logic.makeMove(MAZE, PLAYER2)
        moveCounter += 1
        
        #Reset moveCounter(speed control)
        if moveCounter > moveCounterMax:
            moveCounter = 0

        pg.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()