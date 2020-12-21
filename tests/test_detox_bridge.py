import os

from pytest import fixture, mark, raises

from detox_bridge import by, detox, device, element, expect, jsawait, node, node_with_detox, waitFor


@fixture(scope="session")
def detox_node_server():
    cwd = os.getcwd()
    try:
        os.chdir("./example")
        app_path = os.getcwd()
        with node_with_detox(app_path=app_path, default_timeout=10) as connection:
            yield connection
    finally:
        os.chdir(cwd)


@fixture(scope="session")
def detox_server(detox_node_server):
    ios_sim_release = {
        "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/example.app",
        "type": "ios.simulator",
        "device": {"type": "iPhone 11"},
    }
    configurations_obj = {
        "configurations": {"ios.sim.release": ios_sim_release},
        "selectedConfiguration": "ios.sim.release",
    }
    detox_node_server(jsawait(detox.init(configurations_obj)), timeout=360)
    yield detox_node_server
    detox_node_server(jsawait(detox.cleanup()))


@fixture
def app_server(detox_server):
    detox_server(jsawait(device.reloadReactNative()))
    yield detox_server


def test_detox_init_launches_app_reloads_and_cleanup_runs(app_server):
    pass


def test_welcome_screen_is_displayed(app_server):
    app_server(jsawait(expect(element(by.id("welcome"))).toBeVisible()))


def test_should_show_hello_after_tap(app_server):
    app_server(jsawait(element(by.id("hello_button")).tap()))
    app_server(jsawait(expect(element(by.label("Hello!!!"))).toBeVisible()))


def test_should_show_world_after_tap(app_server):
    app_server(jsawait(element(by.id("world_button")).tap()))
    app_server(jsawait(expect(element(by.label("World!!!"))).toBeVisible()))


def test_should_waitFor_passes_when_element_is_visible(app_server):
    app_server(jsawait(waitFor(element(by.id("world_button"))).toBeVisible().withTimeout(2000)))


@mark.skip(reason="not clear if this expectation is as per spec. question to wix is pending")
def test_should_waitFor_passes_when_element_is_not_visible_it_fails(app_server):
    with raises(node.NodeError):
        app_server(jsawait(waitFor(element(by.id("notthere"))).toBeVisible().withTimeout(2000)))


def test_should_raise_exception_after_tap_since_expectation_hasnt_been_met(app_server):
    app_server(jsawait(element(by.id("world_button")).tap()))
    with raises(node.NodeError):
        app_server(jsawait(expect(element(by.label("NotVisible!!!"))).toBeVisible()))
