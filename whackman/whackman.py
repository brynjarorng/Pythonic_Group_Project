import pygame as pg
from whackmanPlayer import whackMan

pg.init()

# load maze into memory
maze = [0] * 31
with open('maze.txt') as f:
    for i,l in enumerate(f):
        tmp = []
        for c in l:
            tmp.append(c)
        maze[i] = tmp[:-1]


# game board init
SCALE = 3
squares = 10 * SCALE
width = 28 * squares
height = 31 * squares
screen = pg.display.set_mode((width, height))

# TMP TEST!
pos = (0, 0)

def buildBoard():
    global screen
    global pos

    # set background color
    backgroundColor = (0, 0, 0)
    background = pg.display.set_mode((height,width))
    background.fill(backgroundColor)
    # colors


    for y,l in enumerate(maze):
        for x,c in enumerate(l):
            # walls
            if c == '|':
                pg.draw.rect(screen, (0, 0, 255), (x * squares, y * squares, squares, squares))
            # food
            elif c == 'O':
                #obj = pg.draw.circle(screen, )
                pg.draw.circle(screen, (255, 255, 0), (int(x * squares + squares / 2), int(y * squares + squares / 2)), int(squares/10) )
            # ghost spawn
            elif c == 'S':
                s = 1
                #pg.draw.rect(screen, (0, 0, 0), (x * squares, y * squares, squares, squares))
            # nothing
            elif c == 'N':
                s=1
                #pg.draw.rect(screen, (255, 255, 255), (x * squares, y * squares, squares, squares))
            # super food
            elif c == 'Q':
                pg.draw.rect(screen, (255, 255, 0), (x * squares, y * squares, squares/2, squares/2))
            elif c == 'P':
                pg.draw.rect(screen, (200, 50, 20), (x * squares, y * squares, squares, squares))
                pos = (x, y)

clock = pg.time.Clock()
z = whackMan(width/2, height*2/3 + 85, 10)
dire = 'R'
# 0 - stop
# 1 - left
# 2 - down
# 3 - right
# 4 - up
moveDir = 0

# slow down the move speed
moveCounter = 0
moveCounterMax = 3

def valDown():
    return maze[pos[1] + 1][pos[0]] == 'N' or maze[pos[1] + 1][pos[0]] == 'O' or maze[pos[1] + 1][pos[0]] == 'G' or maze[pos[1] + 1][pos[0]] == 'Q'
def valUp():
    return maze[pos[1] - 1][pos[0]] == 'N' or maze[pos[1] - 1][pos[0]] == 'O' or maze[pos[1] - 1][pos[0]] == 'G' or maze[pos[1] - 1][pos[0]] == 'Q'
def valLeft():
    return maze[pos[1]][pos[0] + 1] == 'N' or maze[pos[1]][pos[0] + 1] == 'O' or maze[pos[1]][pos[0] + 1] == 'G' or maze[pos[1]][pos[0] + 1] == 'Q'
def valRight():
    return maze[pos[1]][pos[0] - 1] == 'N' or maze[pos[1]][pos[0] - 1] == 'O' or maze[pos[1]][pos[0] - 1] == 'G' or maze[pos[1]][pos[0] - 1] == 'Q'

while 1:
    clock.tick(60)
    pg.event.pump()
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()

    buildBoard()
    #screen.blit(z.img, z.rect)

    # set floating direction
    if keyinput[pg.K_LEFT]:
        if moveDir == 2 or moveDir == 4:
            if not valRight():
                continue
        moveDir = 1
    elif keyinput[pg.K_RIGHT]:
        if moveDir == 2 or moveDir == 4:
            if not valLeft():
                continue
        moveDir = 3
    elif keyinput[pg.K_UP]:
        if moveDir == 1 or moveDir == 3:
            if not valUp():
                continue
        moveDir = 4
    elif keyinput[pg.K_DOWN]:
        if moveDir == 1 or moveDir == 3:
            if not valDown():
                continue
        moveDir = 2
    
    # move player
    if moveCounter == 0:
        if moveDir == 1:
            if valRight():
                maze[pos[1]][pos[0]] = 'N'
                maze[pos[1]][pos[0] - 1] = 'P'
                moveDir = 1
        elif moveDir == 3:
            if valLeft():
                maze[pos[1]][pos[0]] = 'N'
                maze[pos[1]][pos[0] + 1] = 'P'
                moveDir = 3
        elif moveDir == 4:
            if valUp():
                maze[pos[1]][pos[0]] = 'N'
                maze[pos[1] - 1][pos[0]] = 'P'
                moveDir = 4
        elif moveDir == 2:
            if valDown():
                maze[pos[1]][pos[0]] = 'N'
                maze[pos[1] + 1][pos[0]] = 'P'
                moveDir = 2
        moveCounter += 1
    else:
        moveCounter += 1
        if moveCounter > moveCounterMax:
            moveCounter = 0


    '''
    if keyinput[pg.K_LEFT]:
        z.moveL()
        z.update()
        dire = 'L'
    elif keyinput[pg.K_RIGHT]:
        z.moveR()
        z.update()
        dire = 'R' 
    elif keyinput[pg.K_UP]:
        z.moveU()
        z.update()
    elif keyinput[pg.K_DOWN]:
        z.moveD()
        z.update()

    
    if dire == 'L':
        screen.blit(pg.transform.flip(z.img, True, False), z.rect)
    elif dire == 'R':
        screen.blit(z.img, z.rect)
    '''
    pg.display.update()
    










'''
for l in maze:
    for c in l:
        print(c, end='')
    print()
'''