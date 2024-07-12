import os, sys, html, html.parser, html.entities
from numpy import imag
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
        self.in_menu = False
        self.default_menu_image_location = None
        self.current_menu_buttons = []
        if __debug__:
            print(
                f"object {self} created at {hex(id(self))} with size {sys.getsizeof(self)} bytes"
            )

    def __str__(self):
        return self.name

    def handle_decl(self, decl: str) -> None:
        if not decl.split(" ")[1].lower() == "pgml":
            raise SyntaxError("PYGUI file must be based on xhtml without a url")

    def handle_viewport_tag(self):
        flags = 0
        for index, attribute_pair in enumerate(self.tag_attributes):
            match attribute_pair:
                case ("context", context):
                    flags |= pygame.OPENGL if context.lower() == "3d" else 0
                case ("size", size):
                    size = tuple([int(dimension) for dimension in size.split("x")])
                case ("fullscreen", flag):
                    flags |= (
                        (pygame.FULLSCREEN | pygame.SCALED)
                        if flag.lower() == "true"
                        else 0
                    )
                case _:
                    print(
                        f"ignoring attribute pair {index} containing {attribute_pair[index]}"
                    )
        # pygame.display.set_mode(size, flags) # If commented out, the rest of the code isn't ready
        self.UIManager = menu.get_manager()

    def handle_button_tag(self):
        attributes = {key: value for key, value in self.tag_attributes}
        if __debug__: log(attributes)
        button_image = "test.png"
        for attribute_pair in self.tag_attributes:
            match attribute_pair:
                case ('text', text):
                    button_text = text or "TEST"
                case ("pos", position):
                    button_position = position or "0,0"
                case ("size", size):
                    button_size = size or "200x300"
                case ("color", text_color):
                    font_color = text_color or "black"
                case ("background_image", background_image):
                    button_image = background_image
                case ("background_color", background_color):
                    button_background_color = background_color or "grey4"
                case _:
                    log(f"Invalid attribute pair {attribute_pair}")
        self.current_menu_buttons.append(
            menu.make_button(
                pygame.rect.Rect(pygame.Vector2([int(axis) for axis in button_position.split(",")]), pygame.Vector2([int(dimension) for dimension in button_size.split("x")])),
                button_text,
                button_image or pygame.Color(button_background_color)
            )
        )
        if __debug__:
            log(attributes)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if __debug__:
            log(f"tag:{tag} attributes {attrs}")
        self.tag_attributes = attrs
        if tag.lower() == "meta":
            if __debug__: log(attrs[0][0])
            match attrs[0][0].lower():
                case "version":
                    # Basic version checking
                    if attrs[0][1] in versioning.INCOMPATIBLE_VERSIONS:
                        log(
                            f"Version {attrs[0][1]} is incompatible with the current version"
                        )
                        raise Exception(
                            f"Version {attrs[0][1]} is no longer supported."
                        )
                case "viewport":
                    self.handle_viewport_tag()
                case _:
                    log(f"ignoring attribute {attrs} for tag {tag.lower()}")
        if tag.lower() == "button":
            self.handle_button_tag()
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
                    case ("id", name):
                        current_menu = menu_name = name
                    case ("background-image", img):
                        image_location = img or self.default_menu_image_location
                    case ("event", evnt):
                        to_event = evnt # event to be posted after a timer expires
                    case ("duration", milliseconds):
                        timer = milliseconds # The duration for the event above
                    case ("background_music", bgm):
                        music_location = bgm
                    case _:
                        if len(attrs) - 1 == index:
                            menu.Menu(
                                menu_name,
                                music_location,
                                image_location,
                                to_event,
                                timer,
                            )
                        log(
                            f"ignoring attribute pair {index} with content {attribute_pair}"
                        )
    
    def handle_endtag(self, tag: str) -> None:
        if self.in_menu and tag.lower() == "menu":
            self.in_menu = False

    def handle_img_tag(self):
        """"""
        attributes = {key: value for key, value in self.tag_attributes}
        if __debug__: log(attributes)
        if not self.in_menu:
            self.default_menu_image_location = self.tag_attributes
        log(f"{attributes}")
        if "global" in attributes.keys():
            img_id = attributes.get("id", "noid")
            pygame.event.post(
                pygame.Event(
                    LOAD_IMAGE,
                    {
                        "image": pygame.image.load(attributes.get("src", "error.png")),
                        "id": img_id
                    },
                )
            )
            if __debug__:
                log(f"Image {img_id} to be loaded globally.")
        if __debug__:
            print(attributes)

    def load(self):
        with open(self.file) as file:
            self.data = file.read()
        self.feed(self.data)
        log(
            f"file {self.file} read and interpreted resulting in object {str(self)}@{hex(id(self))} being of size {sys.getsizeof(self)} bytes"
        )

    def get_UI_Manager(self) -> pygame_gui.UIManager:
        return self.UIManager

    def get_buttons(self):
        return self.buttons


if __debug__:
    log("library loaded")
