from pathlib import Path
import os, sys
import pygame as pg
import pygame.gfxdraw
import snake.snake as snakeGame
import randomPong.randomPong as pongGame
import whackman.whackman as whackmanGame

pg.init()
pg.display.set_caption('Mini arcade')
clock = pg.time.Clock()
height = 800
width = 800

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

basePath = Path(sys.argv[0]).parent
titleIconPath = basePath / "whackman" / "data" / "sprites" / "ghost.png"
titleIcon = pg.image.load(str(titleIconPath))
pg.display.set_icon(titleIcon)

fontLoc = basePath / "whackman" / "data" / "fonts" / "minotaur.ttf"
largeText = pg.font.Font(str(fontLoc), 60)
menuTitle = pg.font.Font(str(fontLoc), 100)

# menu text elements
ArcadeSurf, miniArcade = text_objects("Mini arcade", menuTitle)
SnakeSurf, snake = text_objects("Snake", largeText)
PongSurf, pong = text_objects("Pong", largeText)
WhackmanSurf, whackman = text_objects("Whackman", largeText)
QuitGameSurf, quitGame = text_objects("Quit", largeText)
selectBar = pg.Rect(0, 0, 800, 100)

# 0 - play snake
# 1 - play pong
# 2 - play whackman
# 3 - quit
menuState = 0

# Find center for text
miniArcade.center = ((height/2),(width/2) - 250)
snake.center = ((height/2),(width/2) - 100)
pong.center = ((height/2),(width/2))
whackman.center = ((height/2),(width/2) + 100)
quitGame.center = ((height/2),(width/2) + 200)

while 1:
    gameDisplay = pg.display.set_mode((height,width))
    
    # UI elements
    gameDisplay.fill((0,0,0))

    # add elements to drawing surface
    gameDisplay.blit(ArcadeSurf, miniArcade)
    gameDisplay.blit(SnakeSurf, snake)
    gameDisplay.blit(PongSurf, pong)
    gameDisplay.blit(WhackmanSurf, whackman)
    gameDisplay.blit(QuitGameSurf, quitGame)

    keyinput = pg.key.get_pressed()
    if keyinput[pg.K_ESCAPE]:
        pg.quit()
        quit()
    
    # Move displayed selection
    selectBar.center = ((height/2),(width/2) + 100 * (menuState - 1))
    pg.gfxdraw.box(gameDisplay, selectBar, (0, 25, 175, 125))

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