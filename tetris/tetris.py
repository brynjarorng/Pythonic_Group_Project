import pygame as pg

# init base variables
BOARDSIZE = (10, 24)
BOARD = [[0] * BOARDSIZE[1]] * BOARDSIZE[0]
SCALE = 5
TILE = 10 * SCALE
WINDOWSIZE = (BOARDSIZE[0] * TILE, BOARDSIZE[1] * TILE)
FPS = 30
FPSCLOCK = pg.time.Clock()

# init drawing surface
SCREEN = pg.display.set_mode((WINDOWSIZE[0], WINDOWSIZE[1]))


# tetris blocks
I = ['X', 'X', 'X', 'X']
J = [['X', 'X', 'X', None],
    [None, None, None, 'X']]
L = [['X', 'X', 'X', None],
    ['X', None, None, None]]
O = [['X', 'X', None, None],
    ['X', 'X', None, None]]
S = [[None, 'X', 'X', None],
    ['X', 'X', None, None]]
T = [['X', 'X', 'X', None],
    [None, 'X', None, None]]
Z = [['X', 'X', None, None],
    [None, 'X', 'X', None]]
BLOCKS = [I, J, L, O, S, T, Z]

while 1:
    pg.event.pump()
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE]:
        quit()
        sys.exit()
    
    FPSCLOCK.tick(FPS)
    pg.display.flip()