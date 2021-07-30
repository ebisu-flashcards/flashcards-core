from flashcards_core.database import Tag


def test_tag_create(session):
    assert Tag.create(session=session, name="test")


def test_tag_repr(session):
    tag = Tag.create(session=session, name="tag")
    assert f"<Tag 'tag' (ID: {tag.id})>" == f"{tag}"
