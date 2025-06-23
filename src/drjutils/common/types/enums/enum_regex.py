"""
# enum_regex.py

## drjutils.common.types.enums.enum_regex

Base class for enums that map regex patterns to enum members.

This class is similar to :class:`MappedEnum` but uses regular
expressions to associate strings with enum members. Each enum value is
created with one or more regex patterns. The first pattern's string is
used as the display value for the enum member.

The regex patterns are compiled using the :mod:`regex` library.
"""

from enum import Enum
from regex import Pattern, compile
from typing import Self, Tuple, Optional

__all__ = ["EnumRegex"]


class EnumRegex(Enum):
    """Enum members backed by regex pattern matches."""

    _ENUMS_TO_REGEXES: dict[Self, Tuple[Pattern[str], ...]]

    def __new__(cls, *patterns: str | Pattern[str]) -> Self:
        if not patterns:
            raise ValueError("EnumRegex members require at least one pattern")

        compiled = []
        for pat in patterns:
            compiled.append(compile(pat) if isinstance(pat, str) else pat)

        obj = object.__new__(cls)
        obj._value_ = compiled[0].pattern
        obj._regexes = tuple(compiled)
        obj._display_ = obj._value_
        return obj

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return self._display_

    def get_regexes(self) -> Tuple[Pattern[str], ...]:
        """Return the compiled regex patterns for this enum member."""
        return self._regexes

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._ENUMS_TO_REGEXES = {}
        cls._PATTERNS_TO_ENUMS: dict[str, Self] = {}

        for member in cls:  # type: ignore[assignment]
            regexes = member._regexes  # type: ignore[attr-defined]
            cls._ENUMS_TO_REGEXES[member] = regexes
            for rx in regexes:
                pat = rx.pattern
                if pat in cls._PATTERNS_TO_ENUMS:
                    prev = cls._PATTERNS_TO_ENUMS[pat]
                    raise ValueError(
                        f"Duplicate pattern {pat!r} for {prev!r} and {member!r}"
                    )
                cls._PATTERNS_TO_ENUMS[pat] = member

    @classmethod
    def is_valid_str(cls, string: str, self: Optional[Self] = None) -> bool:
        """Return ``True`` if the string matches an enum pattern."""
        if self is None:
            for regexes in cls._ENUMS_TO_REGEXES.values():
                for rx in regexes:
                    if rx.fullmatch(string):
                        return True
            return False
        for rx in cls._ENUMS_TO_REGEXES[self]:
            if rx.fullmatch(string):
                return True
        return False

    @classmethod
    def maybe_from_str(cls, string: str) -> Optional[Self]:
        """Return the matching enum member if any."""
        for member, regexes in cls._ENUMS_TO_REGEXES.items():
            for rx in regexes:
                if rx.fullmatch(string):
                    return member
        return None

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Convert a string to an enum member or raise ``ValueError``."""
        result = cls.maybe_from_str(string)
        if result is None:
            raise ValueError(f"Invalid value: {string}")
        return result
