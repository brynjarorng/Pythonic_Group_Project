import pygame as pg

# init base variables
BOARDSIZE = (10, 10) # 10, 24
BOARD = [[0] * BOARDSIZE[0]] * BOARDSIZE[1]
SCALE = 3
TILE = 10 * SCALE
WINDOWSIZE = (BOARDSIZE[0] * TILE, BOARDSIZE[1] * TILE)
FPS = 30
FPSCLOCK = pg.time.Clock()

# init drawing surface
SCREEN = pg.display.set_mode((WINDOWSIZE[0], WINDOWSIZE[1]))

# colors
BLUE = (0, 0, 255)


# tetris blocks
'''
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
'''

'''
BLOCKS = {}
BLOCKS['I'] = ([int("0F00", 16), int("2222", 16), int("00F0", 16), int("4444", 16)], (255, 0, 0))
BLOCKS['J'] = ([int("44C0", 16), int("8E00", 16), int("6440", 16), int("0E20", 16)], (0, 255, 0))
BLOCKS['L'] = ([int("4460", 16), int("0E80", 16), int("C440", 16), int("2E00", 16)], (0, 0, 255))
BLOCKS['O'] = ([int("CC00", 16), int("CC00", 16), int("CC00", 16), int("CC00", 16)], (0, 0, 0))
BLOCKS['S'] = ([int("06C0", 16), int("8C40", 16), int("6C00", 16), int("4620", 16)], (0, 0, 0))
BLOCKS['T'] = ([int("0E40", 16), int("4C40", 16), int("4E00", 16), int("4640", 16)], (0, 0, 0))
BLOCKS['Z'] = ([int("0C60", 16), int("4C80", 16), int("C600", 16), int("2640", 16)], (0, 0, 0))
'''

# all blocks in all rotations
BLOCKS = {}
BLOCKS['I'] = (["0F00", "2222", "00F0", "4444"], (255, 0, 0))
BLOCKS['J'] = (["44C0", "8E00", "6440", "0E20"], (0, 255, 0))
BLOCKS['L'] = (["4460", "0E80", "C440", "2E00"], (0, 0, 255))
BLOCKS['O'] = (["CC00", "CC00", "CC00", "CC00"], (0, 0, 0))
BLOCKS['S'] = (["06C0", "8C40", "6C00", "4620"], (0, 0, 0))
BLOCKS['T'] = (["0E40", "4C40", "4E00", "4640"], (0, 0, 0))
BLOCKS['Z'] = (["0C60", "4C80", "C600", "2640"], (0, 0, 0))


def createBlock(pos, blocks, rot):
    global BOARD
    row = 0
    col = 0
    t = 0
    block = blocks[rot]
    for c in block:
        baseTwo = str(bin(int(c, 16))[2:].zfill(4))
        for n in baseTwo:
            col += 1
            if n == '1':
                t+=1
                print(BOARD[col][row])
                BOARD[col][row] = 'I'
        col = 0
        row += 1
    print(t)



#print(BLOCKS['I'][0])
createBlock((0,0), BLOCKS['I'][0], 0)

for i,y in enumerate(BOARD):
    for j,x in enumerate(BOARD[i]):
        print(x, end="")
    print()

'''
while 1:
    pg.event.pump()
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE]:
        quit()
        sys.exit()
    
    FPSCLOCK.tick(FPS)
    pg.display.flip()
'''