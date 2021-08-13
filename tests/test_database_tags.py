from flashcards_core.database import Tag


def test_tag_create(session):
    assert Tag.create(session=session, name="test")


def test_tag_get_by_name_exists(session):
    tag = Tag.create(session=session, name="test")
    assert tag == Tag.get_by_name(session=session, name="test")


def test_tag_get_by_name_doesnt_exist(session):
    assert not Tag.get_by_name(session=session, name="test")


def test_tag_repr(session):
    tag = Tag.create(session=session, name="tag")
    assert f"<Tag 'tag' (ID: {tag.id})>" == f"{tag}"
