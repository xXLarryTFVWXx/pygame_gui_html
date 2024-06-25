from pygame import time, error

def get_timestamp() -> str:
    """convert pygame.time.get_ticks to hours:minutes:seconds.miliseconds"""
    ticks = time.get_ticks()/1000
    seconds = ticks%60
    minutes = int(seconds/60)
    hours = int(minutes/60)
    return f"{hours}:{minutes}:{seconds}"

def log(*data) -> None:
    """Basic wrapper around print to output to a file"""
    with open("log.txt", "w") as log_file:
        for info in data:
            print(f"[{get_timestamp()}]{info}", file=log_file)

__all__ = ["log", "get_timestamp"]
