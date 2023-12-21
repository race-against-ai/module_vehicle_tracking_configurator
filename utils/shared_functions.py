"""Contains functions that are used by different files."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
from json import load

from typing import Any


MAIN_DIR = Path(__file__).parent.parent


class DirectoryNotFoundError(Exception):
    """Raised when the directory is not found.

    Args:

    """

    def __init__(self, message: str = "directory was not found.") -> None:
        self.message = message
        super().__init__(self.message)


def get_all_schemas() -> dict[str, dict[str, Any]]:
    """Get all the schemas in the schemas directory.

    Returns:
        list[Path]: A list of all the schemas.
    """
    schemas: dict[str, dict[str, Any]] = {}
    for schema in (MAIN_DIR / "schema").glob("*.json"):
        with open(schema, "r", encoding="utf-8") as schema_file:
            schema_name = schema.stem
            schemas[schema_name] = load(schema_file)
    return schemas
