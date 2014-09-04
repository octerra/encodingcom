import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="encodingcom-py3",
    version="0.0.3",
    description=("Python 3 wrapper for Encoding.com api"),
    license="",
    keywords="encoding.com transcoding",
    url="https://github.com/studionowinc/encodingcom-py3",
    author="Ryan Stubblefield",
    author_email="ryan.stubblefield@gmail.com",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.examples", "example*"]),
    long_description=read('README.md'),
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3"
    ],
)
