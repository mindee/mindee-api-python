import os
import subprocess
import re
from setuptools import find_packages, setup
import pathlib

__version__ = None

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def get_latest_git_tag(filepath):
    try:
        return (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=os.path.dirname(filepath),
            )
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        return "no_tag_found"


APP_NAME = "mindee"
PACKAGE_NAME = "mindee"
GIT_URL = "https://github.com/publicMindee/mindee-api-python"
VERSION = "v0.1"


def make_requirements_list(file="requirements.txt", only_regular=True):
    """
    Make a list of package requirements from a requirements.txt file
    :param file: path to txt file
    :param only_regular: remove rows with /, #, space or empty
    :return:
    """

    with open(file) as f:
        lines = f.read().splitlines()
    if only_regular:
        regex = (
            "\/$|^#|^$$|^git\+"
        )  # remove line with /, starting by # or space or empty
        return [line for line in lines if not re.findall(regex, line)]
    else:
        return lines


setup(
    name=f"{PACKAGE_NAME}",
    version=VERSION,
    long_description_content_type="text/markdown",
    url=GIT_URL,
    long_description=README,
    packages=find_packages(),
    install_requires=make_requirements_list(),
    include_package_data=True
)