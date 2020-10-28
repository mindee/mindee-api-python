import os
import subprocess
import re
from setuptools import find_packages, setup

__version__ = None


with open("README.md", "r", newline="", encoding="utf-8") as fh:
    long_description = fh.read()


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
VERSION = "v0.3"


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
    python_requires=">=3.0",
    name=f"{PACKAGE_NAME}",
    description="Mindee API helper library for python",
    version=VERSION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=GIT_URL,
    packages=find_packages(),
    author="Mindee",
    author_email="contact@mindee.com",
    install_requires=make_requirements_list(),
    include_package_data=True
)