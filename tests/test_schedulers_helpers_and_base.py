import pytest

import flashcards_core
from flashcards_core.errors import ObjectNotFoundException
from flashcards_core.database import Deck
from flashcards_core.schedulers import (
    get_available_schedulers,
    get_scheduler_class,
    get_scheduler_for_deck,
)
from flashcards_core.schedulers.base import BaseScheduler


class FakeScheduler(BaseScheduler):

    def __init__(self, *args, **kwargs):
        pass

    def next_card(self):
        pass

    def process_test_result(self, card, result):
        pass


@pytest.fixture()
def fake_schedulers(monkeypatch):
    fake_schedulers = {"test": FakeScheduler}
    monkeypatch.setattr(flashcards_core.schedulers, "SCHEDULERS", fake_schedulers)
    return fake_schedulers


def test_get_available_schedulers(fake_schedulers):
    assert get_available_schedulers() == fake_schedulers.keys()


def test_get_scheduler_class(fake_schedulers):
    assert get_scheduler_class("test") == FakeScheduler


def test_get_scheduler_class_non_existing_algorithm(fake_schedulers):
    with pytest.raises(ObjectNotFoundException):
        get_scheduler_class("wrong")


def test_get_scheduler_for_deck(session, fake_schedulers):
    deck = Deck.create(session=session, name="a", description="a", algorithm="test")
    assert get_scheduler_for_deck(session=session, deck=deck).__class__ == FakeScheduler


def test_get_scheduler_for_deck_non_existing_algorithm(session, fake_schedulers):
    deck = Deck.create(session=session, name="a", description="a", algorithm="wrong")
    with pytest.raises(ObjectNotFoundException):
        get_scheduler_for_deck(session=session, deck=deck)


def test_base_scheduler_is_abstract(session, monkeypatch):
    fake_schedulers = {"base": BaseScheduler}
    monkeypatch.setattr(flashcards_core.schedulers, "SCHEDULERS", fake_schedulers)

    deck = Deck.create(session=session, name="a", description="a", algorithm="base")
    with pytest.raises(TypeError, match="anstract class BaseScheduler"):
        get_scheduler_for_deck(session=session, deck=deck)

