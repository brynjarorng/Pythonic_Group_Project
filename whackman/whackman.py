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
SCALE = 2
squares = 10 * SCALE
width = 28 * squares
height = 31 * squares
screen = pg.display.set_mode((width, height))


def buildBoard():
    global screen

    # set background color
    backgroundColor = (255, 255, 255)
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
                pg.draw.circle(screen, (255, 255, 0), (int(x * squares + squares / 2), int(y * squares + squares / 2)), int(squares/2) )
            # ghost spawn
            elif c == 'S':
                pg.draw.rect(screen, (0, 0, 0), (x * squares, y * squares, squares, squares))
            # nothing
            elif c == 'N':
                pg.draw.rect(screen, (255, 255, 255), (x * squares, y * squares, squares, squares))
            # super food
            elif c == 'Q':
                pg.draw.rect(screen, (255, 255, 0), (x * squares, y * squares, squares/2, squares/2))
    pg.display.flip()

clock = pg.time.Clock()
z = whackMan(220, 250, 5)
dire = 'R'
while 1:
    clock.tick(30)
    pg.event.pump()
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()

    #buildBoard()
    #screen.blit(z.img, z.rect)
    pg.display.flip()


    if keyinput[pg.K_LEFT]:
        z.moveL()
        dire = 'L'
    elif keyinput[pg.K_RIGHT]:
        z.moveR()
        dire = 'R'
    elif keyinput[pg.K_UP]:
        z.moveU()
    elif keyinput[pg.K_DOWN]:
        z.moveD()
    
    backgroundColor = (255, 255, 255)
    background = pg.display.set_mode((height,width))
    background.fill(backgroundColor)

    if dire == 'L':
        screen.blit(pg.transform.flip(z.img, True, False), z.rect)
    elif dire == 'R':
        screen.blit(z.img, z.rect)
    










'''
for l in maze:
    for c in l:
        print(c, end='')
    print()
'''