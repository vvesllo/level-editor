import Vector

import pygame
import enum

class TileTypeEnum:
    DEFAULT=0
    SLOPE_LEFT=1
    SLOPE_RIGHT=2
    DANGER=3
    JUMPER=4
    END=5
    PLAYER=6

class Tile:
    def __init__(
        self,
        image: pygame.Surface,
        rect: tuple,
        position: Vector.Vec2,
        is_solid: bool,
        type: int
    ):
        self.surface = image.subsurface(rect)
        self.rect = rect
        self.position = position
        self.is_solid = is_solid
        self.type = type

    def getRect(self):
        return self.rect
    
    def getSurface(self):
        return self.surface
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, position: Vector.Vec2):
        self.position = position
    
    def move(self, coords: Vector.Vec2):
        self.position += coords
    
    def isSolid(self):
        return self.is_solid

    def getType(self):
        return self.type

