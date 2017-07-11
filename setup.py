
from setuptools import setup
setup(**{'author': 'Jan-Eric Duden',
 'author_email': 'jan-eric.duden@kpn.com',
 'classifiers': ['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Internet :: WWW/HTTP'],
 'description': 'A python bridge to the detox greybox testing library',
 'include_package_data': True,
 'install_requires': [],
 'long_description': 'Detox Python Bridge\n'
                     '===========================\n'
                     '\n'
                     '.. image:: '
                     'https://secure.travis-ci.org/kpn-digital/py-detox-bridge.svg?branch=master\n'
                     '    :target:  '
                     'http://travis-ci.org/kpn-digital/py-detox-bridge?branch=master\n'
                     '\n'
                     '.. image:: '
                     'https://img.shields.io/codecov/c/github/kpn-digital/py-detox-bridge/master.svg\n'
                     '    :target: '
                     'http://codecov.io/github/kpn-digital/py-detox-bridge?branch=master\n'
                     '\n'
                     '.. image:: '
                     'https://img.shields.io/pypi/v/detox-bridge.svg\n'
                     '    :target: https://pypi.python.org/pypi/detox-bridge\n'
                     '\n'
                     '.. image:: '
                     'https://readthedocs.org/projects/detox-bridge/badge/?version=latest\n'
                     '    :target: '
                     'http://detox-bridge.readthedocs.org/en/latest/?badge=latest\n'
                     '\n'
                     'A bridge to enable python code to use the detox grey-box '
                     'testing API ( https://github.com/wix/detox )\n'
                     '\n'
                     '\n'
                     'Requirements\n'
                     '============\n'
                     '\n'
                     'NVM\n'
                     '---\n'
                     '\n'
                     'The package requires nvm to be installed. Either the NVM '
                     'environment variable needs to contain the full path of '
                     'the nvm.sh script, or \n'
                     'the NVM_DIR environment variable needs to point at the '
                     'root directory of nvm containing the nvm.sh script.\n'
                     '\n'
                     'NODE\n'
                     '----\n'
                     '\n'
                     'The code emitted by this bridge requires node 7.6.0 or '
                     'higher.\n',
 'name': 'detox-bridge',
 'packages': ['detox_bridge'],
 'tests_require': ['tox'],
 'url': 'ssh://git@github.com:kpn-digital/py-detox-bridge.git',
 'version': None,
 'zip_safe': False})
