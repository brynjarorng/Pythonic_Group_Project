import pygame as pg
import random
import logging
import math

pg.init()

logging.basicConfig(filename='apple_pos.log',level=logging.INFO)

# global variables so that the game does not need to look for the apple
appleX = -1
appleY = -1

# game board size
width = 1000
height = 1000
SCALE = 10

# init snake
x = int(width / 2)
y = int(height / 2)
unitSize = 20
snakeColor = (0,255,0)
snakeTail = []

# base movement
moveSpeed = 1
moveX = 1
moveY = 0

# init apple
appleColor = (255,0,0)

# init game screen
screen = pg.display.set_mode((width, height))
backgroundColor = (0,0,0)
background = pg.Surface(screen.get_size())
background.fill(backgroundColor)


screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()

# game logic functions
def placeApple():
    global appleX
    global appleY
    col = math.floor(width/SCALE)
    row = math.floor(height/SCALE)
    appleX = random.randint(1, col - SCALE) * SCALE
    appleY = random.randint(1, row - SCALE) * SCALE
    # Debug info
    logging.info('\nappleX: ' + str(appleX) + '\nappleY: ' + str(appleY))
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
        #print(snakeTail[ind][0], snakeTail[ind][1])
        pg.draw.rect(screen, snakeColor, (snakeTail[ind][0], snakeTail[ind][1], unitSize, unitSize))
    # move the snake
    if len(snakeTail) >= 1:
        snakeTail[0] = (x, y)
    for ind in range(len(snakeTail) - 1, -1, -1):
        snakeTail[ind] = snakeTail[ind - 1]
    x += moveX*SCALE
    y += moveY*SCALE
    
    detectEdge()
    detectCollision()
    pg.display.update()
def detectApple():
    if appleX - unitSize/2 <= y and y <= appleX + unitSize/2 and appleY - unitSize/2 <= x and x <= appleY + unitSize/2:
        global snakeTail
        snakeTail.append((x,y))
        placeApple()
def detectEdge():
    if x <= 0 or x >= width or y <= 0 or y >= height:
        resetGame()
def detectCollision():
    global x
    global y
    if (x, y) in snakeTail:
        resetGame()
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



# Initial apple
placeApple()

# game code
while 1:
    # limit runtime speed to 60 frames/second
    clock.tick(30)
    pg.event.pump()

    # input listener
    keyinput = pg.key.get_pressed()

    # quit the game 'ESC'
    if keyinput[pg.K_ESCAPE]:
        raise SystemExit

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

    detectApple()
    drawGame()
    
        


'''
pg.init()
# generate font
pg.font.init()
pf = pg.font.SysFont('Comic Sans MS', 30)

# set screen size
width = 640
height = 640
screen = pg.display.set_mode((width, height))
pg.display.set_caption("move with arrow keys (escape key to exit)")

# color (r, g, b) tuple, values 0 to 255
white = (255, 255, 255)
background = pg.Surface(screen.get_size())
background.fill(white)

# initial position of sprite, center of screen
screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()


# moving box
x = height / 2
y = width / 2
moveX = 6
moveY = 0
direction = 'x'
boxSize = 10
moveSpeed = 6

# create the obligatory event loop
while 1:
    # limit runtime speed to 30 frames/second
    clock.tick(60)
    pg.event.pump()
    # a key has been pressed
    keyinput = pg.key.get_pressed()
    # press escape key to quit game
    if keyinput[pg.K_ESCAPE]:
        raise SystemExit
    # optional exit on window corner x click
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    
    if keyinput[pg.K_LEFT]:
        moveX = -moveSpeed
        moveY = 0
        direction = 'x'
    elif keyinput[pg.K_RIGHT]:
        moveX = moveSpeed
        direction = 'x'
        moveY = 0
    elif keyinput[pg.K_UP]:
        moveY = -moveSpeed
        moveX = 0
        direction = 'y'
    elif keyinput[pg.K_DOWN]:
        moveY = moveSpeed
        moveX = 0
        direction = 'y'

    # continuous movement
    if direction == 'x':
        x += moveX
    else:
        y += moveY

    # check if player has lost the game
    # check if touching walls
    if x >= width - boxSize or x < 0 or y > height - boxSize or y < 0:
        break

    pg.display.flip()
    screen.blit(background, (0,0))
    pg.draw.rect(screen, (0,255,0), (x,y,boxSize,boxSize))
    pg.display.update()

screen.blit(background, (0,0))
textsurface = pf.render('Game Over!', True, (0, 0, 0))
screen.blit(textsurface,(0,0))
while 1:
    clock.tick(60)
    pg.event.pump()

    keyinput = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pg.display.update()
'''