import Vector
import pygame


class Tile:
    def __init__(
        self,
        image: pygame.Surface,
        rect: tuple,
        position: Vector.Vec2,
        is_solid: bool
    ):
        self.surface = image.subsurface(rect)
        self.rect = rect
        self.position = position
        self.is_solid = is_solid

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
