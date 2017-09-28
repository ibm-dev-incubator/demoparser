#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "demoparser.util",
        ["demoparser/util.pyx"]
    ),
    Extension(
        "demoparser.props",
        ["demoparser/props.pyx"]
    ),
    Extension(
        "demoparser.bitbuffer",
        ["demoparser/bitbuffer.pyx"]
    ),
    Extension(
        "demoparser.parser",
        ["demoparser/parser.pyx"]
    ),
]
setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    ext_modules=cythonize(extensions)
)
