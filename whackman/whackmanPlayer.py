import pygame as pg
import glob

pg.init()

class whackMan(pg.sprite.Sprite):
    def __init__(self, x, y, changeSize):
        self.x = x
        self.y = y
        self.changeSize = changeSize
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob('sprites/walk/*.png')
        self.ani.sort()
        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.img = pg.image.load(self.ani[0])
        self.img = pg.transform.scale(self.img, (50, 50))
        self.rect = self.img.get_rect()
        self.update()

        pg.sprite.Sprite.__init__(self)
        self.rect.center = (x,y)

    def update(self):
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.img = pg.image.load(self.ani[self.ani_pos])
            self.img = pg.transform.scale(self.img, (50, 50))
            self.ani_speed = self.ani_speed_init
            if self.ani_pos == self.ani_max:
                self.ani_pos = 0
            else:
                self.ani_pos += 1
    
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
