class LibraryError(Exception):
    """Wrong library is installed"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)