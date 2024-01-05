# Copyright (C) 2023, NG:ITL
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(fname):
    return open(Path(__file__).parent / fname).read()


setup(
    name="raai_module_template",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="NGITl",
    author_email="arne.hilbig@volkswagen.de",
    description=("RAAI module for configuring the raai_module_vehicle_tracking."),
    license="GPL 3.0",
    keywords="vehicle tracking configuration",
    url="https://github.com/vw-wob-it-edu-ngitl/raai_module_vehicle_tracking_configurator",
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires=["pynng~=0.7.2", "PySide6==6.5.3", "opencv-python~=4.8.1.78", "webdav4~=0.9.8", "pillow~=10.1.0", "jsonschema~=4.20.0"],
    include_package_data=True,
)
