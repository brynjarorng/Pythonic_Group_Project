import pygame as pg
import pygame.gfxdraw

def menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS):
    FPSCLOCK = pg.time.Clock()
    openMenu = True

    # 0 - Continue
    # 1 - restart
    # 2 - Quit
    menuState = 0
    
    # main menu background positioning
    rec = pg.Rect(0, 0, 520, 325)
    rec.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 30)

    # wait here in order to not instantly exit the menu
    pg.time.wait(400)
    
    pg.event.clear()
    while openMenu:
        FPSCLOCK.tick(FPS)
        pg.event.pump()

        # draw main background
        pg.gfxdraw.box(SCREEN, rec, (100, 100, 120, 245))

        # text on screen
        largeText = pg.font.Font('freesansbold.ttf', 60)

        # draw the selection bar
        selectBar = pg.Rect(0, 0, 520, 70)
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

        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()
            
            # 0 - exit
            # 1 - continue
            # 2 - restart
            elif ev.type == pg.locals.KEYDOWN:
                if ev.key == pg.K_DOWN:
                    menuState += 1
                    if menuState == 3:
                        menuState = 0
                elif ev.key == pg.K_UP:
                    menuState -= 1
                    if menuState == -1:
                        menuState = 2
                elif ev.key == pg.K_RETURN:
                    if menuState == 0:
                        return 1
                    elif menuState == 1:
                        return 2
                    elif menuState == 2:
                        return 0
                elif ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                    return 1

        
        pg.display.flip()


def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 