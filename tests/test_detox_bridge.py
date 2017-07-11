import os

from detox_bridge import await, by, detox, device, element, expect, node
from pytest import fixture


@fixture(scope="session")
def detox_node_server():
    cwd = os.getcwd()
    try:
        os.chdir("./detox/examples/demo-react-native")
        app_path = os.getcwd()
        with node.start(default_timeout=10) as connection:
            connection("require('{}');".format(
                os.path.join(app_path, 'node_modules', 'babel-polyfill')))
            connection("detox = require('{}');".format(
                os.path.join(app_path, 'node_modules', 'detox')))
            yield connection
    finally:
        os.chdir(cwd)


@fixture(scope="session")
def detox_server(detox_node_server):
    ios_sim_release = {
        "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/example.app",
        "type": "ios.simulator",
        "name": "iPhone 7 Plus"
    }
    configurations_obj = {"configurations": {"ios.sim.release": ios_sim_release}}
    detox_node_server(await(detox.init(configurations_obj)), timeout=360)
    yield detox_node_server
    detox_node_server(await(detox.cleanup()))


@fixture
def app_server(detox_server):
    print(detox_server("return Object.getOwnPropertyNames(global)"))
    detox_server(await(device.reloadReactNative()))
    yield detox_server


def test_detox_init_launches_app_reloads_and_cleanup_runs(app_server):
    pass


def test_welcome_screen_is_displayed(app_server):
    app_server(await(expect(element(by.id('welcome'))).toBeVisible()))


def test_should_show_hello_after_tap(app_server):
    app_server(await(element(by.id('hello_button')).tap()))
    app_server(await(expect(element(by.label('Hello!!!'))).toBeVisible()))


def test_should_show_world_after_tap(app_server):
    app_server(await(element(by.id('world_button')).tap()))
    app_server(await(expect(element(by.label('World!!!'))).toBeVisible()))
