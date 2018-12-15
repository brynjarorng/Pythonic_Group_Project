import pygame as pg
from logic import *
from AI import *
from sprites.Player import Player
from sprites.Ghost import Ghost 
import whackmanMenu as wm

FPS = 100
SCALE = 2

def readBoard():
    with open('whackman/maze.txt') as f:
        for i, l in enumerate(f):
            MAZE.append([])
            for c in l.strip():
                MAZE[i].append(c)

# The board
MAZE = []
PLAYERS = ['P', 'p']
GHOSTS = ['A', 'B', 'C', 'D']
readBoard()

# Gameboard attributes
TILE = 10 * SCALE
WINDOWWIDTH = len(MAZE[0]) * TILE
WINDOWHEIGHT = len(MAZE) * TILE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Object attributes
COINRADIUS = int(TILE/10)
BIGCOINRADIUS = int(TILE/3)
ENTITYRADIUS = int(TILE/2)-1

# Colors
BLACK = (0,0,0)
GREY = (125, 125, 125)
GOLD = (255,223,0)
BLUE = (0, 25, 175)
ENTITYCOLORS = {
    "P": (255, 255, 255),
    "p": (150, 150, 150),

    "A": (255, 255, 0),
    "B": (200, 50, 20),
    "C": (0, 255, 0),
    "D": (0, 25, 175)
}

def checkIfDead(player, ghosts, MAZE):
    for ghost in ghosts:
        if player.pos == ghost.pos:
            # dec. live counter and hide the player
            player.lives -= 1
            player.diedThisGame = True
            MAZE[player.pos[1]][player.pos[0]] = '_'
            player.pos = (-1, -1)
            return

def drawGame(SCREEN, TILE, MAZE):
    pg.draw.rect(SCREEN, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
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
            
            elif c.isalpha() and c in ENTITYCOLORS:
                if c.lower() == 'p':
                    pg.draw.circle(SCREEN, ENTITYCOLORS[c], (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                    for i, player in enumerate(PLAYERS):
                        if player.char == c:
                            PLAYERS[i].pos = (x, y)
                else:
                    pg.draw.rect(SCREEN, ENTITYCOLORS[c], (x * TILE, y * TILE, TILE-1, TILE-1))
                    ENTITYCOLORS[c]
                    for i, ghost in enumerate(GHOSTS):
                        if ghost.char == c:
                            #print(c, ghost.char)
                            GHOSTS[i].pos = (x, y)

            
            # Player 1
            elif c == 'P':
                pg.draw.circle(SCREEN, WHITE, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYERS[0].pos = (x, y)
            # Player 2
            elif c == 'p':
                pg.draw.circle(SCREEN, SILVER, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYERS[1].pos = (x, y)
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
    global PLAYERS, GHOSTS

    # Initializing entities
    PLAYERS = [Player('', char, '_', (0, 0), (0, 0), 0, 10) for char in PLAYERS]
    GHOSTS = [Ghost('', char, '_', (0, 0), (0, 0), 0, 10, 'R') for char in GHOSTS]
    for i, player in enumerate(PLAYERS):
        GHOSTS[i].chasing = player.char

    # Used to regulate entity speeds
    maxSpeed = 100
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    while 1:
        drawGame(SCREEN, TILE, MAZE)
        
        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            wm.menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
            pg.time.wait(250)

        # Set next direction on key press
        if keyinput[pg.K_LEFT]:
            PLAYERS[0].nextDir = LEFT
        elif keyinput[pg.K_RIGHT]:
            PLAYERS[0].nextDir = RIGHT
        elif keyinput[pg.K_UP]:
            PLAYERS[0].nextDir = UP
        elif keyinput[pg.K_DOWN]:
            PLAYERS[0].nextDir = DOWN

        if keyinput[pg.K_a]:
            PLAYERS[1].nextDir = LEFT
        elif keyinput[pg.K_d]:
            PLAYERS[1].nextDir = RIGHT
        elif keyinput[pg.K_w]:
            PLAYERS[1].nextDir = UP
        elif keyinput[pg.K_s]:
            PLAYERS[1].nextDir = DOWN

        # Check if next direction is valid
        for player in PLAYERS:
            if validateNextDir(MAZE, player):
                player.moveDir = player.nextDir
        
        # move the players
        for player in PLAYERS:
            if player.moveCount > maxSpeed:
                player = movePlayer(MAZE, player)
                player = updateScore(player)
                player.moveCount = 0    #Reset moveCounter(speed control)
            else:
                player.moveCount += player.speed

        # move the ghosts
        for ghost in GHOSTS:
            if ghost.moveCount > maxSpeed:
                if not ghost.path:
                    if ghost.chasing == 'R':
                        ghost.path = randomPath(ghost.pos, MAZE, 10)
                    else:
                        playerToChase = next(x for x in PLAYERS if x.char == ghost.chasing)
                        ghost.path = distShortPath(ghost.pos, playerToChase.pos, MAZE, 10)
                        
                nextPos = ghost.path.pop()        
                ghost.moveDir = (nextPos[0] - ghost.pos[0], nextPos[1] - ghost.pos[1])
                ghost = moveGhost(MAZE, ghost)
                ghost.moveCount = 0
            else:
                ghost.moveCount += ghost.speed
        
        # check if player should be dead
        for player in PLAYERS:
            if not player.diedThisGame:
                checkIfDead(player, GHOSTS, MAZE)
        
        pg.display.flip()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
