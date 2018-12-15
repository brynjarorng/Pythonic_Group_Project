import pygame as pg
import pygame.gfxdraw
from pathlib import Path
import sys

def menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS):
    FPSCLOCK = pg.time.Clock()
    openMenu = True

    # 0 - Continue
    # 1 - restart
    # 2 - Quit
    menuState = 0
    menuDelay = 0

    # -1 - Do nothing
    # 0 - go down
    # 1 - go up
    # 2 - select
    nextMenuState = 0
    
    # main menu background positioning
    rec = pg.Rect(0, 0, WINDOWWIDTH * (2 / 3), WINDOWHEIGHT * (2 / 3))
    rec.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    # wait here in order to not instantly exit the menu
    pg.time.wait(400)
    
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
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3)))
        elif menuState == 1:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 100))
        elif menuState == 2:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 200))
        pg.gfxdraw.box(SCREEN, selectBar, (100, 0, 0, 255))

        # main menu options text
        continueTextSurf, continueText = text_objects("CONTINUE", largeText)
        continueText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3)))

        restartTextSurf, restartText = text_objects("RESTART", largeText)
        restartText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 100))

        quitTextSurf, quitText = text_objects("EXIT TO MENU", largeText)
        quitText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 200))

        # blit text to surface
        SCREEN.blit(continueTextSurf, continueText)
        SCREEN.blit(restartTextSurf, restartText)
        SCREEN.blit(quitTextSurf, quitText)
        
        # the menu selection logic
        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_ESCAPE]:
            quit()
            return True
        elif keyinput[pg.K_DOWN]:
            nextMenuState = 0
        elif keyinput[pg.K_UP]:
            nextMenuState = 1
        elif keyinput[pg.K_RETURN]:
            nextMenuState = 2
        else:
            nextMenuState = -1
        
        # EXEC logic
        if menuDelay == 12:
            menuDelay = 0
            if nextMenuState == 0:
                menuState += 1
                if menuState == 3:
                    menuState = 0
            elif nextMenuState == 1:
                menuState -= 1
                if menuState == -1:
                    menuState = 2
            elif nextMenuState == 2:
                if menuState == 0:
                    return True
                elif menuState == 1:
                    # to implement!!!!!
                    return
                elif menuState == 2:
                    pg.quit()
                    quit()
        else:
            menuDelay += 1

        
        pg.display.flip()


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