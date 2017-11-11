#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Copyright (c) 2017, Tozti.

# This file is part of Tozti.

# Tozti is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Tozti is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Tozti.  If not, see <http://www.gnu.org/licenses/>.


import re
from setuptools import setup


setup(
    name='tozti',
    version=re.search(r"__version__\W*=\W*'([^']+)'",
                      open('server.py').read()).group(1),
    py_modules=['server'],
    author='Tozti',
    url='https://tozti.readthedocs.org',
    description='Storage engine for Tozti',
    license='AGPLv3',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
    install_requires=[
        'aiohttp~=2.3',
        'pyyaml~=3.12',
        'logbook~=1.1',
    ],
    entry_points={
        'console_scripts': ['run_tozti=server:main'],
    },
)
