import pytest
from drjutils.common.types.enums.mapped_enum import MappedEnum

class Color(MappedEnum):
    RED  = ("red", "r")
    BLUE = ("blue", "b")


def test_mappings():
    assert Color._ENUMS_TO_STRINGS[Color.RED] == ("red", "r")
    assert Color._STRINGS_TO_ENUMS["b"] is Color.BLUE


def test_is_valid_str():
    assert Color.is_valid_str("red")
    assert not Color.is_valid_str("green")
    assert Color.is_valid_str("r", Color.RED)
    assert not Color.is_valid_str("b", Color.RED)


def test_from_str():
    assert Color.from_str("red") is Color.RED
    with pytest.raises(ValueError):
        Color.from_str("green")
