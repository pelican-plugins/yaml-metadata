#!/usr/bin/env python

from setuptools import setup

setup(
    name="pelican-yaml-metadata",
    version="2.0.0",
    description="A Pelican plugin that parses metadata from YAML headers in markdown files",
    url="https://github.com/pR0Ps/pelican-yaml-metadata",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Pelican",
        "Framework :: Pelican :: Plugins",
        "Operating System :: OS Independent",
    ],
    packages=["pelican.plugins.yaml_metadata"],
    install_requires=[
        "pelican>=4.5,<5.0.0",
        "markdown>=3.3.4,<4.0.0",
        "pyYAML>=5.4.1,<6.0.0",
    ],
)
