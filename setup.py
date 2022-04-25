"""Mindee module setup."""

import os

from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))
version_file = os.path.join(dir_path, "mindee", "version")
with open(version_file, "r", encoding="utf-8") as file_p:
    __version__ = file_p.read().strip()

setup(
    version=__version__,
)
