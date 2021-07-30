from typing import Any, Mapping

# import json
import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from flashcards_core.database import Base


# def import_from_json(session: Session, json_string: str, **json_kwargs) -> None:
#     """
#     Import the objects from their JSON representation.
#     Simple wrapper around `import_from_dict()`.

#     :param session: the session (see flashcards_core.database:init_session()).
#     :param json_string: the string containing the data of the objects to import.
#         It should have been created with `export_to_json()`
#         or match the same schema.
#     :param json_kwargs: any parameter you may wish to pass to `json.loads()`
#     """
#     hierarchy = json.loads(json_string, **json_kwargs)
#     return import_from_dict(session=session, hierarchy=hierarchy)


def import_from_dict(session: Session, hierarchy: Mapping[str, Any]) -> None:
    """
    Create objects in the database from the data contained in the dictionary.
    Note that the keys must be strings, not UUID objects.

    Example of valid input:

    .. code-block:: json

        {
            'decks': {
                1: {
                    'name': 'Test Deck',
                    'description': 'A deck for tests',
                    'algorithm': 'random',
                    'parameters': {
                        'unseen_first': true
                    },
                    'state': {
                        'last_reviewed_card': 2
                    }
                }
            },
            'cards': {
                1: {
                    'deck_id': 1,
                    'question_id': 1,
                    'answer_id': 2
                }
            },
            'facts': {
                1: {
                    'value': 'A question',
                    'format': 'text'
                },
                2: {
                    'value': 'An answer',
                    'format': 'text'
                }
            },
            'reviews': {
                1: {
                    'card_id': 1,
                    'result': True,
                    'algorithm': 'random',
                    'datetime': '2021-01-01 12:00:00'
                }
            },
            'tags': {
                1: {
                    'name': 'test-tag-1'
                },
                2: {
                    'name': 'test-tag-2'
                }
            }
            'decktags': [
                1: {
                    'deck_id': 1,
                    'tag_id': 1
                },
                2: {
                    'deck_id': 1,
                    'tag_id': 2
                }
            }
        }

    :param session: the session (see flashcards_core.database:init_session()).
    :param hierarchy: a dictionary containing all the data of the objects to import.
        See above or `export_to_dict()` for more info.
    :returns: None
    """
    for tablename, entities in hierarchy.items():

        # Find the relevant table
        table = Base.metadata.tables.get(tablename)
        if table is None:
            raise ValueError(
                "The hierarchy contains a key that does not "
                f"correspond to any know table: '{tablename}'. "
                "Remove it and try again."
            )
        logging.debug(f"Importing into {tablename}...")

        for index, values in entities.items():
            try:
                logging.debug(f"Importing {index}: {values}")
                uuid = UUID(index)
                insert = table.insert().values(id=uuid, **values)
                session.execute(insert)
            except IntegrityError:
                logging.error(
                    f"Cannot import object with id {index} in table "
                    f"{tablename}: the object either exists already "
                    "in this database, or it's malformed."
                )
