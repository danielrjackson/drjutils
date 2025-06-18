from drjutils.common.types.type_debugging import (
    set_debug_name,
    set_debug_context,
    set_debug_name_and_context,
)

class Dummy:
    pass


def test_debug_helpers():
    obj = Dummy()
    set_debug_name(obj, "name", True)
    assert obj._debug_name == "name"

    set_debug_context(obj, "ctx", True)
    assert obj._debug_context == "ctx"

    obj2 = Dummy()
    ret = set_debug_name_and_context(obj2, debug_name="dn", context="cx", condition=True)
    assert obj2._debug_name == "dn"
    assert obj2._debug_context == "cx"
    assert ret is obj2

