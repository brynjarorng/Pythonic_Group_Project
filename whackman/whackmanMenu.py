import pygame as pg
import pygame.gfxdraw
from pathlib import Path
import sys

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

def drawScore(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, BOTTOMOFFSET, PLAYERS):
    # find the base path of the project and execute from there
    basePath = Path(sys.argv[0]).parent
    fontLoc = basePath / "whackman" / "data" / "fonts" / "minotaur.ttf"
    heartLoc = basePath / "whackman" / "data" / "sprites" / "heart.png"

    largeText = pg.font.Font(str(fontLoc), 35)
    heart = pg.image.load(str(heartLoc))

    # center division line
    devLine = pg.Rect(0, 0, 3, BOTTOMOFFSET - 1)
    devLine.center = (WINDOWWIDTH / 2, WINDOWHEIGHT - BOTTOMOFFSET / 2 + 1)
    pg.gfxdraw.box(SCREEN, devLine, (255, 255, 255, 245))

    # player 1 - left
    # score
    playerOneScoreSurf, playerOneScoreText = text_objects('P1: ' + str(PLAYERS[0].points), largeText)
    playerOneScoreText = (10, (WINDOWHEIGHT - BOTTOMOFFSET + 5))

    # lives
    baseHeartPos = 10
    for live in range(PLAYERS[0].lives):
        SCREEN.blit(heart, (baseHeartPos, WINDOWHEIGHT - BOTTOMOFFSET / 2 + 10))
        baseHeartPos += 15

    # player 2 - right
    # score
    playerTwoScoreSurf, playerTwoScoreText = text_objects('P2: ' + str(PLAYERS[1].points), largeText)
    playerTwoScoreText = (WINDOWWIDTH / 2 + 10, (WINDOWHEIGHT - BOTTOMOFFSET + 5))

    # lives
    baseHeartPos = WINDOWWIDTH / 2 + 10
    for live in range(PLAYERS[1].lives):
        SCREEN.blit(heart, (baseHeartPos, WINDOWHEIGHT - BOTTOMOFFSET / 2 + 10))
        baseHeartPos += 15


    # blit text to surface
    SCREEN.blit(playerOneScoreSurf, playerOneScoreText)
    SCREEN.blit(playerTwoScoreSurf, playerTwoScoreText)