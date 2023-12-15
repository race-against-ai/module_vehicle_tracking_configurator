"""Contains functions that are used by different files."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path


class DirectoryNotFoundError(Exception):
    """Raised when the directory is not found.
    
    Args:
        
    """

    def __init__(self, message: str = "directory was not found.") -> None:
        self.message = message
        super().__init__(self.message)


def find_base_directory() -> Path | DirectoryNotFoundError:
    """Find the base directory of the project. If not found exits the program.

    Returns:
        Path: The base directory.
    """
    search_paths = {Path().cwd(), Path().cwd().parent, Path(__file__).parent.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    return DirectoryNotFoundError("Base directory was not found.")
