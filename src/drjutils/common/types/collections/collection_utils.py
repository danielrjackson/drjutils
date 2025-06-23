"""General collection utilities."""

from collections.abc import Iterable, Mapping, Sequence
from typing import Collection, Hashable, Optional, TypeVar, Union
from typing_extensions import TypeAlias

from ..type_checks import (
    T,
    set_name,
    set_name_if,
    set_docstring,
    set_docstring_if,
    set_name_and_doc,
    set_name_and_doc_if,
)

__all__ = [
    "Many",
    "OneOrMany",
    "ValueOrValues",
    "Keys",
    "KeyOrKeys",
    "is_empty",
    "is_not_empty",
    "check_empty",
    "check_not_empty",
    "get_element_type",
    "get_key_type",
    "get_value_type",
    "maybe_set_name",
    "set_name",
    "set_name_if",
    "set_docstring",
    "set_docstring_if",
    "set_name_and_doc",
    "set_name_and_doc_if",
]

Many: TypeAlias = Collection[T]
OneOrMany: TypeAlias = Union[T, Many[T]]
ValueOrValues: TypeAlias = OneOrMany[T]

Key = TypeVar("Key", bound=Hashable)
Keys: TypeAlias = Sequence[Key]
KeyOrKeys: TypeAlias = Union[Key, Keys]

Map = Mapping[Key, T]


def _get_description(obj: object, description: Optional[str] = None) -> str:
    return description or type(obj).__name__


def maybe_set_name(obj: T, name: Optional[str] = None) -> T:
    if hasattr(obj, "__name__") and name is not None:
        obj.__name__ = name
    return obj


def _check_collection(iterable: Iterable, description: Optional[str] = None) -> str:
    description = _get_description(iterable, description)
    if iterable is None:
        raise ValueError(f"The {description} must not be None.")
    if not isinstance(iterable, Iterable):
        raise TypeError(
            f"The {description} must be an iterable collection, not {type(iterable).__name__}."
        )
    return description


def is_empty(iterable: Iterable, description: Optional[str] = None) -> bool:
    _check_collection(iterable, description)
    return len(iterable) == 0


def is_not_empty(iterable: Iterable, description: Optional[str] = None) -> bool:
    _check_collection(iterable, description)
    return len(iterable) > 0


def check_empty(iterable: Iterable, description: Optional[str] = None) -> Iterable:
    description = _check_collection(iterable, description)
    if len(iterable) > 0:
        raise ValueError(
            f"The {description} must be empty, but it contains {len(iterable)} elements."
        )
    return iterable


def check_not_empty(iterable: Iterable, description: Optional[str] = None) -> Iterable:
    description = _check_collection(iterable, description)
    if len(iterable) == 0:
        raise ValueError(f"The {description} must not be empty.")
    return iterable


def get_element_type(iterable: Iterable, description: Optional[str] = None) -> type | None:
    description = _check_collection(iterable, description)
    iterator = iter(iterable)
    for element in iterator:
        if element is not None:
            return type(element)
    return None


def get_key_type(map: Map, description: Optional[str] = None) -> type | None:
    description = description or type(map).__name__
    if map is None:
        raise ValueError(f"The {description} must not be None.")
    if not isinstance(map, Mapping):
        raise TypeError(f"The {description} must be a mapping, not {type(map).__name__}.")
    for key in map.keys():
        if key is not None:
            return type(key)
    return None


def get_value_type(map: Map, description: Optional[str] = None) -> type | None:
    description = description or type(map).__name__
    if map is None:
        raise ValueError(f"The {description} must not be None.")
    if not isinstance(map, Mapping):
        raise TypeError(f"The {description} must be a mapping, not {type(map).__name__}.")
    for value in map.values():
        if value is not None:
            return type(value)
    return None
