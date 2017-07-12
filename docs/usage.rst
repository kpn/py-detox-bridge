========
Usage
========

To use detox_bridge in a project
    
.. code:: python

   from detox_bridge import await, by, detox, device, element, expect, node_with_detox

   app_path = "detox/examples/demo-react-native"

   # Start Node server in app_path root folder that contains node_modules

   with node_with_detox(app_path=app_path, default_timeout=10) as appserver:

       # Detox Config (we could also load this from package.json)

       ios_sim_release = {
           "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/example.app",
           "type": "ios.simulator",
           "name": "iPhone 7 Plus"
       }

       configurations_obj = {"configurations": {"ios.sim.release": ios_sim_release}}

       # Longer timeout since the app may be installed

       appserver(await(detox.init(configurations_obj)), timeout=360)

       # Reload react native

       appserver(await(device.reloadReactNative()))

       # Expectation

       appserver(await(expect(element(by.id('welcome'))).toBeVisible()))

       # Cleanup

       appserver(await(detox.cleanup()))
