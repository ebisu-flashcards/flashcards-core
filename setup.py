from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent.absolute()
with (HERE / "README.md").open("rt") as fh:
    LONG_DESCRIPTION = fh.read().strip()

setup(
    name="flashcards-core",
    version="0.0.1",
    author="Sara Zanzottera",
    author_email="",
    description="Flashcards Core",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "sqlalchemy",
        "sqlalchemy-json",
        # FIXME we could make algorithms pluggable instead of pulling them all... right?
        "ebisu",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-random-order",
            "freezegun",  # Mock datetime objects
            "pre-commit",
            "black",
            "flake8",
            "coveralls",
        ]
    },
)
