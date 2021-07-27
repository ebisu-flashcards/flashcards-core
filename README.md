# Flashcards Core

[![Unit Tests](https://github.com/ebisu-flashcards/flashcards-core/actions/workflows/tests.yml/badge.svg)](https://github.com/ebisu-flashcards/flashcards-core/actions/workflows/tests.yml)  [![CodeQL](https://github.com/ebisu-flashcards/flashcards-core/actions/workflows/codeql.yml/badge.svg)](https://github.com/ebisu-flashcards/flashcards-core/actions/workflows/codeql.yml)  [![Coverage Status](https://coveralls.io/repos/github/ebisu-flashcards/flashcards-core/badge.svg?branch=main)](https://coveralls.io/github/ebisu-flashcards/flashcards-core?branch=main)  ![Profile View Counter](https://komarev.com/ghpvc/?username=flashcards-core)  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)   <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>  

Python library for flashcards and spaced repetition applications.

## Intro

### Flashcards & SRS (Spaced Repetition Software)

Flashcards are a great way to memorize large amount of facts, for example a foreign language vocabulary, the world's flags, some trivia, bird songs, your new colleagues names, or any other long list of item pairs, be that text, images, or sounds.

What makes flashcards so powerful is the possibility to review them as soon as they start to get forgotten thanks to spaced repetition algorithms (SRS), which are designed to propose you study session of optimal lenght and timing, so that you can study the least while achieving the most. Some popular algorithms include Anki's SM2, SuperMemo's algorithms, Duolingo's algorithm, and other simpler ones. Flashcards supports also very trivial schedulers like "random order" or "last seen first", etc. If you know how to write Python, you can also write your own scheduler and send it to us to add it to the library! See the "Contribute" section below to understand how to do it.

SRS algorithms have a noticeable impact on the short term learning rate, but their greatest benefits are seen on the long term, as many studies already display.

(Note to self: **add some references to back up these claims**)

### Library Structure

Flashcards is made of two main components:

- **Database model**, of a collection of flashcards decks. It includes extra features like tags and context for questions and answers. 
- **Schedulers**, algorithms that can be used to decide in which order the flashcards should be studied

In addition, it provides a simple **Study API**, an object that can be initialized and used to study existing collections through a single function call (see [the docs](https://ebisu-flashcards.github.io/flashcards-core/study.html)).

You can see the various parts of the library in mode detail by [checking out the docs](https://ebisu-flashcards.github.io/flashcards-core/).

Note that this is a library, not a complete application! This package provides no interface whatsoever and can be used only through the Python REPL or other Python scripts. If you're looking for a flashcards application, check out [Flashcards Web](https://github.com/ebisu-flashcards/flashcards-web), [Flashcards CLI](https://github.com/ebisu-flashcards/flashcards-cli), or make your own frontend.

### Versioning

This library is in development and might still experience radical changes from version to version. Do not assume backwards compatibility between minor versions until we hit version 1.0.

## Install

Flashcards can be installed from this repo as follows:

```bash
> git clone git+https://github.com/ebisu-flashcards/flashcards-core.git
> cd flashcards-core/
> python3 -m venv venv
> source venv/bin/activate
> pip install .
```

Or from PyPi (**not yet, soon!**):

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install flashcards
```

## Contribute

Contributions are welcome here! To get started, install an editable version of this package:

```bash
> git clone git+https://github.com/ebisu-flashcards/flashcards-core.git
> cd flashcards-core/
> python3 -m venv venv
> source venv/bin/activate
> pip install --editable .
> pre-commit install

... do your changes ...

> pytest
```

The pre-commit hook runs [Black](https://black.readthedocs.io/en/stable/) and 
[Flake8](https://flake8.pycqa.org/en/latest/) with fairly standard setups. 
Do not send a PR if these checks, or the tests, are failing, but rather 
[ask for help](https://github.com/ebisu-flashcards/flashcards-core/issues/new).


## Contacts

Soon...

## Contributors

![GitHub Contributors Image](https://contrib.rocks/image?repo=ebisu-flashcards/flashcards-core)
