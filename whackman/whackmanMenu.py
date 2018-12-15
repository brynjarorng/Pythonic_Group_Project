import pygame as pg
import pygame.gfxdraw

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

        quitTextSurf, quitText = text_objects("QUIT", largeText)
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
        if menuDelay == 15:
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