#!/usr/bin/env python2.7

import distutils.core

distutils.core.setup(
    name='dateconv',
    version='0.1.0',
    description='Converts unix timestamps to different Python date representations',
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    py_modules=['dateconv'])
