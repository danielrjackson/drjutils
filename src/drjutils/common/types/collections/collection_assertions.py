"""Collection assertion helpers."""

from collections.abc import Iterable, Mapping, Sequence
from typing import Optional, TypeVar, Union
from typing_extensions import TypeAlias, overload

__all__ = [
    "assert_not_empty",
    "assert_lengths_match",
    "assert_keys",
    "assert_values",
    "assert_contains",
    "Key",
    "Value",
    "KeyOrKeys",
    "ValueOrValues",
]

Key = TypeVar("Key")
Value = TypeVar("Value")

Keys: TypeAlias = Sequence[Key]
Values: TypeAlias = Sequence[Value]
KeyOrKeys: TypeAlias = Union[Key, Keys]
ValueOrValues: TypeAlias = Union[Value, Values]
Map = Mapping[Key, Value]


def assert_not_empty(collection: Iterable, description: Optional[str] = None) -> None:
    """Assert that *collection* is not empty."""
    description = description or type(collection).__name__
    assert collection is not None, f"The {description} must not be None."
    assert len(collection) > 0, f"The {description} must not be empty."


def assert_lengths_match(
    collection1: Iterable,
    collection2: Iterable,
    description1: Optional[str] = None,
    description2: Optional[str] = None,
) -> None:
    """Assert that two collections have the same length."""
    assert_not_empty(collection1, description1)
    assert_not_empty(collection2, description2)

    len1 = len(collection1)
    len2 = len(collection2)
    description1 = description1 or type(collection1).__name__
    description2 = description2 or type(collection2).__name__
    assert len1 == len2, (
        f"The lengths of {description1} and {description2} must match: {len1} != {len2}."
    )


def _to_sequence(value_or_values: ValueOrValues | KeyOrKeys) -> Sequence:
    if isinstance(value_or_values, (list, tuple, set, frozenset)):
        return list(value_or_values)
    return [value_or_values]


def assert_keys(
    map: Map,
    included_keys: Optional[KeyOrKeys] = None,
    excluded_keys: Optional[KeyOrKeys] = (None,),
    description: Optional[str] = None,
) -> None:
    """Assert key presence and absence in a mapping."""
    assert_not_empty(map, description)
    description = description or type(map).__name__

    if included_keys is not None:
        for key in _to_sequence(included_keys):
            assert key in map, f"The {description} must contain the key: {key!r}."

    if excluded_keys is not None:
        for key in _to_sequence(excluded_keys):
            assert key not in map, f"The {description} must not contain the key: {key!r}."


def assert_values(
    map: Map,
    included_values: Optional[ValueOrValues] = None,
    excluded_values: Optional[ValueOrValues] = (None,),
    description: Optional[str] = None,
) -> None:
    """Assert value presence and absence in a mapping."""
    assert_not_empty(map, description)
    description = description or type(map).__name__

    if included_values is not None:
        for value in _to_sequence(included_values):
            assert value in map.values(), (
                f"The {description} must contain the value: {value!r}."
            )

    if excluded_values is not None:
        for value in _to_sequence(excluded_values):
            assert value not in map.values(), (
                f"The {description} must not contain the value: {value!r}."
            )


@overload
def assert_contains(map: Map, keys: Key, description: Optional[str] = None) -> None:
    ...


@overload
def assert_contains(map: Map, keys: Keys, description: Optional[str] = None) -> None:
    ...


def assert_contains(map: Map, keys: KeyOrKeys, description: Optional[str] = None) -> None:
    """Assert that *map* contains *keys*."""
    assert_not_empty(map, description)
    if isinstance(keys, (list, tuple, set, frozenset)):
        keys_to_check = keys
    else:
        keys_to_check = [keys]

    key_type = type(next(iter(map))) if map else object
    value_type = type(next(iter(map.values()))) if map else object
    description = description or f"{type(map).__name__}[{key_type!r}, {value_type!r}]"

    for key in keys_to_check:
        assert key in map, f"The {description} must contain the key: {key!r}."
