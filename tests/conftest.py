from os import chdir, getcwd

from pytest import fixture

from detox_bridge import node


@fixture
def node_environment(tmpdir):
    old = getcwd()
    chdir(str(tmpdir))
    open(".nvmrc", "w").write("v15.2.1")
    yield node
    chdir(old)


@fixture
def node_server(node_environment):
    with node.start() as connection:
        yield connection
