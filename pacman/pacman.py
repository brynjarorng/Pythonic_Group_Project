import pygame as pg

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
    backgroundColor = (0, 0, 0)
    background = pg.Surface(screen.get_size())
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
                pg.draw.rect(screen, (0, 0, 0), (x * squares, y * squares, squares, squares))
            # nothing
            elif c == 'N':
                pg.draw.rect(screen, (255, 255, 255), (x * squares, y * squares, squares, squares))
            # super food
            elif c == 'Q':
                pg.draw.rect(screen, (255, 255, 0), (x * squares, y * squares, squares/2, squares/2))
    pg.display.flip()

clock = pg.time.Clock()
while 1:
    clock.tick(30)
    pg.event.pump()
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()

    buildBoard()










'''
for l in maze:
    for c in l:
        print(c, end='')
    print()
'''