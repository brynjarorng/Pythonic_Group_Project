import pygame as pg

FPS = 200

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

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GOLD = (212,175,55)
BLUE = (0, 25, 175)
GREY = (125, 125, 125)

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE[i] = []
            for c in l.strip():
                MAZE[i].append(c)

def buildBoard():
    
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

def main():
    pg.init()
    global SCREEN
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    readBoard()
    buildBoard()


    while 1:
        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            quit()
            sys.exit()


        pg.display.update()
    FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()