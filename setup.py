#!/usr/bin/env python
import os

from setuptools import setup

setup(
    name="Cardz",
    description="A Basic Deck of Cards Game. LogMeIn assignment.",
    author="Francois Drolet",
    author_email="francoisd@pobox.com",
    packages=["cardz"],
    install_requires=["gunicorn>=20.0.4,<21", "Flask>=1.1.2,<2"],
    extras_require={
        "dev": [
            "black",
        ]
    },
)
