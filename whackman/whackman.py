import pygame as pg
from whackman.logic import *
from whackman.AI import *
from whackman.data.entities.Player import Player
from whackman.data.entities.Ghost import Ghost 
import whackman.whackmanMenu as wm
import os, sys
from pathlib import Path

FPS = 100
SCALE = 2

# get path of file and use that as the base path
mazePath = Path(sys.argv[0]).parent / "whackman" / 'maze.txt'

def readBoard():
    with open(mazePath) as f:
        for i, l in enumerate(f):
            MAZE.append([])
            for c in l.strip():
                MAZE[i].append(c)

# The board
MAZE = []
PLAYERS = ['P', 'p']
GHOSTS = ['A', 'B', 'C', 'D']
GHOSTSTART = [(9,12), (19,12), (9, 18), (19,18)]
readBoard()

# Gameboard attributes
BOTTOMOFFSET = 60
TILE = 12 * SCALE
WINDOWWIDTH = len(MAZE[0]) * TILE
WINDOWHEIGHT = len(MAZE) * TILE + BOTTOMOFFSET

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
    "1": (255, 255, 255),
    "2": (150, 150, 150),

    "A": (255, 255, 0),
    "B": (200, 50, 20),
    "C": (0, 255, 0),
    "D": (175, 0, 175)
}

def drawBoard(SCREEN, TILE, MAZE):
    pg.draw.rect(SCREEN, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
    for y, l in enumerate(MAZE):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1), 4)
            # Coin
            elif c == '0':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRADIUS)
            # Super food
            elif c == '1':
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRADIUS)
            
def drawEntities(SCREEN, TILE, MAZE):
    for player in PLAYERS:
        if not player.diedThisGame:
            if player.nextDir[0] == 1:
                SCREEN.blit(player.img, (int(player.pos[0] * TILE), int(player.pos[1] * TILE)))
            else:
                SCREEN.blit(pg.transform.flip(player.img, True, False), (int(player.pos[0] * TILE), int(player.pos[1] * TILE)))
    for ghost in GHOSTS:
        SCREEN.blit(ghost.img, (int(ghost.pos[0] * TILE), int(ghost.pos[1] * TILE)))

def play():
    pg.init()
    global PLAYERS, GHOSTS

    # get image links
    basePath = Path(sys.argv[0]).parent
    ghostArr = [basePath / "whackman" / "data" / "sprites" / "ghost1.png",
    basePath / "whackman" / "data" / "sprites" / "ghost2.png",
    basePath / "whackman" / "data" / "sprites" / "ghost3.png",
    basePath / "whackman" / "data" / "sprites" / "ghost4.png",
    basePath / "whackman" / "data" / "sprites" / "p1.png"]

    # Initializing entities
    PLAYERS = [Player(ghostArr[4], '1', 'P', (15, 23), (0, 0), 0, 10),
               Player(ghostArr[4], '2', 'P', (13, 23), (0, 0), 0, 10)]
    GHOSTS = [Ghost(ghostArr[i], char, 'G', GHOSTSTART[i], (0, 0), 0, 10, 'R') for i, char in enumerate(GHOSTS)]
    for i, player in enumerate(PLAYERS):
        GHOSTS[i].chasing = player

    # Used to regulate entity speeds
    maxSpeed = 100
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    playGame = True
    while playGame:
        drawBoard(SCREEN, TILE, MAZE)
        drawEntities(SCREEN, TILE, MAZE)
        wm.drawScore(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, BOTTOMOFFSET, PLAYERS)

        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            playGame = wm.menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
            pg.time.wait(400)

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

        for entity in PLAYERS + GHOSTS:
            # Validate next direction for player
            if entity.eType == 'P' and validateNextDir(MAZE, entity):
                entity.moveDir = entity.nextDir
            # Get path from AI for ghost
            elif entity.eType == 'G' and not entity.path:
                if entity.chasing == 'R' or entity.chasing.diedThisGame:
                    entity.path = randomPath(entity.pos, MAZE, 10)
                else:
                    entity.path =  distShortPath(entity.pos, entity.chasing.pos, MAZE, 10)
            #Move entities
            if entity.moveCount > maxSpeed:
                moveEntity(MAZE, entity)
                if entity.eType == 'P':
                    checkIfDead(MAZE, entity, GHOSTS)
                else:
                    checkIfDead(MAZE, entity, PLAYERS)
            else:
                entity.moveCount += entity.speed

        pg.display.flip()
        FPSCLOCK.tick(FPS)