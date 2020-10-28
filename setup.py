import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file

README = (HERE / "README.md").read_text()
# This call to setup() does all the work

setup(
    name="mindee",
    version="0.0.1",
    description="Mindee SDK repository",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/publicMindee/python-sdk",
    author="Mindee",
    author_email="contact@mindee.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["mindee"],
    include_package_data=True,
    install_requires=[]
)