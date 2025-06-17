"""
# sentinel.py

## drjutils.common.types.sentinel

### Summary

Utility helpers for “argument omitted” handling.

### Sentinel

`UNSET` is a sentinel value used to indicate that an argument was not provided.
It is used to differentiate between an argument that was explicitly set to `None` and one that was
not provided at all.

### Type Aliases

-   `Opt`:       Type alias for a value that can be of type `_T` or the sentinel `UNSET`.
-   `OptOrNone`: Type alias for a value that can be of type `_T`, the sentinel `UNSET`, or `None`.
-   `OrNone`:    Type alias for a value that can be of type `_T` or `None`.

### Methods

-   `default_factory`: Always calls a factory function to create a default value, even if the
    argument is not `UNSET`.
-   `require`:         Returns the value unless it is `UNSET`, in which case it raises a
    `TypeError`.
-   `resolve`:         Returns the value unless it is `UNSET`, in which case it returns a default
    value or calls a factory function.
"""


# -----------------------------------------------------------------------------
# Standard Libraries
# -----------------------------------------------------------------------------
from __future__ import annotations # Allow forward references in type hints

# Provides type hints and type variables
from typing     import (
    Callable,
    final,
    Final,
    overload,
    TypeAlias,
    TypeVar,
    ParamSpec
    )

__all__ = [
    # Sentinel
    "UNSET",
    # Type Aliases
    "Opt",
    "OptOrNone",
    "OrNone",
    # Helper Functions
    "default_factory",
    "require",
    "resolve",
]

# -----------------------------------------------------------------------------
# Sentinel
# -----------------------------------------------------------------------------
@final
class _UnsetType:
    """
    Sentinel value Type class.add()

    This class ensures that the `UNSET` value is of a unique type,
    which ensures that the methods that it is used in can maintain their type signatures.
    """
    __slots__ = ()

    def __repr__(self) -> str: return "UNSET"

    def __init_subclass__(cls, *a, **k):
        raise TypeError("UNSET may not be subclassed")

UNSET: Final = _UnsetType()
"""
Sentinel value to indicate that an argument was not provided.

This is used to differentiate between an argument that was explicitly set to `None`
and one that was not provided at all.

See also: `require`, `resolve` for methods that make the use of this sentinel more convenient.
"""


# -----------------------------------------------------------------------------
# Generics
# -----------------------------------------------------------------------------
_P = ParamSpec("P")
"""
Type variable for callable parameters, used in factory functions.

For passthrough factory signatures.
"""

_R = TypeVar("R")
"""Type variable for generic return values."""

_T = TypeVar("T")
"""Type variable for generic objects."""

# -----------------------------------------------------------------------------
# Type Aliases
# -----------------------------------------------------------------------------
Opt:       TypeAlias = _T | _UnsetType
"""Optional type alias for a value that can be of type `_T` or the sentinel `UNSET`."""

OptOrNone: TypeAlias = _T | _UnsetType | None
"""Optional type alias for a value that can be of type `_T`, the sentinel `UNSET`, or `None`."""

OrNone:    TypeAlias = _T | None
"""Optional type alias for a value that can be of type `_T` or `None`."""

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def default_factory(
    factory:  Callable[_P, _R],
    *args:    _P.args,
    **kwargs: _P.kwargs
    ) -> _R:
    """
    Always call `factory`, sugar for `factory(*args, **kwargs)`.

    This is useful for default values that should always be computed,
    even if the argument is not `UNSET`.

    Args:
        factory:  Callable to create a default value
        *args:    Positional arguments to pass to the `factory`
        **kwargs: Keyword arguments to pass to the `factory`

    Returns:
        The result of calling the factory with the provided arguments
    """
    return factory(*args, **kwargs)

def require(
        value: Opt[_T] = UNSET,
        name:  str    = "Argument"
        ) -> _T:
    """
    Return *value* or raise `TypeError` if it is `UNSET`.

    This is useful when the caller does not necessarily need a default value,
    and you can derive the value in another way.
    That method would then call a method that uses `require` to ensure
    that the derivation succeeded if the value is not provided.

    Args:
        value: Value to check, which can be of type `_T` or the sentinel `UNSET`.
        name:  Name of the argument, used in the error message if it is `UNSET`.

    Returns:
        T: The value itself if it is not `UNSET`.

    Raises:
        TypeError: If the value is `UNSET`, indicating that the argument is required.
    """
    if value is UNSET:
        raise TypeError(f"{name} is required")
    return value

# -----------------------------------------------------------------------------
# resolve
# -----------------------------------------------------------------------------
@overload
def resolve(
    value:   Opt[_T] = UNSET,
    /, *,
    default: _T
    ) -> _T: ...
"""
Return `value` unless it is `UNSET`, in which case return `default`.

Args:
    value:   Either a real value of type `_T` or the sentinel `UNSET`.
    default: Literal to use when the argument was omitted.

Returns:
    T:
        -   The value itself if it is not `UNSET`
        -   Otherwise, the `default` value
"""

@overload
def resolve(
    value:   Opt[_T] = UNSET,
    /, *,
    default: _R
    ) -> _T | _R: ...
"""
Return `value` unless it is `UNSET`, in which case return `default`.

Args:
    value:   Either a real value of type `_T` or the sentinel `UNSET`.
    default: Literal to use when the argument was omitted.

Returns:
    T:
        -   The value itself if it is not `UNSET`
    R:
        -   Otherwise, the `default` value
"""

@overload
def resolve(
    value:    Opt[_T] = UNSET,
    /,
    *args:    _P.args,
    factory:  Callable[_P, _T],
    **kwargs: _P.kwargs,
    ) -> _T: ...
"""
Return `value` unless it is `UNSET`, in which case call `factory` with `args`/`kwargs`.

Args:
    value:    Either a real value of type `_T` or the sentinel `UNSET`
    factory:  Callable to lazily create a default. Called with `args`/`kwargs`
    *args:    Positional arguments to pass to the `factory`
    **kwargs: Keyword arguments to pass to the `factory`

Returns (T):
        -   The value itself if it is not `UNSET`, otherwise
        -   the object built by the `factory`
"""

@overload
def resolve(
    value:    Opt[_T] = UNSET,
    /,
    *args:    _P.args,
    factory:  Callable[_P, _R],
    **kwargs: _P.kwargs,
    ) -> _T | _R: ...
"""
Return `value` unless it is `UNSET`, in which case call `factory` with `args`/`kwargs`.

Args:
    value   (T): Either a real value of type `_T` or the sentinel `UNSET`
    factory (R): Callable to lazily create a default. Called with `args`/`kwargs`
    *args:       Positional arguments to pass to the `factory`
    **kwargs:    Keyword arguments to pass to the `factory`

Returns:
    T: The value itself if it is not `UNSET`, otherwise
    R: The object built by the `factory`
"""

def resolve(
    value:    Opt[_T] = UNSET,
    /,
    *args:    _P.args,
    default:  OrNone[_T | _R]              = None,
    factory:  OrNone[Callable[_P, _T | _R]] = None,
    **kwargs: _P.kwargs,
) -> _T | _R:
    """
    Return `value` unless it is `UNSET`.

    In that case, return either `default` or
    call `factory` with `args`/`kwargs` depending on which is specified.

    R is usually of the same type as T, but can be different
    if you want to return a different type when the value is `UNSET`.

    Args:
        value   (T): Either a real value of type `_T` or the sentinel `UNSET`
        default (R): Literal to use when the argument was omitted.
            Mutually exclusive with `factory`
        factory (R): Callable to lazily create a default.  Called with `args`/`kwargs`.

    Returns:
        T:
            -   The value itself if it is not `UNSET`, otherwise:
        R:
            -   The default value if it is specified, otherwise:
            -   The object built by the factory
    """
    if value is not UNSET:
        return value # explicit argument wins

    if (default is None) == (factory is None): # XOR check
        raise TypeError("Either default= or factory= must be specified.")

    if default is not None:
        return default  # type: ignore[return-value]  # guard guarantees R

    return factory(*args, **kwargs)
