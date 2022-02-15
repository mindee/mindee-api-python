import os
from setuptools import find_packages, setup

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "mindee", "version"), "r") as version_file:
    __version__ = version_file.read().strip()

with open("README.md", "r", newline="", encoding="utf-8") as fh:
    long_description = fh.read()


requirements = [
    "pikepdf==4.5.0",
    "pytz==2021.3",
    "requests==2.25.1",
]

test_requirements = [
    "pytest==6.2.5",
    "pytest-cov==2.12.1",
]

dev_requirements = [
    "black==22.1.0",
    "mypy==0.931",
    "pip-tools==6.4.0",
    "pylint==2.12.2",
    "setuptools==49.6.0",
]

setup(
    python_requires=">=3.7",
    name="mindee",
    description="Mindee API helper library for Python",
    version=__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mindee.com/",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Documentation": "https://developers.mindee.com/docs/python-sdk",
        "Source": "https://github.com/publicMindee/mindee-api-python",
    },
)
