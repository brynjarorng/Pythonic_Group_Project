import pygame as pg
import random
from pathlib import Path
import math
import sys
import gameMenu as gm

pg.mixer.pre_init(44100, 16, 2, 4096)
pg.init()
pg.mixer.init()

# load audio
audioPath = Path(sys.argv[0]).parent / "snake" / 'crunch.wav'
eatSound = pg.mixer.Sound(str(audioPath))

# run variable
playGame = True

# global variables so that the game does not need to look for the apple
appleX = -1
appleY = -1

# game board size
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
FPS = 30
SCALE = 10

# init snake
x = int(WINDOWWIDTH / 2)
y = int(WINDOWHEIGHT / 2)
unitSize = 20
snakeColor = (0, 255, 0)
snakeTail = []

# base movement
moveSpeed = 1
moveX = 1
moveY = 0

# init apple
appleColor = (255, 0, 0)

# init game screen
SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
backgroundColor = (0, 0, 0)
background = pg.Surface(SCREEN.get_size())
background.fill(backgroundColor)

SCREEN.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()

# game logic functions
def play():
    # draw initial game frame and set start variables to true
    drawGame()
    global run
    playGame = True
    startMain = True
    while startMain:
        keyinput = pg.key.get_pressed()

        # bar for the text
        largeText = pg.font.Font('freesansbold.ttf', 80)
        selectBar = pg.Rect(0, 0, 800, 100)
        selectBar.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2))

        pg.gfxdraw.box(SCREEN, selectBar, (100, 0, 0, 255))

        # menu text elements
        startSurf, startText = text_objects("press space to start", largeText)
        startText.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2))
        
        # add elements to drawing surface
        SCREEN.blit(startSurf, startText)
        pg.display.flip()
        pg.event.pump()
        clock.tick(30)

        if keyinput[pg.K_SPACE]:
            resetGame()
            startMain = start()

def placeApple():
    global appleX
    global appleY
    col = math.floor(WINDOWWIDTH / SCALE)
    row = math.floor(WINDOWHEIGHT / SCALE)
    appleX = random.randint(1, col - SCALE) * SCALE
    appleY = random.randint(1, row - SCALE) * SCALE

def drawGame():
    global x
    global y
    global snakeTail

    pg.display.flip()
    SCREEN.blit(background, (0,0))

    # apple
    pg.draw.rect(SCREEN, appleColor, (appleY,appleX,unitSize,unitSize))

    # snake
    pg.draw.rect(SCREEN, snakeColor, (x,y,unitSize,unitSize))

    # tail
    for ind in range(len(snakeTail)):
        pg.draw.rect(SCREEN, snakeColor, (snakeTail[ind][0], snakeTail[ind][1], unitSize, unitSize))

    # move the snake

    for ind in range(len(snakeTail) - 1, 0, -1):
        snakeTail[ind] = snakeTail[ind - 1]

    if len(snakeTail) >= 1:
        snakeTail[0] = (x, y)

    x += moveX*SCALE
    y += moveY*SCALE
    
    detectEdge()
    detectCollision()
    pg.display.flip()

def detectApple():
    if appleX - unitSize/2 <= y and y <= appleX + unitSize/2 and appleY - unitSize/2 <= x and x <= appleY + unitSize/2:
        global snakeTail
        eatSound.play()
        snakeTail.append((x, y))
        placeApple()

def detectEdge():
    if x <= 0 or x >= WINDOWWIDTH or y <= 0 or y >= WINDOWHEIGHT:
        gameOver()

def detectCollision():
    global x
    global y
    if (x, y) in snakeTail:
        gameOver()

def resetGame():
    global x
    global y
    global moveX
    global moveY
    global snakeTail
    snakeTail = []
    x = int(WINDOWWIDTH / 2)
    y = int(WINDOWHEIGHT / 2)
    moveX = 1
    moveY = 0

def gameOver():
    global run
    runLoop = True
    while runLoop:
        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_y]:
            resetGame()
            return
        elif keyinput[pg.K_n]:
            playGame = False
            runLoop = False
            resetGame()

        # bar for the text
        largeText = pg.font.Font('freesansbold.ttf', 80)
        selectBar = pg.Rect(0, 0, 800, 250)
        selectBar.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2))

        pg.gfxdraw.box(SCREEN, selectBar, (100, 0, 0, 255))

        # menu text elements
        scoreTextSurf, scoreText = text_objects("score: " + str(len(snakeTail)), largeText)
        playAgainSurf, playAgainText = text_objects("play again? (Y/N)", largeText)
        scoreText.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2) - 50)
        playAgainText.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2) + 50)

        # add elements to drawing surface
        SCREEN.blit(scoreTextSurf, scoreText)
        SCREEN.blit(playAgainSurf, playAgainText)

        clock.tick(30)
        pg.event.pump()
        pg.display.update()

def movePlayer(keyinput):
    global moveX
    global moveY
    # move the player
    if keyinput[pg.K_LEFT]:
        moveX = -moveSpeed
        moveY = 0
    elif keyinput[pg.K_RIGHT]:
        moveX = moveSpeed
        moveY = 0
    elif keyinput[pg.K_UP]:
        moveY = -moveSpeed
        moveX = 0
    elif keyinput[pg.K_DOWN]:
        moveY = moveSpeed
        moveX = 0

# MOVE TO SEPERATE FILE?
def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

# Initial apple
placeApple()

def start():
    # game code
    global playGame
    while playGame:
        # limit runtime speed to 30 frames/second
        clock.tick(FPS)
        pg.event.pump()

        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()
            
            # 0 - exit
            # 1 - continue
            # 2 - restart
            elif ev.type == pg.locals.KEYDOWN:
                # input listener
                keyinput = pg.key.get_pressed()

                movePlayer(keyinput)        
                if keyinput[pg.K_ESCAPE]:
                    ret = gm.menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
                    if ret == 2:
                        resetGame()
                    elif ret == 0:
                        return False
        detectApple()
        drawGame()

    # exit out of game
    return False