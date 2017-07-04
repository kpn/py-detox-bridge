
from setuptools import setup
setup(**{'author': 'Jan-Eric Duden',
 'author_email': 'jan-eric.duden@kpn.com',
 'classifiers': ['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Internet :: WWW/HTTP'],
 'description': 'A python bridge to the detox greybox testing library',
 'include_package_data': True,
 'install_requires': [],
 'long_description': 'Detox Python Bridge\n'
                     '===========================\n'
                     '\n'
                     'A bridge to enable python code to use the detox grey-box '
                     'testing API ( https://github.com/wix/detox )\n'
                     '\n'
                     '\n'
                     'Requirements\n'
                     '============\n'
                     '\n'
                     'The package requires nvm to be installed. The NVM_DIR '
                     'environment needs to point at the root directory of nvm '
                     'containing the nvm.sh script.\n'
                     '\n'
                     '\n'
                     '.. image:: '
                     'https://secure.travis-ci.org/kpn-digital/detox_bridge.svg?branch=master\n'
                     '    :target:  '
                     'http://travis-ci.org/kpn-digital/detox_bridge?branch=master\n'
                     '\n'
                     '.. image:: '
                     'https://img.shields.io/codecov/c/github/kpn-digital/detox_bridge/master.svg\n'
                     '    :target: '
                     'http://codecov.io/github/kpn-digital/detox_bridge?branch=master\n'
                     '\n'
                     '.. image:: '
                     'https://img.shields.io/pypi/v/detox_bridge.svg\n'
                     '    :target: https://pypi.python.org/pypi/detox_bridge\n'
                     '\n'
                     '.. image:: '
                     'https://readthedocs.org/projects/detox_bridge/badge/?version=latest\n'
                     '    :target: '
                     'http://detox_bridge.readthedocs.org/en/latest/?badge=latest\n',
 'name': 'detox-bridge',
 'packages': ['detox_bridge', 'tests'],
 'tests_require': ['tox'],
 'url': 'ssh://git@github.com:kpn-digital/py-detox-bridge.git',
 'version': None,
 'zip_safe': False})
