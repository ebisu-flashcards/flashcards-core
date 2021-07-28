from typing import Any, List, Mapping

import json
import logging

from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from flashcards_core.database import Base


def export_to_json(
    session: Session, objects_to_export: List[Base], **json_kwargs
) -> str:
    """
    Exports the given objects into a JSON string. Simple wrapper around `export_to_dict()`.

    :param session: the session (see flashcards_core.database:init_session()).
    :param objects_to_export: a list of objects to export. They should be
        subclasses of any class defined in `flashcards_core.database.models`.
    :param json_kwargs: any parameter you may wish to pass to `json.dumps()`
    """
    hierarchy = export_to_dict(session=session, objects_to_export=objects_to_export)

    logging.debug("Export procedure complete, dumping data to JSON string")
    return json.dumps(hierarchy, **json_kwargs)


def export_to_dict(
    session: Session,
    objects_to_export: List[Base],
    _hierarchy: Mapping[str, Any] = None,
) -> Mapping[str, Any]:
    """
    Exports the given objects to a dictionary, which then can be easily dumped
    into a standard format like JSON or YAML.

    :param session: the session (see flashcards_core.database:init_session()).
    :param objects_to_export: a list of objects to export. They should be
        subclasses of any class defined in `flashcards_core.database.models`.
    :param _hierarchy: internal, used to pass the already built hierarchy through
        recursive calls.

    :returns: a definition of all the objects required to reconstruct the
        database hierarchy the objects were taken from.

        Note that this function will export hierarchies as follows:

        - Exporting Decks will export all their Cards.
        - Exporting Cards will export all their Facts and Reviews.
        - Exporting any model with Tags will export all the involved Tags.
        - Export any object involved in a many-to-many relationship with
            another entity will export all the involved entities and the
            relevant rows in the respective associative tables.

        The list of given objects can be a mixture of several subclasses
        of SQLAlchemy's Base class. In the output they will be categorized
        by table name.

        Example output where only one Deck object was passed:

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

        If more Decks were passed, the overall structure would be the same,
        as well as if the list was made of mixed objects.
    """
    logging.debug(f"'export_to_dict' starting. Objects to export: {objects_to_export}")

    if not isinstance(objects_to_export, list):
        raise ValueError(
            "You must provide a list of objects "
            "even if you want to export a single one."
        )

    # Init the hierarchy if needed
    if not _hierarchy:
        logging.debug("Creating empty hierarchy")
        _hierarchy = {}

    for item in objects_to_export:
        entry = item.__class__.__tablename__

        # Init the hierarchy block if not found
        if entry not in _hierarchy.keys():
            logging.debug(f"Creating key '{entry}' in hierarchy.")
            _hierarchy[entry] = {}

        # Check if the object is already in the hierarchy
        if item.id in _hierarchy[entry].keys():
            logging.debug("Item already in the hierarchy, skipping.")
            continue

        # Add the scalar fields
        logging.debug("Checking for related objects...")
        description = {
            field: value
            for field, value in vars(item).items()
            if not field.startswith("_") and field != "id"
        }
        _hierarchy[entry][item.id] = description
        logging.debug(
            f"Added entry in '{entry}'. " f"Current hierarchy:\n{_hierarchy}\n"
        )

        # Discover the relationships
        logging.debug("Checking for related objects...")
        _hierarchy = _export_find_related_objects(
            session=session, item=item, _hierarchy=_hierarchy
        )

        logging.debug(
            f"Check for related objects complete: "
            f"returning the current hierarchy:\n{_hierarchy}\n"
            f"********************\n"
        )

    return _hierarchy


def _export_find_related_objects(
    session: Session, item: Base, _hierarchy: Mapping
) -> Mapping:
    """
    Scans the model class structure to look for related entities, namely
    reverse ForeignKey relationships (for example `deck.cards`) and
    many-to-many relationships (for example `deck.tags`) with their
    respective associative tables.

    **INTERNAL, UNSTABLE, DON'T USE**

    :param session: the session (see flashcards_core.database:init_session()).
    :param item: the model object to inspect for related entities.
    :param _hierarchy: the hierarchy to add the related entities to.

    :returns: the modified _hierarchy.
    """
    for field, value in vars(item.__class__).items():
        if isinstance(value, InstrumentedAttribute) and isinstance(
            value.property, RelationshipProperty
        ):
            logging.debug(f"'{field}' points to some related objects.")

            # Get the values referenced by this relationship
            related_objects = getattr(item, field)
            logging.debug(f"Objects discovered: {related_objects}")

            # Recursive call to export the referenced objects
            # Note that we ignore direct ForeignKey relationships
            # (like card->deck) to avoid circular references.
            # TODO check if this ever becomes and issue; maybe
            #    for 1-to-1 relationships?
            if isinstance(related_objects, list):
                _hierarchy = export_to_dict(
                    session=session,
                    objects_to_export=related_objects,
                    _hierarchy=_hierarchy,
                )
            else:
                logging.debug("Discovered objects are not in a list, skipping.")

            # If this is a many-to-many, export the associations too
            # FIXME is there a better way to go with this?
            logging.debug("Checking for related associative tables...")
            associative_table = (
                value.property.secondary
            )  # M2M have a 'secondary' attribute
            if associative_table is not None:  # Cannot use a table as a boolean
                _hierarchy = _export_find_related_associative_tables(
                    session=session,
                    item=item,
                    associative_table=associative_table,
                    _hierarchy=_hierarchy,
                )

    return _hierarchy


def _export_find_related_associative_tables(
    session: Session, item: Base, associative_table: Table, _hierarchy: Mapping
) -> Mapping:
    """
    Given an associative table and a model object, retrieve the relevant
    rows from that table, serializes them into a dictionary, and adds them
    to the hierarchy under their own custom block named after the associative
    table itself.

    TODO: check if this whole thing could be done better.

    **INTERNAL, UNSTABLE, DON'T USE**

    :param session: the session (see flashcards_core.database:init_session()).
    :param item: the model object to inspect for related entities.
    :param associative_table: the associative table containing information on some
        many-to-many relationship in which `item` is involved.
    :param _hierarchy: the hierarchy to add the related rows to.

    :returns: the modified _hierarchy.
    """
    for column in associative_table.columns:
        for key in column.foreign_keys:
            if key.column.table.fullname == item.__class__.__tablename__:
                associations = (
                    session.query(associative_table).filter(key.column == item.id).all()
                )
                for association in associations:

                    if associative_table.fullname not in _hierarchy.keys():
                        logging.debug(
                            f"Creating key {associative_table.fullname} in hierarchy."
                        )
                        _hierarchy[associative_table.fullname] = {}

                    column_names = [
                        column.name
                        for column in associative_table.columns
                        if column.name != "id"
                    ]
                    description = dict(zip(column_names, association[1:]))
                    _hierarchy[associative_table.fullname][association[0]] = description
                    logging.debug(
                        f"New description to add:\n{description}\n"
                        f"Current hierarchy:\n{_hierarchy}\n"
                    )
    return _hierarchy
