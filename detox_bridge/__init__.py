# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager

from . import js, node

node_global = js.Identifier("global")
detox = node_global.detox
device = node_global.device
by = node_global.by
element = node_global.element
expect = node_global.expect
waitFor = node_global.waitFor
jsawait = js.GlobalAwait


@contextmanager
def node_with_detox(*, app_path, default_timeout):
    old_cwd = os.getcwd()
    os.chdir(app_path)
    app_path = os.getcwd()  # Absolute path

    try:
        with node.start(default_timeout=default_timeout) as connection:
            connection("detox = require('{}');".format(os.path.join(app_path, "node_modules", "detox")))
            yield connection
    finally:
        os.chdir(old_cwd)
