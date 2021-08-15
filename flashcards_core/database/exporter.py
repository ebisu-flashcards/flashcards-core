from typing import Any, List, Mapping

import json
import logging
from uuid import UUID
from datetime import datetime, date

from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from flashcards_core.database import Base


#: Default fields not to follow for related objects discovery.
#: See `export_to_json()` for more info
DEFAULT_EXCLUDE_FIELDS = {"cards": ["deck"]}


def hierarchy_to_json(obj):
    """
    JSON serializer for objects not serializable by default, like dates, sets, UUIDs.

    This is the 'default' method of the JSON encoder, see `export_to_json`.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj.hex)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_uuids(hierarchy: Mapping[str, Any]) -> Mapping[str, Any]:
    """
    Updates all UUID keys to be strings.

    :param hierarchy: the hierarchy to normalize
    :returns: the normalized hierarchy
    """
    new_hierarchy = {}
    for key, values in hierarchy.items():

        if isinstance(values, dict):
            # Recursive call
            values = serialize_uuids(values)

        # Key update
        if isinstance(key, UUID):
            new_hierarchy[key.hex] = values
        else:
            new_hierarchy[key] = values

    return new_hierarchy


def export_to_json(
    session: Session,
    objects_to_export: List[Base],
    exclude_fields: Mapping[str, List[str]] = None,
    **json_kwargs,
) -> str:
    """
    Exports the given objects into a JSON string.
    Simple wrapper around `export_to_dict()` that performs some normalization
    (like UUIDs to string, set to list, etc...)

    :param session: the session (see flashcards_core.database:init_session()).
    :param objects_to_export: a list of objects to export. They should be
        subclasses of any class defined in `flashcards_core.database.models`.
    :param json_kwargs: any parameter you may wish to pass to `json.dumps()`
    """
    hierarchy = export_to_dict(
        session=session,
        objects_to_export=objects_to_export,
        exclude_fields=exclude_fields,
    )

    # Convert all UUID keys to strings
    logging.debug("Normalizing UUID keys into strings...")
    new_hierarchy = serialize_uuids(hierarchy)

    logging.debug("Export procedure complete, dumping data to JSON string")
    return json.dumps(new_hierarchy, default=hierarchy_to_json, **json_kwargs)


def export_to_dict(
    session: Session,
    objects_to_export: List[Base],
    exclude_fields: Mapping[str, List[str]] = None,
    _hierarchy: Mapping[str, Any] = None,
) -> Mapping[str, Any]:
    """
    Exports the given objects to a dictionary, which can be easily dumped
    into a standard format like JSON or YAML.

    Note that, by default, all relationships are followed, except for the
    following ones:

        * Exporting a Card won't export its Deck.
        * Exporting a Fact will not export the Cards it's included in.

    These default can be overridden by providing a value to the
    `exclude_fields` attribute. It expect a mapping of a tablename (like 'cards')
    and a list of string with the name of the columns that should not be checked
    for potential related objects to export.
    Its default value looks like ``{'cards': ['deck']}`` (facts don't have
    references to the cards they're included in, so you need a query to find them).

    Remember to pass an empty dictionary to `exclude_fields` to really exclude
    no fields; passing None will instruct this function to apply the
    default exclusion list.

    The list of objects to export can be a mixture of several subclasses
    of SQLAlchemy's Base class. In the output they will be categorized
    by table name.

    Example output where only one Deck object was passed:

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


    If more Decks were passed, the overall structure would be the same,
    as well as if the list was made of mixed objects.

    :param session: the session (see flashcards_core.database:init_session()).
    :param objects_to_export: a list of objects to export. They should be
        subclasses of any class defined in `flashcards_core.database.models`.
    :param exclude_fields: If any of the model object columns should not be followed,
        they should be added here. Note that these exclusions apply to all
        the objects of this type discovered by following other relationships.
        The default value is set to ``{'cards': ['deck']}`` (see above).
    :param _hierarchy: internal, used to pass the already built hierarchy through
        recursive calls.
    :returns: a definition of all the objects required to reconstruct the
        database hierarchy the objects were taken from.

    """
    logging.debug("'export_to_dict' starting.")
    logging.debug(f"Objects to export: {objects_to_export}.")
    logging.debug(f"Fields to exclude: {exclude_fields}.")

    if exclude_fields is None:
        exclude_fields = DEFAULT_EXCLUDE_FIELDS

    # In recursive calls, sometimes export_to_dict will receive single objects
    # instead of lists. It's ok, just wrap them.
    if not isinstance(objects_to_export, list):
        objects_to_export = [objects_to_export]

    # Init the hierarchy if needed
    if not _hierarchy:
        logging.debug("Creating empty hierarchy")
        _hierarchy = {}

    for item in objects_to_export:
        logging.info(f"Exporting '{item}'")

        # Broken references are represented by None objects.
        # TODO make a setting to fail or not when these are encountered.
        if item is None:
            logging.info(" -> This item is probably a broken reference, skipping.")
            continue

        entry = item.__class__.__tablename__

        # Init the hierarchy block if not found
        if entry not in _hierarchy.keys():
            logging.debug(f"Creating key '{entry}' in hierarchy.")
            _hierarchy[entry] = {}

        # Check if the object is already in the hierarchy
        if item.id.hex in _hierarchy[entry].keys():
            logging.info("Item already in the hierarchy, skipping.")
            continue

        # Add the scalar fields
        description = {
            field: value
            for field, value in vars(item).items()
            if not field.startswith("_") and field != "id"
        }
        _hierarchy[entry][item.id.hex] = description
        logging.debug(
            f"Added entry in '{entry}'. " f"Current hierarchy:\n{_hierarchy}\n"
        )

        # Discover related objects
        logging.debug("Checking for related objects...")
        _hierarchy = _export_find_related_objects(
            session=session,
            item=item,
            exclude_fields=exclude_fields,
            _hierarchy=_hierarchy,
        )

        logging.debug(
            f"Check for related objects complete: "
            f"returning the current hierarchy:\n{_hierarchy}\n"
            f"********************\n"
        )

    return _hierarchy


def _export_find_related_objects(
    session: Session,
    item: Base,
    exclude_fields: Mapping[Base, List[str]],
    _hierarchy: Mapping,
) -> Mapping:
    """
    Scans the model class structure to look for related entities, namely
    reverse ForeignKey relationships (for example `deck.cards`) and
    many-to-many relationships (for example `deck.tags`) with their
    respective associative tables.

    **INTERNAL, UNSTABLE, DON'T USE**

    :param session: the session (see flashcards_core.database:init_session()).
    :param item: the model object to inspect for related entities.
    :param exclude_fields: If any of the model object columns should not be followed,
        they should be added here. Note that these exclusions apply to all
        the objects of this type discovered by following other relationships.
        The default value is set to ``{'cards': ['deck']}`` (see `export_to_dict`).
    :param _hierarchy: the hierarchy to add the related entities to.

    :returns: the modified _hierarchy.
    """
    for field, value in vars(item.__class__).items():
        if isinstance(value, InstrumentedAttribute) and isinstance(
            value.property, RelationshipProperty
        ):
            logging.debug(f"'{field}' points to some related objects.")

            if item.__class__.__tablename__ in exclude_fields.keys():
                if field in exclude_fields[item.__class__.__tablename__]:
                    logging.debug(
                        f"'{field}' excluded by 'exclude_fields': {exclude_fields}."
                    )
                    continue

            # Get the values referenced by this relationship
            related = getattr(item, field)

            # Don't send too many None and empty lists to the recursive call...
            if related:
                number_of_objects = len(related) if isinstance(related, list) else 1
                logging.info(
                    f"{number_of_objects} objects discovered in {field}. "
                    "Adding them to the exports list."
                )
                logging.debug(f"Objects: {related}")

                # Recursive call to export the referenced objects
                # Note that we avoid circular references by checking if the object
                # is already in the hierarchy (see export_to_dict()).
                _hierarchy = export_to_dict(
                    session=session,
                    objects_to_export=related,
                    exclude_fields=exclude_fields,
                    _hierarchy=_hierarchy,
                )

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
                        _hierarchy[str(associative_table.fullname)] = set()

                    _hierarchy[str(associative_table.fullname)].add(tuple(association))
                    logging.debug(
                        f"New row to add:\n{association}\n"
                        f"Current hierarchy:\n{_hierarchy}\n"
                    )
    return _hierarchy
