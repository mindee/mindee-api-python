import re
from setuptools import find_packages, setup

__version__ = None


with open("README.md", "r", newline="", encoding="utf-8") as fh:
    long_description = fh.read()


APP_NAME = "mindee"
PACKAGE_NAME = "mindee"
GIT_URL = "https://github.com/publicMindee/mindee-api-python"


requirements = [
    "requests==2.23.0",
    "pytz==2021.3",
    "PyMuPDF==1.18.17",
]

test_requirements = [
    "pytest==6.1.2",
    "pytest-cov==2.11.1",
]

dev_requirements = [
    "black==21.12b0",
    "setuptools==49.2.0",
    "pip-tools==6.4.0",
]

setup(
    python_requires=">=3.0",
    name=f"{PACKAGE_NAME}",
    description="Mindee API helper library for Python",
    version="v1.2.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=GIT_URL,
    packages=find_packages(),
    author="Mindee",
    author_email="devrel@mindee.com",
    install_requires=requirements,
    test_requirements=test_requirements,
    extras_require={
        "dev": dev_requirements,
        "test": test_requirements,
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
