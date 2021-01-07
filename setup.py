#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()


setup(
    name="detox-bridge",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="A python bridge to the detox greybox testing library",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Jan-Eric Duden",
    author_email="jan-eric.duden@kpn.com",
    url="https://github.com/kpn-digital/py-detox-bridge",
    packages=find_packages(exclude=["tests*", "detox"]),
    tests_require=["tox"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
