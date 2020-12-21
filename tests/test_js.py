from collections import OrderedDict

from pytest import raises

from detox_bridge.js import Call, GlobalAwait, Identifier, ObjectProperty, Operators
from detox_bridge.node import NodeError


def test_operators_raises_attribute_error_for_underscore_methods_that_are_not_supported():
    with raises(AttributeError):
        Operators().__getitem__


def test_operators_returns_object_property_on_attribute_access():
    assert type(Operators().bla) == ObjectProperty


def test_operators_returns_call_when_calling():
    assert type(Operators()()) == Call


def test_identifier():
    assert str(Identifier("g")) == "g"


def test_identifier_call_0_args():
    assert str(Identifier("g")()) == "g()"


def test_identifier_call_1_arg_with_string():
    assert str(Identifier("g")("string")) == """g("string")"""


def test_identifier_call_2_args_with_string_and_int():
    assert str(Identifier("g")("string", 123)) == """g("string", 123)"""


def test_identifier_call_1_arg_with_object():
    assert str(Identifier("g")(Identifier("other"), 123)) == """g(other, 123)"""


def test_identifier_property():
    assert str(Identifier("g").prop) == """g.prop"""


def test_identifier_property_call_with_0_args():
    assert str(Identifier("g").prop()) == """g.prop()"""


def test_identifier_property_property():
    assert str(Identifier("g").prop.prop_child) == """g.prop.prop_child"""


def test_await():
    assert (
        str(GlobalAwait(Identifier("g").some_method("hello", 1337)))
        == """return (async ()=> { return await g.some_method("hello", 1337); })()"""
    )


def test_call_encodes_strings_with_quotes_includes_escapes():
    assert str(Call(args=['he"llo'], parent="")) == """("he\\"llo")"""


def test_call_encodes_lists():
    assert str(Call(args=[["item1", "item2"]], parent="")) == """(["item1", "item2"])"""


def test_call_encodes_dicts():
    assert str(Call(args=[{"key1": "item1", "key2": "item2"}], parent="")) == """({"key1": "item1", "key2": "item2"})"""


def test_call_encodes_ordereddict():
    assert (
        str(Call(args=[OrderedDict({"key1": "item1", "key2": "item2"})], parent=""))
        == """({"key1": "item1", "key2": "item2"})"""
    )


def test_call_encodes_dicts_with_escapes_keys():
    assert str(Call(args=[{"key\\1": "item1"}], parent="")) == r"""({"key\\1": "item1"})"""


def test_call_encodes_dicts_with_values_doing_calls():
    assert (
        str(Call(args=[{"key": Call(args=["second", 123], parent="")}], parent="")) == r"""({"key": ("second", 123)})"""
    )


def test_call_encodes_lists_with_values_doing_calls():
    assert str(Call(args=[[Call(args=["second", 123], parent="")]], parent="")) == r"""([("second", 123)])"""


def test_call_encodes_none_to_null():
    assert str(Call(args=[None], parent="")) == r"""(null)"""


def test_value_error_if_encoding_is_broken():
    with raises(ValueError):
        str(Call(args=[object()], parent=""))


def test_property_works_with_node(node_server):
    node_server("property = 4")
    assert node_server("return {}".format(Identifier("property"))) == 4


def test_property_is_a_global_property(node_server):
    node_server("property = 4")
    assert node_server("return {}".format(Identifier("global").property)) == 4


def test_function_works_with_node(node_server):
    node_server("add = (x, y) => (x+y);")
    assert node_server("return {}".format(Identifier("add")(3, 4))) == 7


def test_calling_function_with_dict_with_node(node_server):
    node_server("id = (x) => (x);")
    assert node_server("return {}".format(Identifier("id")({"hello": 1, "world": 2}))) == {"hello": 1, "world": 2}


def test_calling_function_with_list_with_node(node_server):
    node_server("id = (x) => (x);")
    assert node_server("return {}".format(Identifier("id")(["hello", 1, "world", 2]))) == ["hello", 1, "world", 2]


def test_access_property_of_result_of_function(node_server):
    node_server("id = (x) => (x);")
    assert node_server("return {}".format(Identifier("id")({"hello": 1}).hello)) == 1


def test_require_function_is_available(node_server):
    node_server("{} = {}".format(Identifier("readline"), Call(args=["readline"], parent="require")))
    assert node_server("return readline") is not None


def test_identifier_await_is_able_to_set_result(node_server):
    node_server("async_func = async (x) => { global.x = x };")
    node_server(GlobalAwait(Identifier("async_func")(1)))
    assert node_server("return global.x") == 1


def test_identifier_await_propagates_exceptions(node_server):
    with raises(NodeError) as excinfo:
        node_server("async_func = async () => { throw new Error('hello'); };")
        node_server(GlobalAwait(Identifier("async_func")()))
        node_server("throw new Error('hello')", timeout=5)
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack


def test_identifier_await_propagates_promise_rejection_as_exception(node_server):
    with raises(NodeError) as excinfo:
        node_server("p = () => { return Promise.reject(new Error('hello')); }")
        node_server(GlobalAwait(Identifier("p")()))
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack
    with raises(NodeError) as excinfo:
        node_server("async_func = async () => { throw new Error('hello'); };")
        node_server(GlobalAwait(Identifier("async_func")()))
        node_server("throw new Error('hello')", timeout=5)
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack
