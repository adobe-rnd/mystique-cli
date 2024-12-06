from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mystique-cli",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mystique=app.app:main",
        ],
    },
    install_requires=requirements,
    description="A command-line tool for building EDS website using Gen AI",
    author="Vitaly Tsaplin",
)
