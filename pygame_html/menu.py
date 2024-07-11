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
        self.surface = pygame.display.get_surface()
        menus.update((self.name, self))

    def add_buttons(self, buttons: list[pygame_gui.elements.UIButton]):
        for button in buttons:
            self.buttons.append(button)

    def load(self):
        self.background = pygame.image.load(self.background_image_file).convert()
        self.music = pygame.mixer_music.load(self.background_music_file)

    def draw(self):
        if not self.is_animated:
            self.surface.blit(self.background, (0, 0))
            return
        if self.animation.animation_type == "scroll":
            self.surface.blit(
                self.background,
                (0, 0),
            )


# Please refrain from acessing this directly,
# I have no Idea what would happen if one were to directly access this.
# DON'T even THINK about making one of these a NoneValue!
menus: dict[str, Menu | None] = {
    "current": None  # This is only here so then I don't get fussed at by pylance
}

manager: pygame_gui.UIManager = pygame_gui.UI_Manager((600, 600))


def get_manager() -> pygame_gui.UIManager:
    return manager


def make_button(rect: pygame.Rect, text: str, background: pygame.Color | str):
    return pygame_gui.elements.UIButton(rect, text, get_manager())
