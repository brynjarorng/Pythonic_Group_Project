import pygame as pg
import random
from pathlib import Path
import math

pg.mixer.pre_init(44100, 16, 2, 4096)
pg.init()
pg.mixer.init()

# load audio
p = Path('./')
p = p / 'snake'
p = p / 'crunch.wav'
eatSound = pg.mixer.Sound(str(p.absolute()))

# run variable
run = True

# global variables so that the game does not need to look for the apple
appleX = -1
appleY = -1

# game board size
width = 800
height = 800
SCALE = 10

# init snake
x = int(width / 2)
y = int(height / 2)
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
screen = pg.display.set_mode((width, height))
backgroundColor = (0, 0, 0)
background = pg.Surface(screen.get_size())
background.fill(backgroundColor)

screen.blit(background, (0, 0))
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
        selectBar.center = ((height/2),(width/2))

        pg.gfxdraw.box(screen, selectBar, (100, 0, 0, 255))

        # menu text elements
        startSurf, startText = text_objects("press space to start", largeText)
        startText.center = ((height/2),(width/2))
        
        # add elements to drawing surface
        screen.blit(startSurf, startText)
        pg.display.flip()
        pg.event.pump()
        clock.tick(30)

        if keyinput[pg.K_SPACE]:
            resetGame()
            startMain = start()

def placeApple():
    global appleX
    global appleY
    col = math.floor(width / SCALE)
    row = math.floor(height / SCALE)
    appleX = random.randint(1, col - SCALE) * SCALE
    appleY = random.randint(1, row - SCALE) * SCALE

def drawGame():
    global x
    global y
    global snakeTail

    pg.display.flip()
    screen.blit(background, (0,0))

    # apple
    pg.draw.rect(screen, appleColor, (appleY,appleX,unitSize,unitSize))

    # snake
    pg.draw.rect(screen, snakeColor, (x,y,unitSize,unitSize))

    # tail
    for ind in range(len(snakeTail)):
        pg.draw.rect(screen, snakeColor, (snakeTail[ind][0], snakeTail[ind][1], unitSize, unitSize))

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
    if x <= 0 or x >= width or y <= 0 or y >= height:
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
    x = int(width / 2)
    y = int(height / 2)
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
        selectBar.center = ((height/2),(width/2))

        pg.gfxdraw.box(screen, selectBar, (100, 0, 0, 255))

        # menu text elements
        scoreTextSurf, scoreText = text_objects("score: " + str(len(snakeTail)), largeText)
        playAgainSurf, playAgainText = text_objects("play again? (Y/N)", largeText)
        scoreText.center = ((height/2),(width/2) - 50)
        playAgainText.center = ((height/2),(width/2) + 50)

        # add elements to drawing surface
        screen.blit(scoreTextSurf, scoreText)
        screen.blit(playAgainSurf, playAgainText)

        clock.tick(30)
        pg.event.pump()
        pg.display.update()

# load the game menu for snake
def getMenu(keyinput):
    if keyinput[pg.K_ESCAPE]:
        global x
        global y
        global run
        tmp = (x, y)
        #x = 10
        #y = 10
        while 1:
            menuState = 0
            keyinput = pg.key.get_pressed()
            # quit the game 'ESC'
            clock.tick(30)
            pg.event.pump()
            menuState = drawMenu(keyinput)
            if keyinput[pg.K_y]:
                run = False
                return
            elif keyinput[pg.K_n]:
                x,y = tmp
                return

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

def drawMenu(keyinput):
    # bar for the text
    largeText = pg.font.Font('freesansbold.ttf', 80)
    selectBar = pg.Rect(0, 0, 800, 250)
    selectBar.center = ((height/2),(width/2))

    pg.gfxdraw.box(screen, selectBar, (100, 0, 0, 255))

    # menu text elements
    quitTextSurf, quitText = text_objects("want to quit? (Y/N)", largeText)
    quitText.center = ((height/2),(width/2))

    # add elements to drawing surface
    screen.blit(quitTextSurf, quitText)
    pg.display.update()

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
        clock.tick(30)
        pg.event.pump()

        # input listener
        keyinput = pg.key.get_pressed()

        movePlayer(keyinput)        
        detectApple()
        getMenu(keyinput)
        drawGame()

    # exit out of game
    return False