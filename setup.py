import os
from setuptools import setup, find_packages

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name="encodingcom-py3",
    version="0.0.5",
    description="Python 3 wrapper for Encoding.com api",
    license="",
    keywords="encoding.com transcoding",
    url="https://github.com/studionowinc/encodingcom-py3",
    zip_safe=False,
    author="Ryan Stubblefield, David Hwu",
    author_email="pypi@studionow.com",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.examples", "example*"]),
    long_description='Encoding.com service handling (c) StudioNow 2015',
    include_package_data=True,
    install_requires=[
    ],
    data_files = ['README.md'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3"
    ],
)
