#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Pythonic API to UPS® Shipping Services

    :copyright: (c) 2010-2011 by Openlabs Technologies & Consulting (P) LTD
    :copyright: (c) 2010 by Sharoon Thomas.
    :license: AGPL, see LICENSE for more details
'''
from setuptools import setup

import api

setup(
    name = 'PyUPS',
    version = api.__version__,
    license = 'AGPL',
    author = api.__author__,
    author_email = 'info@openlabs.co.in',
    url = 'http://openlabs.co.in',

    description = "Python client to UPS® Shipping Webservice API",
    long_description = __doc__,
    keywords = "UPS®, Shipping, United Parcel Service of America®",

    packages = [
        'ups',
        'ups.tests',
        ],
    package_dir = {
        'ups': 'api',
        'ups.tests': 'tests',
        },
    install_requires=[
        'distribute',
        'lxml',
        'unittest2',
        ]
)

