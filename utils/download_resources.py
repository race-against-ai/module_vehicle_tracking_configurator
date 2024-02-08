#!/usr/bin/env python
"""Download all the resources from the webdav server."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
from typing import Any
from json import load

from webdav4.client import Client


BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
WEBDAV_REMOTE_PATH = "/large_files"


def main() -> None:
    """Download all the resources from the webdav server."""
    with open(BASE_DIR / "vehicle_tracking_configurator_config.json", "r", encoding="utf-8") as f:
        config: dict[str, Any] = load(f)["resource_downloader"]

    webdav_url = config["url"]
    client_name = config["client_name"]
    client_password = config["client_password"]
    client = Client(webdav_url, auth=(client_name, client_password))

    ls_results: list[str] = client.ls(WEBDAV_REMOTE_PATH, False)
    for file in ls_results:
        file_name = file[::-1]
        file_name = file_name[: file_name.find("/")][::-1]

        if RESOURCES_DIR.is_file():
            raise FileExistsError("A file with the name 'resources' already exists. Can't create the directory.")
        if not RESOURCES_DIR.exists():
            RESOURCES_DIR.mkdir()

        dir_for_file = RESOURCES_DIR / file_name

        print("Downloading: " + file_name)
        client.download_file(file, dir_for_file)
        if Path.exists(dir_for_file):
            print("File downloaded successfully")
        else:
            print("File could not be downloaded")
        print("\n")


if __name__ == "__main__":
    main()
