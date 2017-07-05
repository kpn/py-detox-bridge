from os import chdir, getcwd

from detox_bridge import node
from pytest import fixture, raises


@fixture
def node_environment(tmpdir):
    old = getcwd()
    chdir(str(tmpdir))
    open(".nvmrc", "w").write("v7.6.0")
    yield
    chdir(old)


@fixture
def node_server(node_environment):
    with node.start() as connection:
        yield connection


def test_node_which_pick_up_installed_node(node_environment):
    assert node.which().endswith("v7.6.0/bin/node")


def test_node_server_responds_with_a_timeout_error_if_code_executioin_takes_too_long(node_server):
    with raises(node.TimeoutError):
        node_server.send("while(true);", timeout=1)


def test_node_server_executes_code_keeping_global_state(node_server):
    assert node_server.send("global.b=1+3; return global.b;", timeout=5) == {"result": 4}
    assert node_server.send("return global.b;", timeout=5) == {"result": 4}


def test_node_server_executes_code_reporting_exceptions(node_server):
    with raises(node.NodeError) as excinfo:
        node_server.send("throw new Error('hello')", timeout=5)
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack
