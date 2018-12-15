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

# Get path of file and use that as the base path
def initBoard(maze):
    mazePath = Path(sys.argv[0]).parent / "whackman" / 'maze.txt'
    with open(mazePath) as f:
        for i, l in enumerate(f):
            maze.append([])
            for c in l.strip():
                maze[i].append(c)
# Create players and ghosts
def initEntities(tile):
    players = ['P', 'p']
    ghosts = ['A', 'B', 'C', 'D']
    ghostStart = [(9,12), (19,12), (9, 18), (19,18)]
    # Initializing entities
    players = [Player('', '1', 'P', (15, 23), (0, 0), 0, 10),
               Player('', '2', 'P', (13, 23), (0, 0), 0, 10)]
    ghosts = [Ghost('', char, 'G', ghostStart[i], (0, 0), 0, 4, 'R') for i, char in enumerate(ghosts)]
    for i, player in enumerate(players):
        ghosts[i].chasing = player
    return players, ghosts
# Draw the game board and changes during game
def drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT):
    # Object attributes
    BLACK = (0,0,0)
    GOLD = (255,223,0)
    BLUE = (0, 25, 175)
    COINRADIUS = int(TILE/10)
    BIGCOINRADIUS = int(TILE/3)
    noCoinsLeft = True
    
    pg.draw.rect(SCREEN, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
    for y, l in enumerate(maze):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1), 4)
            # Coin
            elif c == '0':
                noCoinsLeft = False
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRADIUS)
            # Super food
            elif c == '1':
                noCoinsLeft = False
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRADIUS)
    return noCoinsLeft
# Draw players and ghosts
def drawEntities(SCREEN, TILE, players, ghosts):
    ENTITYRADIUS = int(TILE/2)-1
    # Colors
    ENTITYCOLORS = {
        "1": (255, 255, 255),
        "2": (150, 150, 150),

        "A": (255, 255, 0),
        "B": (200, 50, 20),
        "C": (0, 255, 0),
        "D": (175, 0, 175)}

    for player in players:
        if not player.diedThisGame:
            pg.draw.circle(SCREEN, ENTITYCOLORS[player.char], (int((player.pos[0]) * TILE + TILE / 2), int((player.pos[1]) * TILE + TILE / 2)), ENTITYRADIUS)
    for ghost in ghosts:
        pg.draw.rect(SCREEN, ENTITYCOLORS[ghost.char], (int(ghost.pos[0] * TILE), int(ghost.pos[1] * TILE), TILE-1, TILE-1))

def nextLevel(players, ghosts, tile):
    points = [p.points for p in players]
    lives = [p.lives for p in players]
    ghostSpeed = ghosts[0].speed
    players, ghosts = initEntities(tile)
    for i, player in enumerate(players):
        player.points = points[i]
        player.lives = lives[i]
    for ghost in ghosts:
        ghost.speed = ghostSpeed + 2
    return players, ghosts

def play():
    pg.init()

    # The board and entities
    maze = []
    
    initBoard(maze)

    # Gameboard attributes
    BOTTOMOFFSET = 60
    TILE = 10 * SCALE
    WINDOWWIDTH = len(maze[0]) * TILE
    WINDOWHEIGHT = len(maze) * TILE + BOTTOMOFFSET

    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pg.time.Clock()

    players, ghosts = initEntities(TILE)

    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)    
    
    # Used to regulate entity speeds
    maxSpeed = 100
    playGame = True

    while playGame:
        if drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT):
            maze = []
            initBoard(maze)
            players, ghosts = nextLevel(players, ghosts, TILE)
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
        drawEntities(SCREEN, TILE, players, ghosts)
        wm.drawScore(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, BOTTOMOFFSET, players)

        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            playGame = wm.menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
            pg.time.wait(400)

        # Set next direction on key press
        if keyinput[pg.K_LEFT]:
            players[0].nextDir = LEFT
        elif keyinput[pg.K_RIGHT]:
            players[0].nextDir = RIGHT
        elif keyinput[pg.K_UP]:
            players[0].nextDir = UP
        elif keyinput[pg.K_DOWN]:
            players[0].nextDir = DOWN

        if keyinput[pg.K_a]:
            players[1].nextDir = LEFT
        elif keyinput[pg.K_d]:
            players[1].nextDir = RIGHT
        elif keyinput[pg.K_w]:
            players[1].nextDir = UP
        elif keyinput[pg.K_s]:
            players[1].nextDir = DOWN

        for entity in players + ghosts:
            # Validate next direction for player
            if entity.eType == 'P' and validateNextDir(maze, entity):
                entity.moveDir = entity.nextDir
            # Get path from AI for ghost
            elif entity.eType == 'G' and not entity.path:
                if entity.chasing == 'R' or entity.chasing.diedThisGame:
                    entity.path = randomPath(entity.pos, maze, 10)
                else:
                    entity.path =  distShortPath(entity.pos, entity.chasing.pos, maze, 10)
            #Move entities
            if entity.moveCount > maxSpeed:
                moveEntity(maze, entity)
                if entity.eType == 'P':
                    checkIfDead(maze, entity, ghosts)
                else:
                    checkIfDead(maze, entity, players)
            else:
                entity.moveCount += entity.speed

        pg.display.flip()
        FPSCLOCK.tick(FPS)