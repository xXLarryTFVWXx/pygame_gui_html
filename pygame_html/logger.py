time = None
import os
try:
    from pygame import time as pygtime, error
except ImportError:
    import time
if time is not None:
    start_time = round(time.time(), 4)
def get_timestamp() -> str:
    """convert pygame.time.get_ticks to hours:minutes:seconds.miliseconds"""
    if time is None:
        ticks = pygtime.get_ticks()/1000
        seconds = ticks%60
        minutes = int(ticks/60)
        hours = int(minutes/60)
    else:
        current_time = round(time.time()-start_time, 4)
        seconds = round(current_time%60, 4)
        minutes = round(current_time/60%60, 0)
        hours = round(minutes/60, 0)
    if __debug__:
        print(f"{hours}:{minutes}:{seconds}")
    return f"{hours}:{minutes}:{seconds}"

def log(*data) -> None:
    """Basic wrapper around print to output to a file"""
    log_exists = os.path.isfile("log.txt")
    with open("log.txt", "a") as log_file:
        for info in data:
            log_file.write(f"[{get_timestamp()}]{info}\n")
if os.path.isfile("log.txt"):
    os.remove("log.txt")
if __debug__:
    log("logger module loaded")
__all__ = ["log"]
