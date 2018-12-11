import pygame, sys
from pygame.locals import *
from pathlib import Path

SCALE = 2
FPS = 300 * SCALE

WINWIDTH = 400 * SCALE
WINHEIGHT = 300 * SCALE
WINMIDX = WINWIDTH/2
WINMIDY = WINHEIGHT/2
OBJECTWIDTH = 7 * SCALE
PADDLESIZE = 50 * SCALE
PADDLEHEIGHT = (WINHEIGHT - PADDLESIZE)/2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def drawArena():
    DISPLAYSURFACE.fill((0,0,0))
    pygame.draw.line(DISPLAYSURFACE, WHITE, ((WINWIDTH/2),0), ((WINWIDTH/2), WINHEIGHT), 1*SCALE)

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
    p1ScoreRect.topleft = (WINWIDTH/2 + (5 * SCALE), 15*SCALE)
    DISPLAYSURFACE.blit(p1ScoreSurface, p1ScoreRect)
    p2ScoreSurface = FONT.render(score2, True, WHITE)
    p2ScoreRect = p2ScoreSurface.get_rect()
    p2ScoreRect.topleft = (WINWIDTH/2 - (28 * SCALE), 15*SCALE)
    DISPLAYSURFACE.blit(p2ScoreSurface, p2ScoreRect)

def drawPaddle(paddle):
    if paddle.bottom > WINHEIGHT:
        paddle.bottom = WINHEIGHT
    elif paddle.top < 1:
        paddle.top = 1
    pygame.draw.rect(DISPLAYSURFACE, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURFACE, WHITE, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeTB(ball, ballDirY):
    if ball.top == 0 or ball.bottom == WINHEIGHT:
        HITSOUND.play()
        return -1        
    return 1

def checkEdgeLR(ball, ballDirX, score1, score2):
    global SCORESTATUS
    if ball.left == 0:
        score1 += 1
        ballDirX *= -1
        SCORESTATUS = True
    elif ball.right == WINWIDTH:
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
    if ballDirX == 1 and paddle1.left == ball.right and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
        HITSOUND.play()
        return -1
    elif ballDirX == -1 and paddle2.right == ball.left and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        HITSOUND.play()
        return -1
    return 1
        
def main():
    pygame.init()
    global DISPLAYSURFACE
    global FONTSIZE
    global FONT
    global HITSOUND
    global SCORESTATUS

    #Load Audio
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    p = Path('./')
    p = p / 'pong' / '4359__noisecollector__pongblipf4.wav'
    HITSOUND = pygame.mixer.Sound(str(p.absolute()))

    #Setting up fonts for the score
    FONTSIZE = 20 * SCALE
    FONT = pygame.font.Font('freesansbold.ttf', FONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    pygame.display.set_caption('Pong')

    ballDirX , ballDirY= -1, -1
    score1, score2 = 0, 0
    SCORESTATUS = True    

    ball = pygame.Rect(WINMIDX - (OBJECTWIDTH/2), WINMIDY - (OBJECTWIDTH/2), OBJECTWIDTH, OBJECTWIDTH)
    paddle1 = pygame.Rect(WINWIDTH - (OBJECTWIDTH*2), PADDLEHEIGHT, OBJECTWIDTH, PADDLESIZE)
    paddle2 = pygame.Rect(OBJECTWIDTH, PADDLEHEIGHT, OBJECTWIDTH, PADDLESIZE)

    pygame.mouse.set_visible(0)

    while True:
        drawArena()
        drawScore(score1, score2)
        drawBall(ball)
        drawPaddle(paddle1)
        drawPaddle(paddle2)

        pygame.display.update()

        if SCORESTATUS:
            pygame.time.wait(500)
            SCORESTATUS = False

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            paddle1.y -= 1
        elif keys[K_DOWN]:
            paddle1.y += 1
        if keys[K_w]:
            paddle2.y -= 1
        elif keys[K_s]:
            paddle2.y += 1
        
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirY *= checkEdgeTB(ball, ballDirY)
        ballDirX *= checkHitBall(ball, paddle1, paddle2, ballDirX)
        ball, ballDirX, score1, score2 = checkEdgeLR(ball, ballDirX, score1, score2)
        
        if SCORESTATUS:
            ball, paddle1, paddle2 = resetObjects(ball, paddle1, paddle2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
if __name__=='__main__':
    main()