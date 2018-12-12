import pygame as pg
import logic
#from sprites.WhackmanChar import WhackmanChar

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
GREY = (125, 125, 125)
RED = (200, 50, 20)

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE[i] = []
            for c in l.strip():
                MAZE[i].append(c)

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


def main():
    pg.init()
    global SCREEN
    global PLAYER
    global POS

    #PLAYER = WhackmanChar('', 'P', (0,0), PLAYERSIZE, (10,60))
    moveDir = (0, 0)
    nextDir = (0, 0)
    POS = (0, 0)

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
        
        #Reset moveCounter(speed control)
        if moveCounter > moveCounterMax:
            moveCounter = 0

        pg.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()