import pygame as pg
import sys
from pathlib import Path

class Entity:
    def __init__(self, img, char, eType, pos, moveDir, moveCount, speed):
        self.img = pg.transform.scale(pg.image.load(str(img)), (23,22))
        self.char = char
        self.eType = eType
        self.pos = pos
        self.moveDir = moveDir
        self.speed = speed
        self.moveCount = moveCount