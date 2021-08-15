from typing import Any, Mapping

import json
import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from flashcards_core.database import Base


def import_from_json(session: Session, json_string: str, **json_kwargs) -> None:
    """
    Import the objects from their JSON representation.
    Simple wrapper around `import_from_dict()`.

    :param session: the session (see flashcards_core.database:init_session()).
    :param json_string: the string containing the data of the objects to import.
        It should have been created with `export_to_json()`
        or match the same schema.
    :param json_kwargs: any parameter you may wish to pass to `json.loads()`
    """
    hierarchy = json.loads(json_string, **json_kwargs)
    return import_from_dict(session=session, hierarchy=hierarchy)


def import_from_dict(  # noqa: C901
    session: Session, hierarchy: Mapping[str, Any], stop_on_error=False
) -> None:
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
            'decktags': {
                (1, 1),
                (1, 2)
            }
        }

    :param session: the session (see flashcards_core.database:init_session()).
    :param hierarchy: a dictionary containing all the data of the objects to import.
        See above or `export_to_dict()` for more info.
    :param stop_on_error: if an Integrity error is raised, stop instead of
        skipping the object.
    :returns: None
    """
    for tablename, entities in hierarchy.items():

        # Find the relevant table
        table = Base.metadata.tables.get(tablename)
        if table is None:
            message = (
                "The hierarchy contains a key that does not "
                f"correspond to any know table: '{tablename}'. "
            )
            if stop_on_error:
                raise ValueError(message)
            else:
                logging.error(message)
                continue

        logging.debug(f"Importing into {tablename}...")

        if isinstance(entities, dict):
            for index, values in entities.items():
                try:
                    logging.debug(f"Importing {index}: {values}")
                    uuid = UUID(index)
                    insert = table.insert().values(id=uuid, **values)
                    session.execute(insert)
                except IntegrityError as e:
                    if stop_on_error:
                        raise e
                    logging.error(
                        f"Cannot import object with id {index} in table "
                        f"{tablename}: the object either exists already "
                        "in this database, or it's malformed."
                    )

        elif isinstance(entities, list):
            for values in entities:
                try:
                    logging.debug(f"Importing {values}")
                    insert = table.insert().values(values)
                    session.execute(insert)
                except IntegrityError as e:
                    if stop_on_error:
                        raise e
                    logging.error(
                        f"Cannot import row '{values}' in table "
                        f"{tablename}: the object either exists already "
                        "in this database, or it's malformed."
                    )
        else:
            if stop_on_error:
                raise ValueError(
                    f"Table '{tablename}' is malformed: "
                    "it's neither a dict nor a list."
                )
            logging.error(f"Table '{tablename}' is malformed. Skipping")
