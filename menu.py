import pygame as pg
import pygame.gfxdraw
import snake.snake as snakeGame
import randomPong.randomPong as pongGame
import whackman.whackman as whackmanGame

pg.init()
clock = pg.time.Clock()
height = 800
width = 800

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect() 

largeText = pg.font.Font('freesansbold.ttf',80)

# menu text elements
SnakeSurf, snake = text_objects("Play Snake", largeText)
PongSurf, pong = text_objects("Play Pong", largeText)
WhackmanSurf, whackman = text_objects("Play Whackman", largeText)
QuitGameSurf, quitGame = text_objects("Quit", largeText)
selectBar = pg.Rect(0, 0, 800, 100)

# 0 - play snake
# 1 - play pong
# 2 - play whackman
# 3 - quit
menuState = 0

while 1:
    gameDisplay = pg.display.set_mode((height,width))

    # UI elements
    gameDisplay.fill((255,255,255))

    snake.center = ((height/2),(width/2) - 200)
    pong.center = ((height/2),(width/2) - 100)
    whackman.center = ((height/2),(width/2))
    quitGame.center = ((height/2),(width/2) + 100)

    # add elements to drawing surface
    gameDisplay.blit(SnakeSurf, snake)
    gameDisplay.blit(PongSurf, pong)
    gameDisplay.blit(WhackmanSurf, whackman)
    gameDisplay.blit(QuitGameSurf, quitGame)


    keyinput = pg.key.get_pressed()
    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()
    
    # hover play snake
    if menuState == 0:
        selectBar.center = ((height/2),(width/2) - 200)
    # hover play pong
    elif menuState == 1:
        selectBar.center = ((height/2),(width/2) - 100)
    # hover play whackman
    elif menuState == 2:
        selectBar.center = ((height/2),(width/2))
    # hover quit
    elif menuState == 3:
        selectBar.center = ((height/2),(width/2) + 100)
    pg.gfxdraw.box(gameDisplay, selectBar, (100,0,0,127))

    # menu state machine
    for ev in pg.event.get():
        if ev.type == pg.locals.QUIT:
            pg.quit()
            sys.exit()
        
        elif ev.type == pygame.locals.KEYDOWN:
            if ev.key == pg.K_DOWN:
                menuState += 1
                if menuState == 4:
                    menuState = 0
            elif ev.key == pg.K_UP:
                menuState -= 1
                if menuState == -1:
                    menuState = 3
            elif ev.key == pg.K_RETURN:
                if menuState == 0:
                    snakeGame.play()
                elif menuState == 1:
                    pongGame.play()
                elif menuState == 2:
                    whackmanGame.play()
                elif menuState == 3:
                    pg.quit()
                    quit()
    pg.event.clear()
    

    pg.display.update()
    clock.tick(60)