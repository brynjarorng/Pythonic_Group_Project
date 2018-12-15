import pygame as pg
import pygame.gfxdraw
import snake.snake as snake
#import whackman.whackman.py as whackman

pg.init()
clock = pg.time.Clock()
height = 800
width = 800

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()    

# 0 - Play game
# 1 - Quit game
menuState = 0
while 1:
    gameDisplay = pg.display.set_mode((height,width))
    # UI elements
    gameDisplay.fill((255,255,255))
    largeText = pg.font.Font('freesansbold.ttf',115)
    # menu text elements
    PlayGameSurf, playGame = text_objects("Play Game", largeText)
    QuitGameSurf, quitGame = text_objects("Quit", largeText)
    playGame.center = ((height/2),(width/2) - 100)
    quitGame.center = ((height/2),(width/2) + 100)
    # add elements to drawing surface
    gameDisplay.blit(PlayGameSurf, playGame)
    gameDisplay.blit(QuitGameSurf, quitGame)

    keyinput = pg.key.get_pressed()
    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()
    # hover play game
    selectBar = pg.Rect(0, 0, 800, 130)
    if menuState == 0:
        selectBar.center = ((height/2),(width/2) - 100)
        # if hover should be changed to selector below
        if keyinput[pg.K_DOWN]:
            menuState = 1
    # hover quit
    elif menuState == 1:
        selectBar.center = ((height/2),(width/2) + 100)
        # if hover should be changed to selector above
        if keyinput[pg.K_UP]:
            menuState = 0
    pg.gfxdraw.box(gameDisplay, selectBar, (100,0,0,127))
    
    # check if to play game or quit the game
    if keyinput[pg.K_RETURN]:
        if menuState == 0:
            snake.play()
        elif menuState == 1:
            pg.quit()
            quit()

    pg.display.update()
    clock.tick(30)