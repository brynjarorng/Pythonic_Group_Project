import pygame as pg
from logic import *
from AI import *
#from draw import drawGame
from sprites.Player import Player
from sprites.Ghost import Ghost 
import pygame.gfxdraw

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
    "D": (175, 0, 175)
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

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 


def menu(SCREEN):
    FPSCLOCK = pg.time.Clock()
    openMenu = True

    # 0 - Continue
    # 1 - restart
    # 2 - Quit
    menuState = 0
    
    # main menu background positioning
    rec = pg.Rect(0, 0, WINDOWWIDTH * (2 / 3), WINDOWHEIGHT * (2 / 3))
    rec.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    # wait here in order to not instantly exit the menu
    pg.time.wait(400)
    while openMenu:
        FPSCLOCK.tick(FPS)
        pg.event.pump()

        # draw main background
        pg.gfxdraw.box(SCREEN, rec, (100, 100, 120, 245))

        # text on screen
        largeText = pg.font.Font('freesansbold.ttf', 60)

        # draw the selection bar
        selectBar = pg.Rect(0, 0, WINDOWWIDTH * (2 / 3), 70)
        if menuState == 0:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3)))
        elif menuState == 1:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 100))
        elif menuState == 2:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 200))
        pg.gfxdraw.box(SCREEN, selectBar, (100, 0, 0, 255))

        # main menu options text
        continueTextSurf, continueText = text_objects("CONTINUE", largeText)
        continueText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3)))

        restartTextSurf, restartText = text_objects("RESTART", largeText)
        restartText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 100))

        quitTextSurf, quitText = text_objects("QUIT", largeText)
        quitText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 200))

        # blit text to surface
        SCREEN.blit(continueTextSurf, continueText)
        SCREEN.blit(restartTextSurf, restartText)
        SCREEN.blit(quitTextSurf, quitText)

        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_ESCAPE]:
            return True
        elif keyinput[pg.K_DOWN]:
            pg.time.wait(150)
            menuState += 1
            if menuState == 3:
                menuState = 2
        elif keyinput[pg.K_UP]:
            pg.time.wait(150)
            menuState -= 1
            if menuState == -1:
                menuState = 0
        elif keyinput[pg.K_RETURN]:
            if menuState == 0:
                return True
            elif menuState == 1:
                # to implement!!!!!
                return
            elif menuState == 2:
                pg.quit()
                quit()

        pg.display.flip()


def main():
    pg.init()
    global PLAYERS, GHOSTS

    # Initializing entities
    PLAYERS = [Player('', char, '_', (0, 0), (0, 0), 0, 10) for char in PLAYERS]
    GHOSTS = [Ghost('', char, '_', (0, 0), (0, 0), 0, 10, 'R') for char in GHOSTS]
    for i, player in enumerate(PLAYERS):
        GHOSTS[i].chasing = player

    # Used to regulate entity speeds
    maxSpeed = 100
    
    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    while 1:
        drawGame(SCREEN, TILE, MAZE)
        
        pg.event.pump()
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_ESCAPE]:
            menu(SCREEN)
            pg.time.wait(250)
            #quit()
            #sys.exit()

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
        
        # move the players
        for player in PLAYERS:
            if validateNextDir(MAZE, player):   # Check if next direction is valid
                player.moveDir = player.nextDir
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
                    if ghost.chasing == 'R' or ghost.chasing.diedThisGame:
                        ghost.path = randomPath(ghost.pos, MAZE, 10)
                    else:
                        playerToChase = next(x for x in PLAYERS if x.char == ghost.chasing.char)
                        ghost.path = distShortPath(ghost.pos, playerToChase.pos, MAZE, 10)
                    
                nextPos = ghost.path.pop()        
                ghost.moveDir = (nextPos[0] - ghost.pos[0], nextPos[1] - ghost.pos[1])
                ghost = moveGhost(MAZE, ghost)
                for player in PLAYERS:
                    if player.char == ghost.beneath:
                        player.diedThisGame = True
                        player.live -= 1
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
