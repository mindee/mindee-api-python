import os
import subprocess
import re
from setuptools import find_packages, setup

__version__ = None


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
GIT_URL = "https://github.com/teamMindee/python-mindee"
VERSION = get_latest_git_tag(__file__)


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
    name=f"{PACKAGE_NAME}-{VERSION}",
    version=VERSION,
    url=GIT_URL,
    packages=find_packages(),
    install_requires=make_requirements_list(),
    include_package_data=True
)