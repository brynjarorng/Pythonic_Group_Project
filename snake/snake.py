import pygame as pg
import random
from pathlib import Path
import math
import sys
import gameMenu as gm
from whackman.whackman import gameOver as gameOverMenu

pg.mixer.pre_init(44100, 16, 2, 4096)
pg.init()
pg.mixer.init()

basePath = Path(sys.argv[0]).parent
fontLoc = basePath / "whackman" / "data" / "fonts" / "minotaur.ttf"

# load audio
audioPath = Path(sys.argv[0]).parent / "snake" / 'crunch.wav'
eatSound = pg.mixer.Sound(str(audioPath))

# global variables so that the game does not need to look for the apple
appleX = -100
appleY = -100

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
    startMain = True
    '''
    # bar for the text
    largeText = pg.font.Font('freesansbold.ttf', 80)
    selectBar = pg.Rect(0, 0, 800, 100)
    selectBar.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2))

    # menu text elements
    startSurf, startText = text_objects("press space to start", largeText)
    startText.center = ((WINDOWHEIGHT/2),(WINDOWWIDTH/2))
    '''
    placeApple()
    while startMain:

        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()

        if countDownGameStart():
            resetGame()
            startMain = start()

def placeApple():
    global appleX, appleY, unitSize
    col = math.floor(WINDOWWIDTH / SCALE)
    row = math.floor(WINDOWHEIGHT / SCALE)
    appleX = random.randint(unitSize, col - SCALE) * SCALE
    appleY = random.randint(unitSize, row - SCALE) * SCALE

def drawGame():
    SCREEN.blit(background, (0,0))

    # apple
    pg.draw.rect(SCREEN, appleColor, (appleY,appleX,unitSize,unitSize))
    # snake
    pg.draw.rect(SCREEN, snakeColor, (x,y,unitSize,unitSize))
    # tail
    for ind in range(len(snakeTail)):
        pg.draw.rect(SCREEN, snakeColor, (snakeTail[ind][0], snakeTail[ind][1], unitSize, unitSize))

    pg.display.flip()

def detectApple():
    if appleX - unitSize/2 <= y and y <= appleX + unitSize/2 and appleY - unitSize/2 <= x and x <= appleY + unitSize/2:
        global snakeTail
        eatSound.play()
        snakeTail.append((x, y))
        placeApple()

def move():
    global x
    global y
    global snakeTail

    # move the snake
    for ind in range(len(snakeTail) - 1, 0, -1):
        snakeTail[ind] = snakeTail[ind - 1]

    if len(snakeTail) >= 1:
        snakeTail[0] = (x, y)

    x += moveX*SCALE
    y += moveY*SCALE
    
    detectCollision()

def detectCollision():
    global x, y, playGame
    if x <= -1 or x >= WINDOWWIDTH-unitSize+1 or y <= -1 or y >= WINDOWHEIGHT-unitSize+1 or (x, y) in snakeTail:
        gameOverMenu(SCREEN, WINDOWWIDTH, WINDOWHEIGHT, len(snakeTail))
        resetGame()

def resetGame():
    global x, y, moveX, moveY, snakeTail
    snakeTail = []
    x = int(WINDOWWIDTH / 2)
    y = int(WINDOWHEIGHT / 2)
    moveX = 1
    moveY = 0

def movePlayer(keyinput):
    global moveX, moveY
    # move the player
    if keyinput[pg.K_LEFT]:
        if moveX != moveSpeed:
            moveX = -moveSpeed
            moveY = 0
    elif keyinput[pg.K_RIGHT]:
        if moveX != -moveSpeed:
            moveX = moveSpeed
            moveY = 0
    elif keyinput[pg.K_UP]:
        if moveY != moveSpeed:
            moveY = -moveSpeed
            moveX = 0
    elif keyinput[pg.K_DOWN]:
        if moveY != -moveSpeed:
            moveY = moveSpeed
            moveX = 0

# MOVE TO SEPERATE FILE?
def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

def start():
    # game code
    global playGame
    playGame = True
    while playGame:
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
                        countDownGameStart()
                    elif ret == 0:
                        return False

        detectApple()
        move()
        drawGame()

        pg.display.update()
        clock.tick(FPS)

    # exit out of game
    return False

# Count after space has been pressed
def countDownGameStart():    
    largeText = pg.font.Font(str(fontLoc), 200)
    smallText = pg.font.Font(str(fontLoc), 60)

    pressSpaceSurf, pressSpaceText = text_objects('PRESS SPACE TO START', smallText)
    pressSpaceText.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)
    
    countSTarr = []
    for x in ['3', '2', '1', 'GO!']:
        countSurf, countText = text_objects(x, largeText)
        countText.center = (WINDOWWIDTH /2, WINDOWHEIGHT / 2)
        countSTarr.append((countSurf, countText))
    
    FPSCLOCK = pg.time.Clock()
    spacePressed = False
    counter = 0
    blinkSpeed = [int(FPS*(1/2)), FPS]
    while True:
        FPSCLOCK.tick(FPS)
        pg.event.pump()

        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()

        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_SPACE]:
            spacePressed = True

        drawGame()
        
        # countdown sequence
        if spacePressed:
            SCREEN.blit(countSTarr[counter][0], countSTarr[counter][1])
            pg.display.flip()
            for i in range(int(FPS * (2 / 3))):
                pg.event.pump()
                FPSCLOCK.tick(FPS)
                continue
            counter += 1
            if counter == 4:
                return True
        else:
            for i, speed in enumerate(blinkSpeed):
                for x in range(speed):
                    if i == 1:
                        SCREEN.blit(pressSpaceSurf, pressSpaceText)
                    pg.display.flip()
                    pg.event.pump()
                    FPSCLOCK.tick(FPS)
                    keyinput = pg.key.get_pressed()
                    if keyinput[pg.K_SPACE]:
                        break