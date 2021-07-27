from flashcards_core.database import Deck, Card, Fact, Tag


def test_card_create_empty_card(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    assert Card.create(session=session, deck_id=deck.id)


def test_card_create_question_equals_answer(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    fact = Fact.create(session=session, value="A", format="a")
    assert Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )


def test_card_create_with_everything(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    question = Fact.create(session=session, value="A", format="a")
    answer = Fact.create(session=session, value="B", format="b")
    assert Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )


def test_card_assign_and_remove_tag(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    question = Fact.create(session=session, value="A", format="a")
    answer = Fact.create(session=session, value="B", format="b")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    tag = Tag.create(session=session, name="test-tag")
    assert len(card.tags) == 0
    card.assign_tag(session=session, tag_id=tag.id)
    assert len(card.tags) == 1
    card.remove_tag(session=session, tag_id=tag.id)
    assert len(card.tags) == 0


def test_card_assign_and_remove_question_contex(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    question = Fact.create(session=session, value="A", format="a")
    answer = Fact.create(session=session, value="B", format="b")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    question_context = Fact.create(session=session, value="A-context", format="a")
    assert len(card.question_context_facts) == 0
    card.assign_question_context(session=session, fact_id=question_context.id)
    assert len(card.question_context_facts) == 1
    card.remove_question_context(session=session, fact_id=question_context.id)
    assert len(card.question_context_facts) == 0


def test_card_assign_and_remove_answer_contex(session):
    deck = Deck.create(session=session, name="1", description="1", algorithm="a")
    question = Fact.create(session=session, value="A", format="a")
    answer = Fact.create(session=session, value="B", format="b")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    answer_context = Fact.create(session=session, value="A-context", format="a")
    assert len(card.answer_context_facts) == 0
    card.assign_answer_context(session=session, fact_id=answer_context.id)
    assert len(card.answer_context_facts) == 1
    card.remove_answer_context(session=session, fact_id=answer_context.id)
    assert len(card.answer_context_facts) == 0
