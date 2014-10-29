# -*- coding: utf-8 -*-
"""
    __init__

    Test Suite for UPS Shipping

    :copyright: (c) 2011 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPL, see LICENSE for more details.
"""
import unittest2 as unittest

from .test_address_validation import TestAddressValidation
from .test_rating_package import TestRatingPackage
from .test_worldship_xml import TestWorldShipXML
from .test_time_in_transit import TestTimeInTransit


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestAddressValidation),
        unittest.TestLoader().loadTestsFromTestCase(TestRatingPackage),
        unittest.TestLoader().loadTestsFromTestCase(TestWorldShipXML),
        unittest.TestLoader().loadTestsFromTestCase(TestTimeInTransit),
    ])
    return suite
