import Vector
import pygame

class BaseUI:
    position = Vector.Vec2(0, 0)
    label = "NULL"
    font = ''
    text = None
    bg_color = pygame.Color(0xaa, 0xaa, 0xaa)
    
    def setPosition(self, position: Vector.Vec2):
        self.position = position

    def getPosition(self):
        return self.position
    
    def getLabel(self):
        return self.label
    
    def setLabel(self, label: str):
        self.label = label

    def getSurface(self):
        return self.surface

class UIButton(BaseUI):
    def __init__(
            self,
            label: str,
            position: Vector.Vec2,
            size: Vector.Vec2,
            callback_functions
        ):

        self.font = pygame.font.SysFont('microsoftsansserif', 20)
        self.label = label
        self.position = position

        self.surface = pygame.Surface(
            (size.x, size.y)
        )
        self.surface.fill(pygame.Color("grey"))
        self.text = self.font.render(
            label,
            False,
            pygame.Color(0x10, 0x10, 0x10)
        )
        self.__text_center = self.text.get_rect(
            center=(size / 2).get()
        )

        self.__is_hover = False
        self.__callback_functions = callback_functions

    def checkHover(self, mouse_position):
        if self.surface.get_rect(
            topleft=self.position.get()
        ).collidepoint(mouse_position):
            self.__is_hover = True
        else:
            self.__is_hover = False

    def isHovered(self):
        return self.__is_hover
    
    def update(self):
        if self.__is_hover:
            self.surface.fill(
                pygame.Color("white")
            )
        else:
            self.surface.fill(
                pygame.Color("grey")
            )
        self.surface.blit(
            self.text,
            self.__text_center
        )

    def click(self, button: bool):
        if button and self.__is_hover:
            self.surface.fill("white")
            return self.__callback_functions()
        
class UILabel(BaseUI):
    def __init__(
            self,
            label: str,
            position: Vector.Vec2,
            size: Vector.Vec2
        ):
        
        self.font = pygame.font.SysFont('microsoftsansserif', 20)
        self.label = label
        self.position = position

        self.surface = pygame.Surface(
            (size.x, size.y)
        )
        self.surface.fill(pygame.Color(self.bg_color))
        self.text = self.font.render(
            label,
            False,
            pygame.Color(0x10, 0x10, 0x10)
        )
        self.__text_center = self.text.get_rect(
            center=(size / 2).get()
        )

    def update(self):
        self.surface.blit(
            self.text,
            self.__text_center
        )

class UICheckBox(BaseUI):
    def __init__(
            self,
            label: str,
            position: Vector.Vec2,
            size: Vector.Vec2,
            value
        ):

        self.font = pygame.font.SysFont('microsoftsansserif', 20)
        self.label = label
        self.position = position

        self.surface = pygame.Surface(
            (size.x, size.y)
        )
        self.surface.fill(pygame.Color("grey"))
        self.text = self.font.render(
            label,
            False,
            pygame.Color(0x10, 0x10, 0x10)
        )
        self.__text_center = self.text.get_rect(
            center=(size / 2).get()
        )

        self.__mark = pygame.Surface(
            (5, size.y)
        )

        if value:
            self.__mark.fill(
                pygame.Color(0x10, 0xfa, 0x10)
            )
        else:
            self.__mark.fill(
                pygame.Color(0xfa, 0xfa, 0xfa)
            )
        self.surface.blit(
            self.__mark,
            (0, 0)
        )
        self.__is_hover = False
        self.__value = value

    def checkHover(self, mouse_position):
        if self.surface.get_rect(
            topleft=self.position.get()
        ).collidepoint(mouse_position):
            self.__is_hover = True
        else:
            self.__is_hover = False

    def isHovered(self):
        return self.__is_hover
    
    def update(self):
        if self.__is_hover:
            self.surface.fill(
                pygame.Color("white")
            )
        else:
            self.surface.fill(
                pygame.Color("grey")
            )
        self.surface.blit(
            self.text,
            self.__text_center
        )
            
        if self.__value:
            self.__mark.fill(
                pygame.Color(0x10, 0xfa, 0x10)
            )
        else:
            self.__mark.fill(
                pygame.Color(0xfa, 0xfa, 0xfa)
            )
        self.surface.blit(
            self.__mark,
            (0, 0)
        )

    def click(self, button: bool):
        if button and self.__is_hover:
            self.__value = not self.__value
            return self.__value
        