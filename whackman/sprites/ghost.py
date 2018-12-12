import pygame as pg
from .BaseCharacter import BaseCharacter

class ghost(BaseCharacter):
    def __init__(self, img, char, startPos, size, speed):
        super().__init__(img, char, startPos, size, speed)
        self.personality = 0
        self.mode = 0
        self.path = []