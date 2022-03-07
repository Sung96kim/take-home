#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="take_home",
    version="0.1",
    description="indico takehome",
    author="sungkim96@gmail.com",
    author_email="sungkim96@gmail.com",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "fastapi",
        "alembic"
    ],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
)