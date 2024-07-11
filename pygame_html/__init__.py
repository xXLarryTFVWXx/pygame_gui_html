import os, sys, html, html.parser, html.entities
import pygame
import pygame_gui
from . import menu

import pygame_gui.data.licenses
from . import versioning, menu, transitions
from .logger import *
pygame.init()
LOAD_IMAGE = pygame.event.custom_type()

def make_window(size, flags):
    pygame.display.set_mode(size, flags)
    menu.manager = pygame_gui.UIManager(size)
    return


class Parser(html.parser.HTMLParser):
    def __init__(self, file, name="HTMLDoc", *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.file = file
        self.flags = 0
        self.name = name
        self.image_sources = {}
        self.tag_attributes = []
        if __debug__:
            print(f"object {self} created at {hex(id(self))} with size {sys.getsizeof(self)} bytes")
    def __str__(self):
        return self.name
    
    def handle_decl(self, decl: str) -> None:
        if not decl.split(" ")[1].lower() == "gxml":
            raise SyntaxError("PYGUI file must be based on xhtml without a url")
    
    def handle_viewport_tag(self):
        flags = 0
        for index, attribute_pair in enumerate(self.tag_attributes):
            match attribute_pair:
                case ("context", context):
                    flags |= pygame.OPENGL if context.lower() == "3d" else 0
                case ("size", size):
                    size = tuple([int(dimension) for dimension in size.split('x')])
                case ("fullscreen", flag):
                    flags |= (pygame.FULLSCREEN | pygame.SCALED) if flag.lower() == "true" else 0
                case _:
                    print(f"ignoring attribute pair {index} containing {attribute_pair}")
        # pygame.display.set_mode(size, flags) # If commented out, the rest of the code isn't ready
        self.UIManager = menu.get_manager()
    def handle_buttons(self):
        attributes = {}
        for key, value in self.tag_attributes:
            attributes[key] = value
        if __debug__:
            log(attributes)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if __debug__:
            log(f"tag:{tag} attributes {attrs}")
        self.tag_attributes = attrs
        if tag.lower() == "meta":
            match attrs[0][0].lower():
                case "version":
                    # Basic version checking
                    if attrs[0][1] in versioning.INCOMPATIBLE_VERSIONS:
                        log(f"Version {attrs[0][1]} is incompatible with the current version")
                        raise Exception(f"Version {attrs[0][0]} is no longer supported.")
                case "viewport":
                    self.handle_viewport_tag()
                case "button":
                    self.handle_buttons()
                case _:
                    log(f"ignoring attribute {attrs} for tag {tag.lower()}")
        if tag.lower() == "link":
            self.handle_link_tags()
        if tag.lower() == "img":
            self.handle_img_tag()
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "menu":
            if self.in_menu:
                raise Exception("You cannot have nested menus.")
            self.in_menu = True
            for index, attribute_pair in enumerate(attrs):
                match attribute_pair:
                    case ("name", name):
                        menu_name = name
                    case ("background-image", img):
                        image_location = img
                    case ("event", evnt):
                        self.to_event = evnt # event to be posted after a timer expires
                    case ("duration", milliseconds):
                        timer = milliseconds # The duration for the event above
                    case ("background_music", bgm):
                        music_location = bgm
                    case _:
                        if index == len(attrs) - 1:
                            menu.menus.append(menu.Menu(menu_name))
                            menu.menus[-1].set_background(image_location)
                            menu.menus[-1].set_music_track(bgm)
                        log(f"ignoring attribute pair {index} with content {attribute_pair}")
    def handle_img_tag(self):
        """"""
        attributes = {}
        for key, value in self.tag_attributes:
            attributes[key] = value
        log(f"{attributes}")
        if "global" in attributes.keys():
            img_id = attributes.get("id", "noid")
            pygame.event.post(pygame.Event(LOAD_IMAGE, {'image': pygame.image.load(attributes.get('src', "error.png")), "id": img_id}))
            if __debug__:
                log(f"Image {img_id} to be loaded globally.")
        if __debug__:
            print(attributes)

    def load(self):
        with open(self.file) as file:
            self.data = file.read()
        self.feed(self.data)
        log(f"file {self.file} read and interpreted resulting in object {str(self)}@{hex(id(self))} being of size {sys.getsizeof(self)} bytes")
    def get_UI_Manager(self) -> pygame_gui.UIManager:
        return self.UIManager
    def get_buttons(self):
        return self.buttons

if __debug__:
    log("library loaded")