import pygame as pg

class Entity:
    def __init__(self, img, char, eType, pos, moveDir, moveCount, speed):
        self.img = img
        self.char = char
        self.eType = eType
        self.pos = pos
        self.moveDir = moveDir
        self.speed = speed
        self.moveCount = moveCount