# -*- coding: utf-8 -*-

from . import js

node_global = js.Identifier("global")
detox = node_global.detox
device = node_global.device
by = node_global.by
element = node_global.element
expect = node_global.expect
wait_for = node_global.waitFor
await = js.GlobalAwait
