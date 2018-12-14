import pygame as pg
import logic
import AI
from graphAPI import GraphAPI
from sprites.Player import Player
from sprites.Ghost import Ghost 

FPS = 1000

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE.append([])
            for c in l.strip():
                MAZE[i].append(c)

# The board
MAZE = []
readBoard()

# Gameboard attributes
SCALE = 2
TILE = 10 * SCALE
WINDOWWIDTH = len(MAZE[0]) * TILE
WINDOWHEIGHT = len(MAZE) * TILE

# Object attributes
COINRADIUS = int(TILE/10)
BIGCOINRADIUS = int(TILE/3)
ENTITYRADIUS = int(TILE/2)-2

# Sprite attributes
POS = (1, 1)
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BLACK = (0,0,0)
GREY = (125, 125, 125)
GOLD = (255,223,0)

WHITE = (255, 255, 255)
SILVER = (150, 150, 150)

YELLOW = (255, 255, 0)
RED = (200, 50, 20)
GREEN = (0, 255, 0)
BLUE = (0, 25, 175)


'''
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
                if logic.validateMove(MAZE, (x,y)
                
                , (0, 1)):
                    connectedPoints.append((x, y + 1))
                # below
                if logic.validateMove(MAZE, (x,y), (1, 0)):
                    connectedPoints.append((x + 1, y))
                # left
                if logic.validateMove(MAZE, (x,y), (0, -1)):
                    connectedPoints.append((x, y - 1))
                mazeGraph.add((x,y), connectedPoints)
'''

def drawGame():
    for y, l in enumerate(MAZE):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1), 4)
            # Empty tile
            elif c == '_' or c == '-':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
            # Coin
            elif c == '0':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRADIUS)
            # Super food
            elif c == '1':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRADIUS)
            # Player 1
            elif c == 'P':
                pg.draw.circle(SCREEN, WHITE, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYER1.pos = (x, y)
            # Player 2
            elif c == 'p':
                pg.draw.circle(SCREEN, SILVER, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYER2.pos = (x, y)
            # Ghost A
            elif c == 'A':
                pg.draw.rect(SCREEN, YELLOW, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTA.pos = (x, y)
            # Ghost B
            elif c == 'B':
                pg.draw.rect(SCREEN, RED, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTB.pos = (x, y)
            # Ghost C
            elif c == 'C':
                pg.draw.rect(SCREEN, GREEN, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTC.pos = (x, y)
            # Ghost D
            elif c == 'D':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTD.pos = (x, y)

def main():
    pg.init()
    global SCREEN
    global PLAYER1, PLAYER2
    global GHOSTA, GHOSTB, GHOSTC, GHOSTD

    # Initializing entities
    PLAYER1 = Player('', 'P', '_', (0, 0), (0, 0), 20, 0)
    PLAYER2 = Player('', 'p', '_', (0, 0), (0, 0), 20, 0)
    GHOSTA = Ghost('', 'A', '_', (0, 0), (0, 0), 10, 0)
    GHOSTB = Ghost('', 'B', '_', (0, 0), (0, 0), 10, 0)
    GHOSTC = Ghost('', 'C', '_', (0, 0), (0, 0), 10, 0)
    GHOSTD = Ghost('', 'D', '_', (0, 0), (0, 0), 10, 0)

    # Used to regulate entity speeds
    maxSpeed = 100
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    while 1:
        drawGame()
        
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

        # Check if next direction is valid
        for player in [PLAYER1, PLAYER2]:
            if logic.validateNextDir(MAZE, player):
                player.moveDir = player.nextDir
        
        # Move the character and iterate their movement counters
        for player in [PLAYER1, PLAYER2]:
            if player.moveCount > maxSpeed:
                player = logic.movePlayer(MAZE, player)
                player = logic.updateScore(player)
                player.moveCount = 0    #Reset moveCounter(speed control)
            else:
                player.moveCount += player.speed

        for i, ghost in enumerate([GHOSTA, GHOSTB, GHOSTC, GHOSTD]):
            if ghost.moveCount > maxSpeed:
                if not ghost.path:
                    if i < 2:
                        ghost.path = AI.randomPath(ghost.pos, MAZE, 10)
                    elif i is 2:
                        ghost.path = AI.distShortPath(ghost.pos, PLAYER1.pos, MAZE, 10)
                    elif i is 3:
                        ghost.path = AI.distShortPath(ghost.pos, PLAYER2.pos, MAZE, 10)
                nextPos = ghost.path.pop()
                ghost.moveDir = (nextPos[0] - ghost.pos[0], nextPos[1] - ghost.pos[1])
                ghost = logic.moveGhost(MAZE, ghost)
                ghost.moveCount = 0
            else:
                ghost.moveCount += ghost.speed

        '''
        # TEST: Move the 'ghost'    
        if moveCounterGHOST == 0:
            if len(ghostMoves) == 0:
                ghostMoves = AI.randomPath(ghost, MAZE, 50)
            currMove = ghostMoves.pop()
            ghost = logic.makeMoveGHOST(MAZE, ghost, (currMove[0]-ghost[0], currMove[1]-ghost[1]))
        moveCounterGHOST += 1
        '''

        pg.display.flip()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()


#readBoard()
#print(AI.randomPath((1,29), MAZE, 10))
