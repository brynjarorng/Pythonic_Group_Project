import pygame as pg

class BaseCharacter:
    def __init__(self, img, char, startPos, size, speed):
        self.img = img
        self.char = char
        self.pos = startPos
        self.size = size
        self.speed = speed  ### Tuple (curr, max)