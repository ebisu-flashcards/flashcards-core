from flashcards_core.database import Deck, Card, Review, Tag


def test_deck_create_minimum(session):
    assert Deck.create(
        session=session,
        name="Test2",
        description="A long description for deck - b",
        algorithm="random",
    )


def test_deck_create_with_everything(session):
    assert Deck.create(
        session=session,
        name="Test2",
        description="A long description for deck - b",
        algorithm="random",
        parameters={"param1": "test1"},
        state={"param2": "test2"},
    )


def test_deck_create_one_and_get_by_name(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    assert deck == Deck.get_by_name(session=session, name=deck.name)


def test_deck_create_many_and_get_by_name(session):
    Deck.create(
        session=session,
        name="Test1",
        description="A long description for deck - a",
        algorithm="random",
    )
    deck = Deck.create(
        session=session,
        name="Test2",
        description="A long description for deck - b",
        algorithm="random",
    )
    Deck.create(
        session=session,
        name="Test3",
        description="A long description for deck - c",
        algorithm="random",
    )
    assert deck == Deck.get_by_name(session=session, name=deck.name)


def test_deck_get_by_name_not_created(session):
    assert not Deck.get_by_name(session=session, name="TestNotExisting")


def test_deck_unseen_cards_number_no_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    for i in range(3):
        Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
    assert deck.unseen_cards_number() == 3


def test_deck_unseen_cards_number_some_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    for i in range(5):
        card = Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
        if i % 2 == 0:
            Review.create(session=session, result=True, card_id=card.id)
    assert deck.unseen_cards_number() == 2


def test_deck_unseen_cards_number_all_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    for i in range(3):
        card = Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
        Review.create(session=session, result=True, card_id=card.id)
    assert deck.unseen_cards_number() == 0


def test_deck_unseen_cards_list_no_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    cards = []
    for i in range(3):
        cards.append(
            Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
        )
    assert deck.unseen_cards_list() == cards


def test_deck_unseen_cards_list_some_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    cards = []
    for i in range(5):
        card = Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
        if i % 2 == 0:
            Review.create(session=session, result=True, card_id=card.id)
        else:
            cards.append(card)
    assert deck.unseen_cards_list() == cards


def test_deck_unseen_cards_list_all_cards_have_reviews(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    for i in range(3):
        card = Card.create(session=session, deck_id=deck.id, question_id=1, answer_id=2)
        Review.create(session=session, result=True, card_id=card.id)
    assert deck.unseen_cards_list() == []


def test_deck_assign_tag(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    tag = Tag.create(session=session, name="test-tag")
    assert len(deck.tags) == 0
    deck.assign_tag(session=session, tag_id=tag.id)
    assert len(deck.tags) == 1


def test_deck_assign_and_remove_tag(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for the deck",
        algorithm="random",
    )
    tag = Tag.create(session=session, name="test-tag")
    assert len(deck.tags) == 0
    deck.assign_tag(session=session, tag_id=tag.id)
    assert len(deck.tags) == 1
    deck.remove_tag(session=session, tag_id=tag.id)
    assert len(deck.tags) == 0
