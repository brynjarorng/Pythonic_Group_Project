import pygame as pg
from whackman.logic import *
from whackman.AI import *
from whackman.data.entities.Player import Player
from whackman.data.entities.Ghost import Ghost 
import whackman.whackmanMenu as wm
import gameMenu as gm
import os, sys
from pathlib import Path

FPS = 100

# Get path of file and use that as the base path
def initBoard():
    mazePath = Path(sys.argv[0]).parent / "whackman" / 'maze.txt'
    maze = []
    with open(mazePath) as f:
        for i, l in enumerate(f):
            maze.append([])
            for c in l.strip():
                maze[i].append(c)
    return maze

# Create players and ghosts
def initEntities():
    # get image links
    basePath = Path(sys.argv[0]).parent
    imgArr = [basePath / "whackman" / "data" / "sprites" / "ghost1.png",
    basePath / "whackman" / "data" / "sprites" / "ghost2.png",
    basePath / "whackman" / "data" / "sprites" / "ghost3.png",
    basePath / "whackman" / "data" / "sprites" / "ghost4.png",
    basePath / "whackman" / "data" / "sprites" / "p1.png"]

    players = ['P', 'p']
    ghosts = ['A', 'B', 'C', 'D']
    ghostStart = [(9,12), (19,12), (9, 18), (19,18)]

    # Initializing entities
    players = [Player(imgArr[4], '1', 'P', (15, 23), (0, 0), 0, 10),
               Player(imgArr[4], '2', 'P', (13, 23), (0, 0), 0, 10)]
    ghosts = [Ghost(imgArr[i], char, 'G', ghostStart[i], (0, 0), 0, 4, 'R') for i, char in enumerate(ghosts)]
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
    BIGCOINRADIUS = int(TILE/4)
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
    for player in players:
        if not player.dead:
            if player.nextDir[0] == 1:
                SCREEN.blit(player.img, (int(player.pos[0] * TILE), int(player.pos[1] * TILE)))
            else:
                SCREEN.blit(pg.transform.flip(player.img, True, False), (int(player.pos[0] * TILE), int(player.pos[1] * TILE)))
    for ghost in ghosts:
        SCREEN.blit(ghost.img, (int(ghost.pos[0] * TILE), int(ghost.pos[1] * TILE)))

# Load next level when prev level is won
def nextLevel(players, ghosts, tile):
    points = [p.points for p in players]
    lives = [p.lives for p in players]
    ghostSpeed = ghosts[0].speed
    players, ghosts = initEntities()
    for i, player in enumerate(players):
        player.points = points[i]
        player.lives = lives[i]
    for ghost in ghosts:
        ghost.speed = ghostSpeed + 2
    return players, ghosts

# Respawn when both die
def respawn(players, ghosts):
    playerStart = [(15, 23), (13, 23)] 
    ghostStart = [(9,12), (19,12), (9, 18), (19,18)]
    for i, player in enumerate(players):
        player.pos = playerStart[i]
        player.dead = False
        player.moveDir = (0, 0)
        player.nextDir = (0, 0)
        player.moveCount = 0
    for i, ghost in enumerate(ghosts):
        ghost.pos =  ghostStart[i]
        ghost.path = []
        ghost.moveCount = 0
    return players, ghosts
def countDownGameStart(SCREEN, maze, TILE, FPS, WINDOWWIDTH, WINDOWHEIGHT, BOTTOMOFFSET, players, ghosts):
    basePath = Path(sys.argv[0]).parent
    fontLoc = basePath / "whackman" / "data" / "fonts" / "minotaur.ttf"
    
    largeText = pg.font.Font(str(fontLoc), 200)
    smallText = pg.font.Font(str(fontLoc), 60)

    pressSpaceSurf, pressSpaceText = wm.text_objects('PRESS SPACE TO START', smallText)
    pressSpaceText.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)
    
    count3Surf, count3Text = wm.text_objects('3', largeText)
    count3Text.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)

    count2Surf, count2Text = wm.text_objects('2', largeText)
    count2Text.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)

    count1Surf, count1Text = wm.text_objects('1', largeText)
    count1Text.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)
    
    count0Surf, count0Text = wm.text_objects('GO!', largeText)
    count0Text.center = (WINDOWWIDTH /2 + 20, WINDOWHEIGHT / 2)

    FPSCLOCK = pg.time.Clock()
    
    blink = True
    while True:
        FPSCLOCK.tick(FPS)
        pg.event.pump()

        # blinking space
        # on
        drawEntities(SCREEN, TILE, players, ghosts)
        wm.drawScore(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, BOTTOMOFFSET, players)
        drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
        SCREEN.blit(pressSpaceSurf, pressSpaceText)
        pg.display.flip()
        if blink:
            for i in range(FPS * 2):
                    pg.event.pump()
                    FPSCLOCK.tick(FPS)
                    keyinput = pg.key.get_pressed()
                    if keyinput[pg.K_SPACE]:
                        blink = False
                        break
                    continue
        
        # off
        drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
        pg.display.flip()
        if blink:
            for i in range(int(FPS * (1 / 3))):
                    pg.event.pump()
                    FPSCLOCK.tick(FPS)
                    keyinput = pg.key.get_pressed()
                    if keyinput[pg.K_SPACE]:
                        blink = False
                        break
                    continue

        # countdown sequence
        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_SPACE] or not blink:
            # 3
            #pg.draw.rect(SCREEN, (0,0,0), (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
            SCREEN.blit(count3Surf, count3Text)
            pg.display.flip()
            for i in range(int(FPS * (2 / 3))):
                pg.event.pump()
                FPSCLOCK.tick(FPS)
                continue
            
            # 2
            #pg.draw.rect(SCREEN, (0,0,0), (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
            SCREEN.blit(count2Surf, count2Text)
            pg.display.flip()
            for i in range(int(FPS * (2 / 3))):
                pg.event.pump()
                FPSCLOCK.tick(FPS)
                continue
            
            # 1
            #pg.draw.rect(SCREEN, (0,0,0), (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
            SCREEN.blit(count1Surf, count1Text)
            pg.display.flip()
            for i in range(int(FPS * (2 / 3))):
                pg.event.pump()
                FPSCLOCK.tick(FPS)
                continue
            
            # GO!
            #pg.draw.rect(SCREEN, (0,0,0), (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
            SCREEN.blit(count0Surf, count0Text)
            pg.display.flip()
            for i in range(int(FPS / 2)):
                pg.event.pump()
                FPSCLOCK.tick(FPS)
                continue
            return


# Actual game play
def play():
    pg.init()

    # The board and entities    
    maze = initBoard()

    # Gameboard attributes
    BOTTOMOFFSET = 60
    TILE = 24
    WINDOWWIDTH = len(maze[0]) * TILE
    WINDOWHEIGHT = len(maze) * TILE + BOTTOMOFFSET

    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pg.time.Clock()

    players, ghosts = initEntities()

    countDownGameStart(SCREEN, maze, TILE, FPS, WINDOWWIDTH, WINDOWWIDTH, BOTTOMOFFSET, players, ghosts)

    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)    
    
    # Used to regulate entity speeds
    maxSpeed = 100
    playGame = True

    while playGame:
        if players[0].dead and players[1].dead:
            players, ghosts = respawn(players, ghosts)

        if drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT):
            maze = initBoard()
            players, ghosts = nextLevel(players, ghosts, TILE)
            drawBoard(SCREEN, maze, TILE, WINDOWWIDTH, WINDOWHEIGHT)
        drawEntities(SCREEN, TILE, players, ghosts)
        wm.drawScore(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, BOTTOMOFFSET, players)

        pg.event.pump()
        keyinput = pg.key.get_pressed()

        # Game menu
        if keyinput[pg.K_ESCAPE]:
            ret = gm.menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
            # Restart game
            if ret == 2:
                maze = initBoard(maze)
                players, ghosts = initEntities()
                countDownGameStart(SCREEN, maze, TILE, FPS, WINDOWWIDTH, WINDOWWIDTH, BOTTOMOFFSET, players, ghosts)
            # Quit
            elif ret == 0:
                return False
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
                if entity.chasing == 'R' or entity.chasing.dead:
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