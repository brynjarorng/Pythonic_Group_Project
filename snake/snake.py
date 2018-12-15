import pygame as pg
import random
from pathlib import Path
import math
import sys

pg.mixer.pre_init(44100, 16, 2, 4096)
pg.init()
pg.mixer.init()

# load audio
audioPath = Path(sys.argv[0]).parent / "snake" / 'crunch.wav'
eatSound = pg.mixer.Sound(str(audioPath))

# run variable
run = True

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
    run = True
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
            run = False
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

def menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS):
    FPSCLOCK = pg.time.Clock()
    openMenu = True

    # 0 - Continue
    # 1 - Exit
    menuState = 0

    # -1 - Do nothing
    # 0 - go down
    # 1 - go up
    # 2 - select
    nextMenuState = 0
    
    # main menu background positioning
    rec = pg.Rect(0, 0, WINDOWWIDTH * (2 / 3), WINDOWHEIGHT * (2 / 3))
    rec.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    # wait here in order to not instantly exit the menu
    pg.time.wait(250)
    pg.event.clear()
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
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) - 50))
        elif menuState == 1:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 50))
        pg.gfxdraw.box(SCREEN, selectBar, (100,0,0,127))

        # main menu options text
        continueTextSurf, continueText = text_objects("CONTINUE", largeText)
        continueText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) - 50))

        quitTextSurf, quitText = text_objects("EXIT TO MENU", largeText)
        quitText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 50))

        # blit text to surface
        SCREEN.blit(continueTextSurf, continueText)
        SCREEN.blit(quitTextSurf, quitText)
        
        # the menu selection logic
        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()
            
            elif ev.type == pg.locals.KEYDOWN:
                if ev.key == pg.K_DOWN and ev.type == pg.KEYDOWN:
                    menuState += 1
                    if menuState == 2:
                        menuState = 0
                elif ev.key == pg.K_UP and ev.type == pg.KEYDOWN:
                    menuState -= 1
                    if menuState == -1:
                        menuState = 1
                elif ev.key == pg.K_RETURN and ev.type == pg.KEYDOWN:
                    if menuState == 0:
                        return True
                    elif menuState == 1:
                        return False
                elif ev.key == pg.K_ESCAPE and ev.type == pg.KEYDOWN:
                    return True
        
        pg.display.flip()

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

# MOVE TO SEPERATE FILE?
def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

# Initial apple
placeApple()

def start():
    # game code
    global run
    while run:
        # limit runtime speed to 30 frames/second
        clock.tick(FPS)
        pg.event.pump()

        # input listener
        keyinput = pg.key.get_pressed()

        movePlayer(keyinput)        
        detectApple()
        drawGame()
        if keyinput[pg.K_ESCAPE]:
            run = menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)

    # exit out of game
    return False