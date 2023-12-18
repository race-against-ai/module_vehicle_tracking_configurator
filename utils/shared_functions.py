"""Contains functions that are used by different files."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path


FILE_DIR = Path(__file__).parent


class DirectoryNotFoundError(Exception):
    """Raised when the directory is not found.
    
    Args:
        
    """

    def __init__(self, message: str = "directory was not found.") -> None:
        self.message = message
        super().__init__(self.message)


def find_base_directory() -> tuple[Path, None | DirectoryNotFoundError]:
    """Find the base directory of the project. If not found exits the program.

    Returns:
        Path: The base directory or any empty path.
        None | DirectoryNotFoundError: None if the directory is found, else a directory not found error.
    """
    search_paths = {Path().cwd(), Path().cwd().parent, FILE_DIR.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return (directory, None)
    return (Path(), DirectoryNotFoundError("Base directory was not found."))
