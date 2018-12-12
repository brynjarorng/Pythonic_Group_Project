import pygame as pg
from pathlib import Path

class BaseCharacter:
    def __init__(self, imgPath, startPos, size, speed):
        self.imgPath = ('') ### Nota glob!
        self.pos = startPos
        self.size = size
        self.speed = speed  ### Tuple (curr, max)