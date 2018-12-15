import pygame as pg
import sys
from pygame.locals import *
from pathlib import Path
import random

SCALE = 2
FPS = 200 * SCALE

WINDOWWIDTH = 400 * SCALE
WINDOWHEIGHT = 300 * SCALE
WINMIDX = WINDOWWIDTH/2
WINMIDY = WINDOWHEIGHT/2
OBJECTWIDTH = 7 * SCALE
PADDLESIZE = 50 * SCALE
PADDLEHEIGHT = (WINDOWHEIGHT - PADDLESIZE)/2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def drawArena():
    SCREEN.fill((0,0,0))
    pg.draw.line(SCREEN, WHITE, ((WINDOWWIDTH/2),0), ((WINDOWWIDTH/2), WINDOWHEIGHT), 1*SCALE)

def drawScore(score1, score2):
    if score1 < 10:
        score1 = '0' + str(score1)
    else:
        score1 = str(score1)
    if score2 < 10:
        score2 = '0' + str(score2)
    else:
        score2 = str(score2)

    p1ScoreSurface = FONT.render(score1, True, WHITE)
    p1ScoreRect = p1ScoreSurface.get_rect()
    p1ScoreRect.topleft = (WINDOWWIDTH/2 + (5 * SCALE), 15*SCALE)
    SCREEN.blit(p1ScoreSurface, p1ScoreRect)
    p2ScoreSurface = FONT.render(score2, True, WHITE)
    p2ScoreRect = p2ScoreSurface.get_rect()
    p2ScoreRect.topleft = (WINDOWWIDTH/2 - (28 * SCALE), 15*SCALE)
    SCREEN.blit(p2ScoreSurface, p2ScoreRect)

def drawPaddle(paddle):
    if paddle.bottom > WINDOWHEIGHT:
        paddle.bottom = WINDOWHEIGHT
    elif paddle.top < 1:
        paddle.top = 1
    pg.draw.rect(SCREEN, WHITE, paddle)

def drawBall(ball):
    pg.draw.rect(SCREEN, WHITE, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeTB(ball, ballDirY):
    if ball.top == 0 or ball.bottom == WINDOWHEIGHT:
        HITSOUND.play()
        return -1        
    return 1

def checkEdgeLR(ball, ballDirX, score1, score2):
    global SCORESTATUS
    if ball.left == 0:
        score1 += 1
        ballDirX *= -1
        SCORESTATUS = True
    elif ball.right == WINDOWWIDTH:
        score2 += 1
        ballDirX *= -1
        SCORESTATUS = True
    return ball, ballDirX, score1, score2

def resetObjects(ball, paddle1, paddle2):
    ball.x = WINMIDX - (OBJECTWIDTH/2)
    ball.y = WINMIDY - (OBJECTWIDTH/2)
    paddle1.y = PADDLEHEIGHT
    paddle2.y = PADDLEHEIGHT
    return ball, paddle1, paddle2

def checkHitBall(ball, paddle1, paddle2, ballDirX):
    # right paddle
    if ballDirX == 1 and paddle1.left == ball.right and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
        HITSOUND.play() 
        return (-1, [-1, 1][random.randint(0,1)])
        # REMOVE?
        # check top third
        if paddle1.top <= ball.centery < paddle1.top + (paddle1.bottom-paddle1.top)*(1/4):
            return (-1, 1)
        # check bottom third
        elif paddle1.bottom - (paddle1.bottom-paddle1.top)*(1/4) <= ball.centery < paddle1.bottom:
            return (-1 , -1)
        # else middle
        else:
            return (-1, 0)
            
    # left paddle
    elif ballDirX == -1 and paddle2.right == ball.left and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        HITSOUND.play()
        return (-1, [-1, 1][random.randint(0,1)])
        # REMOVE?
        # check top third
        if paddle2.top <= ball.centery < paddle2.top + (paddle2.bottom-paddle2.top)*(1/4):
            return (-1, 1)
        # check bottom third
        elif paddle2.bottom - (paddle2.bottom-paddle2.top)*(1/4) <= ball.centery < paddle2.bottom:
            return (-1 , -1)
        # else middle
        else:
            return (-1, 0)
    return (1, 1)


def menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS):
    FPSCLOCK = pg.time.Clock()
    openMenu = True

    # 0 - Continue
    # 1 - Exit
    menuState = 0

    # -1 - Do nothing
    # 0 - go down
    # 1 - go up
    # 2 - select
    nextMenuState = 0
    
    # main menu background positioning
    rec = pg.Rect(0, 0, WINDOWWIDTH * (2 / 3), WINDOWHEIGHT * (2 / 3))
    rec.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    # wait here in order to not instantly exit the menu
    pg.time.wait(250)
    
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
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) - 50))
        elif menuState == 1:
            selectBar.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 50))
        pg.gfxdraw.box(SCREEN, selectBar, (100,0,0,127))

        # main menu options text
        continueTextSurf, continueText = text_objects("CONTINUE", largeText)
        continueText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) - 50))

        quitTextSurf, quitText = text_objects("EXIT TO MENU", largeText)
        quitText.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT * (1 / 3) + 50))

        # blit text to surface
        SCREEN.blit(continueTextSurf, continueText)
        SCREEN.blit(quitTextSurf, quitText)
        
        # the menu selection logic
        for ev in pg.event.get():
            if ev.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()
            
            elif ev.type == pg.locals.KEYDOWN:
                if ev.key == pg.K_DOWN and ev.type == pg.KEYDOWN:
                    menuState += 1
                    if menuState == 2:
                        menuState = 0
                elif ev.key == pg.K_UP and ev.type == pg.KEYDOWN:
                    menuState -= 1
                    if menuState == -1:
                        menuState = 1
                elif ev.key == pg.K_RETURN and ev.type == pg.KEYDOWN:
                    if menuState == 0:
                        return True
                    elif menuState == 1:
                        return False
                elif ev.key == pg.K_ESCAPE and ev.type == pg.KEYDOWN:
                    return True
        
        pg.display.flip()

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect() 

        
def main():
    pg.init()
    global SCREEN
    global FONTSIZE
    global FONT
    global HITSOUND
    global SCORESTATUS

    #Load Audio
    pg.mixer.pre_init(44100, 16, 2, 4096)
    audioPath = Path(sys.argv[0]).parent / "randomPong" / '4359__noisecollector__pongblipf4.wav'
    HITSOUND = pg.mixer.Sound(str(audioPath))

    #Setting up fonts for the score
    FONTSIZE = 20 * SCALE
    FONT = pg.font.Font('freesansbold.ttf', FONTSIZE)

    FPSCLOCK = pg.time.Clock()
    SCREEN = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pg.display.set_caption('Pong')

    ballDirX , ballDirY= -1, -1
    score1, score2 = 0, 0
    SCORESTATUS = True    

    ball = pg.Rect(WINMIDX - (OBJECTWIDTH/2), WINMIDY - (OBJECTWIDTH/2), OBJECTWIDTH, OBJECTWIDTH)
    paddle1 = pg.Rect(WINDOWWIDTH - (OBJECTWIDTH*2), PADDLEHEIGHT, OBJECTWIDTH, PADDLESIZE)
    paddle2 = pg.Rect(OBJECTWIDTH, PADDLEHEIGHT, OBJECTWIDTH, PADDLESIZE)

    pg.mouse.set_visible(0)

    playGame = True
    while playGame:
        drawArena()
        drawScore(score1, score2)
        drawBall(ball)
        drawPaddle(paddle1)
        drawPaddle(paddle2)

        pg.display.update()

        # wait if either player scored
        if SCORESTATUS:
            pg.time.wait(500)
            SCORESTATUS = False

        keys = pg.key.get_pressed()

        # press the X to quit
        for event in pg.event.get():
            if event.type == QUIT:
                quit()
                sys.exit()\
        
        if keys[K_UP]:
            paddle1.y -= 1
        elif keys[K_DOWN]:
            paddle1.y += 1
        if keys[K_w]:
            paddle2.y -= 1
        elif keys[K_s]:
            paddle2.y += 1
        elif keys[K_ESCAPE]:
            playGame = menu(SCREEN, WINDOWHEIGHT, WINDOWWIDTH, FPS)
        
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirY *= checkEdgeTB(ball, ballDirY)
        tmpX, tmpY = checkHitBall(ball, paddle1, paddle2, ballDirX) 
        ballDirX *= tmpX
        ballDirY *= tmpY
        ball, ballDirX, score1, score2 = checkEdgeLR(ball, ballDirX, score1, score2)
        
        if SCORESTATUS:
            ball, paddle1, paddle2 = resetObjects(ball, paddle1, paddle2)

        pg.display.update()
        FPSCLOCK.tick(FPS)


def play():
    main()