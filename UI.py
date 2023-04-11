import Vector
import pygame

class UIButton:
    def __init__(
            self,
            label: str,
            position: Vector.Vec2,
            size: Vector.Vec2,
            callback_functions
        ):
        
        arial_font = pygame.font.SysFont('umeminchos3', 36)
        self.__label = label
        self.__position = position
        self.__surface = pygame.Surface(
            (size.x, size.y)
        )
        self.__text = arial_font.render(
            label,
            False,
            pygame.Color('white')
        )
        self.__text_center = self.__text.get_rect(
            center=(size / 2).get()
        )
        self.__is_hover = False
        self.__surface.fill(pygame.Color("grey"))
        self.__callback_functions = callback_functions

    def setPosition(self, position: Vector.Vec2):
        self.__position = position

    def getPosition(self):
        return self.__position
    
    def getLabel(self):
        return self.__label
    
    def setLabel(self, label: str):
        self.__label = label

    def getSurface(self):
        return self.__surface
    
    def checkHover(self, mouse_position):
        if self.__surface.get_rect(
            topleft=self.__position.get()
        ).collidepoint(mouse_position):
            self.__is_hover = True
        else:
            self.__is_hover = False

    def isHovered(self):
        return self.__is_hover
    
    def update(self):
        if self.__is_hover:
            self.__surface.fill(
                pygame.Color("blue")
            )
        else:
            self.__surface.fill(
                pygame.Color("grey")
            )
        self.__surface.blit(
            self.__text,
            self.__text_center
        )

    def click(self, button: bool):
        if button and self.__is_hover:
            self.__surface.fill("white")
            return self.__callback_functions()
    