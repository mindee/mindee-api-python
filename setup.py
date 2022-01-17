import os
import re
from setuptools import find_packages, setup

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "mindee", "version"), "r") as version_file:
    __version__ = version_file.read().strip()

with open("README.md", "r", newline="", encoding="utf-8") as fh:
    long_description = fh.read()


APP_NAME = "mindee"
PACKAGE_NAME = "mindee"
GIT_URL = "https://github.com/publicMindee/mindee-api-python"


requirements = [
    "pikepdf==4.3.1",
    "pytz==2021.3",
    "requests==2.25.1",
]

test_requirements = [
    "pytest==6.2.5",
    "pytest-cov==2.11.1",
]

dev_requirements = [
    "black==21.12b0",
    "mypy==0.931",
    "pip-tools==6.4.0",
    "pylint==2.12.2",
    "setuptools==49.2.0",
]

setup(
    python_requires=">=3.6",
    name=PACKAGE_NAME,
    description="Mindee API helper library for Python",
    version=__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=GIT_URL,
    packages=find_packages(),
    author="Mindee",
    author_email="devrel@mindee.com",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": test_requirements,
    },
    include_package_data=True,
    package_data={"mindee": ["version"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
    ],
)
