import pygame as pg

pg.init()

class whackMan(pg.sprite.Sprite):
    def __init__(self, x, y, changeSize):
        self.x = x
        self.y = y
        self.changeSize = changeSize

        pg.sprite.Sprite.__init__(self)
        self.img = pg.image.load('knight-transparent.gif')
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)

    
    # Move the player and update the position
    def moveD(self):
        self.y += self.changeSize
        self.rect.center = (self.x, self.y)
    
    def moveU(self):
        self.y -= self.changeSize
        self.rect.center = (self.x, self.y)
    
    def moveL(self):
        self.x -= self.changeSize
        self.rect.center = (self.x, self.y)
    
    def moveR(self):
        self.x += self.changeSize
        self.rect.center = (self.x, self.y)
