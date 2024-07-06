from typing import Any
from pygame.event import *

NULL_STATE: dict = {
    "background": None
}

states = {}

def make(name, contents) -> None:
    if name in states.keys():
        raise KeyError(f"state {name} already exists")
    states[name] = contents

def query() -> dict[str, Any]:
    return states.get("current", None) # type: dict

def change(name:str):
    if name in states.keys():
        states['current'] = states.get(name)

def next():
    current_state = query()
    if "next state" in current_state.keys:
        change(current_state.get("next state", NULL_STATE))