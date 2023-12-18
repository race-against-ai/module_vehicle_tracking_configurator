"""Contains functions that are used by different files."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
from json import load

from typing import Any


FILE_DIR = Path(__file__).parent
BASE_DIR = FILE_DIR.parent
SCHEMA_DIR = BASE_DIR / "vehicle_tracking_configurator" / "schema"


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

def get_all_schemas() -> dict[str, dict[str, Any]]:
    """Get all the schemas in the schemas directory.

    Returns:
        list[Path]: A list of all the schemas.
    """
    schemas: dict[str, dict[str, Any]] = {}
    for schema in SCHEMA_DIR.glob("*.json"):
        with open(schema, "r", encoding="utf-8") as schema_file:
            schema_name = schema.stem
            schemas[schema_name] = load(schema_file)
    return schemas
