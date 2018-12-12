import pygame as pg
#from whackmanPlayer import whackMan


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

# Sprite attributes
POS = (0, 0)

# Colors
BLACK = (0,0,0)
GOLD = (255,223,0)
GREY = (125, 125, 125)
RED = (200, 50, 20)

#z = whackMan(WINDOWWIDTH/2, WINDOWWIDTH*2/3 + 85, 10)
dire = 'R'



def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE[i] = []
            for c in l.strip():
                MAZE[i].append(c)

def drawBoard():
    global POS
    for y, l in enumerate(MAZE):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, GREY, (x * TILE, y * TILE, TILE, TILE), 5)
            # Coin
            elif c == 'O':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRAD)
            # Ghost spawn
            elif c == 'S':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE, TILE))
            # Empty tile
            elif c == 'N':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE, TILE))
            # Super food
            elif c == 'Q':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRAD)
            elif c == 'P':
                pg.draw.rect(SCREEN, RED, (x * TILE, y * TILE, TILE, TILE))
                POS = (x, y)

def valDown():
    return MAZE[POS[1] + 1][POS[0]] == 'N' or MAZE[POS[1] + 1][POS[0]] == 'O' or MAZE[POS[1] + 1][POS[0]] == 'G' or MAZE[POS[1] + 1][POS[0]] == 'Q'
def valUp():
    return MAZE[POS[1] - 1][POS[0]] == 'N' or MAZE[POS[1] - 1][POS[0]] == 'O' or MAZE[POS[1] - 1][POS[0]] == 'G' or MAZE[POS[1] - 1][POS[0]] == 'Q'
def valLeft():
    return MAZE[POS[1]][POS[0] + 1] == 'N' or MAZE[POS[1]][POS[0] + 1] == 'O' or MAZE[POS[1]][POS[0] + 1] == 'G' or MAZE[POS[1]][POS[0] + 1] == 'Q'
def valRight():
    return MAZE[POS[1]][POS[0] - 1] == 'N' or MAZE[POS[1]][POS[0] - 1] == 'O' or MAZE[POS[1]][POS[0] - 1] == 'G' or MAZE[POS[1]][POS[0] - 1] == 'Q'

def main():
    pg.init()
    global SCREEN
    global POS

    # 0 - stop  1 - left    2 - down    3 - right   4 - up
    moveDir = 0
    nextMoveDir = 0
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

        # set floating direction
        if keyinput[pg.K_LEFT]:
            nextMoveDir = 1
        elif keyinput[pg.K_RIGHT]:
            nextMoveDir = 3
        elif keyinput[pg.K_UP]:
            nextMoveDir = 4
        elif keyinput[pg.K_DOWN]:
            nextMoveDir = 2

        if moveCounter == 0:
        # set the moveDir to the next if POSsible
            if nextMoveDir == 1:
                if valRight():
                    moveDir = nextMoveDir
            elif nextMoveDir == 3:
                if valLeft():
                    moveDir = nextMoveDir
            elif nextMoveDir == 4:
                if valUp():
                    moveDir = nextMoveDir
            elif nextMoveDir == 2:
                if valDown():
                    moveDir = nextMoveDir
        
        # move player
            if moveDir == 1:
                if valRight():
                    MAZE[POS[1]][POS[0]] = 'N'
                    MAZE[POS[1]][POS[0] - 1] = 'P'
                    moveDir = 1
            elif moveDir == 3:
                if valLeft():
                    MAZE[POS[1]][POS[0]] = 'N'
                    MAZE[POS[1]][POS[0] + 1] = 'P'
                    moveDir = 3
            elif moveDir == 4:
                if valUp():
                    MAZE[POS[1]][POS[0]] = 'N'
                    MAZE[POS[1] - 1][POS[0]] = 'P'
                    moveDir = 4
            elif moveDir == 2:
                if valDown():
                    MAZE[POS[1]][POS[0]] = 'N'
                    MAZE[POS[1] + 1][POS[0]] = 'P'
                    moveDir = 2
            moveCounter += 1
        else:
            moveCounter += 1
            if moveCounter > moveCounterMax:
                moveCounter = 0

        pg.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()