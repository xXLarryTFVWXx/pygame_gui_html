import pygame, pygame_gui
import pygame_gui.ui_manager
from .errors import *

valid_animations = []


if not hasattr(pygame, "IS_CE"):
    raise LibraryError("You need pygame_ce installed.")

class Menu:
    """Menu class"""
    def __init__(self, name) -> None:
        self.name = name
        self.buttons = []
        self.animation = None
        if not pygame.display.get_surface() == pygame.Surface((0,0)):
            self.surface = pygame.display.get_surface()
    def add_button(self, button:pygame_gui.elements.UIButton):
        self.buttons.append(button)
    def set_background(self, image_file:str, is_animated:bool=False, animation_type:str|None=None, size:pygame.rect.Rect|None=None):
        self.background_image_file = image_file
        if is_animated and animation_type in valid_animations and size is not None:
            self.animation
    def set_music_track(self, file_location:str):
        self.background_music_file = file_location
    def load(self):
        self.background = pygame.image.load(self.background_image_file).convert()
        self.music = pygame.mixer_music.load(self.background_music_file)
    def draw(self):
        if not self.is_animated:
            self.surface.blit(self.background, (0,0))
            return
        raise NotImplementedError

menus: list[Menu] = []

manager: pygame_gui.UIManager = pygame_gui.UI_Manager((600,600))

def get_manager() -> pygame_gui.UIManager:
    return manager

def make_button(rect: pygame.Rect, text: str, background: pygame.Color | str):
    return pygame_gui.elements.UIButton(rect, text, get_manager())