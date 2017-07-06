from detox_bridge import js, node
from pytest import raises


def test_node_which_pick_up_installed_node(node_environment):
    assert node_environment.which().endswith("v7.6.0/bin/node")


def test_node_server_responds_with_a_timeout_error_if_code_executioin_takes_too_long(node_server):
    with raises(node.TimeoutError):
        node_server("while(true);", timeout=1)


def test_node_server_executes_code_keeping_global_state(node_server):
    assert node_server("global.b=1+3; return global.b;", timeout=5) == 4
    assert node_server("return global.b;", timeout=5) == 4


def test_node_server_executes_code_without_return(node_server):
    assert node_server("global.b=1+3;", timeout=5) is None
    assert node_server("return global.b;", timeout=5) == 4


def test_node_server_executes_uses_str_if_object_is_JSObject(node_server):
    node_server(js.Identifier("global").b, timeout=5)


def test_node_server_executes_code_reporting_exceptions(node_server):
    with raises(node.NodeError) as excinfo:
        node_server("throw new Error('hello')", timeout=5)
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack
