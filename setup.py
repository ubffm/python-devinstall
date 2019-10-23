# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["devinstall"]

package_data = {"": ["*"]}

install_requires = [
    "collist @ git+https://github.com/ninjaaron/collist@master",
    "lazycli @ git+https://github.com/ninjaaron/lazycli@master",
    "libaaron>=1.4,<2.0",
]

entry_points = {"console_scripts": ["devinstall = devinstall:script.run"]}

setup_kwargs = {
    "name": "devinstall",
    "version": "0.1.0",
    "description": "",
    "long_description": None,
    "author": "Aaron Christianson",
    "author_email": "ninjaaron@gmail.com",
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.5,<4.0",
}


setup(**setup_kwargs)
