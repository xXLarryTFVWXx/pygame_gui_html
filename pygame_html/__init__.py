import sys, html, html.parser, html.entities
import pygame
from . import versioning, characters
from .logger import *

class Parser(html.parser.HTMLParser):
    def __init__(self, file, name="HTMLDoc", *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.file = file
        self.flags = 0
        self.name = name
        if __debug__:
            print(f"object {self} created at {hex(id(self))} with size {sys.getsizeof(self)} bytes")
    def __str__(self):
        return self.name
    def handle_decl(self, decl: str) -> None:
        if not decl.lower() == "doctype gxhtml":
            raise SyntaxError("HTML file must be based on HTML5")
    def handle_viewport_tag(self, attributes):
        flags = 0
        for index, attribute_pair in enumerate(attributes):
            match attribute_pair:
                case ("viewport", context):
                    flags |= pygame.OPENGL if context.lower() == "3d" else 0
                case ("size", size):
                    size = tuple([int(dimension) for dimension in size.split('x')])
                case ("fullscreen", flag):
                    flags |= (pygame.FULLSCREEN | pygame.SCALED) if flag.lower() == "true" else 0
                case _:
                    print(f"ignoring attribute pair {index} containing {attribute_pair}")
        # pygame.display.set_mode(size, flags) # If commented out, the rest of the code isn't ready
    def load_character(self, attributes):
        characters.new_character(*attributes)
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        log(tag, attrs)
        if tag.lower() == "meta":
            match attrs[0][0].lower():
                case "version":
                    # Basic version checking
                    if attrs[0][1] in versioning.INCOMPATIBLE_VERSIONS:
                        log(f"Version {attrs[0][1]} is incompatible with the current version")
                case "viewport":
                    self.handle_viewport_tag(attrs)
                case _:
                    log(f"ignoring attribute {attrs} for tag {tag.lower()}")
    def load(self):
        with open(self.file) as file:
            self.data = file.read()
        self.feed(self.data)
        log(f"file {self.file} read and interpreted resulting in object {str(self)}@{hex(id(self))} being of size {sys.getsizeof(self)} bytes")

