#from whackman import SCREEN


# Object attributes
COINRADIUS = int(TILE/10)
BIGCOINRADIUS = int(TILE/3)
ENTITYRADIUS = int(TILE/2)-1

# Colors
BLACK = (0,0,0)
GREY = (125, 125, 125)
GOLD = (255,223,0)

WHITE = (255, 255, 255)
SILVER = (150, 150, 150)

YELLOW = (255, 255, 0)
RED = (200, 50, 20)
GREEN = (0, 255, 0)
BLUE = (0, 25, 175)

def drawGame(SCREEN, TILE, MAZE):
    for y, l in enumerate(MAZE):
        for x, c in enumerate(l):
            # Walls
            if c == '|':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1), 4)
            # Empty tile
            elif c == '_' or c == '-':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
            # Coin
            elif c == '0':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), COINRADIUS)
            # Super food
            elif c == '1':
                pg.draw.rect(SCREEN, BLACK, (x * TILE, y * TILE, TILE-1, TILE-1))
                pg.draw.circle(SCREEN, GOLD, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), BIGCOINRADIUS)
            # Player 1
            elif c == 'P':
                pg.draw.circle(SCREEN, WHITE, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYER1.pos = (x, y)
            # Player 2
            elif c == 'p':
                pg.draw.circle(SCREEN, SILVER, (int(x * TILE + TILE / 2), int(y * TILE + TILE / 2)), ENTITYRADIUS)
                PLAYER2.pos = (x, y)
            # Ghost A
            elif c == 'A':
                pg.draw.rect(SCREEN, YELLOW, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTA.pos = (x, y)
            # Ghost B
            elif c == 'B':
                pg.draw.rect(SCREEN, RED, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTB.pos = (x, y)
            # Ghost C
            elif c == 'C':
                pg.draw.rect(SCREEN, GREEN, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTC.pos = (x, y)
            # Ghost D
            elif c == 'D':
                pg.draw.rect(SCREEN, BLUE, (x * TILE, y * TILE, TILE-1, TILE-1))
                GHOSTD.pos = (x, y)