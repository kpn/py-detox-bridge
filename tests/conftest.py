from os import chdir, getcwd

from detox_bridge import node
from pytest import fixture


@fixture
def node_environment(tmpdir):
    old = getcwd()
    chdir(str(tmpdir))
    open(".nvmrc", "w").write("v7.6.0")
    yield node
    chdir(old)


@fixture
def node_server(node_environment):
    with node.start() as connection:
        yield connection
