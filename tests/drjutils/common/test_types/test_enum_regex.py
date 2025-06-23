import pytest
from regex import compile

from drjutils.common.types.enums.enum_regex import EnumRegex

class Fruit(EnumRegex):
    APPLE  = (r"apple", r"APPLE")
    BANANA = (compile(r"banana"), r"BANANA")


def test_mappings():
    assert Fruit._ENUMS_TO_REGEXES[Fruit.APPLE][0].pattern == "apple"
    assert Fruit._ENUMS_TO_REGEXES[Fruit.BANANA][0].pattern == "banana"


def test_is_valid_str():
    assert Fruit.is_valid_str("apple")
    assert Fruit.is_valid_str("BANANA")
    assert not Fruit.is_valid_str("orange")
    assert Fruit.is_valid_str("APPLE", Fruit.APPLE)
    assert not Fruit.is_valid_str("BANANA", Fruit.APPLE)


def test_from_str():
    assert Fruit.from_str("apple") is Fruit.APPLE
    assert Fruit.from_str("BANANA") is Fruit.BANANA
    with pytest.raises(ValueError):
        Fruit.from_str("orange")
