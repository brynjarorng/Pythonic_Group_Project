import pygame as pg
from pathlib import Path
from BaseCharacter import BaseCharacter

class WhackmanChar(BaseCharacter):
    def __init__(self, imgPath, startPos, size, speed):
        super().__init__(imgPath, startPos, size, speed)
        self.currDir = (0, 0)
        self.nextDir = (0, 0)
        self.points = 0