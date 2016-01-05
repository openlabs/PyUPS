#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Pythonic API to UPS® Shipping Services

    :copyright: (c) 2010-2013 by Openlabs Technologies & Consulting (P) LTD
    :copyright: (c) 2010 by Sharoon Thomas.
    :license: AGPL, see LICENSE for more details
'''

from setuptools import setup


setup(
    name='PyUPS',
    version='0.6.2',
    license='AGPL',
    author='Openlabs Technologies & Consulting (P) LTD',
    author_email='info@openlabs.co.in',
    url='http://openlabs.co.in',
    description="Python client to UPS® Shipping Webservice API",
    long_description=__doc__,
    keywords="UPS®, Shipping, United Parcel Service of America®",
    test_suite='ups.tests.suite',
    packages=[
        'ups',
        'ups.tests',
    ],
    install_requires=[
        'distribute',
        'lxml',
        'unittest2',
    ]
)
