# -*- coding: utf-8 -*-
"""
    test_address_validation

    Test suite for the address API

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPL, see LICENSE for more details.
"""
import os
import logging

import unittest2 as unittest
from lxml import etree

from ups.address_validation import AddressValidation


class TestAddressValidation(unittest.TestCase):
    """
    Test the :class:`AddressValidation`
    """

    @classmethod
    def setUpClass(self):
        """Check if the variables for initialising the test case is available
        in the environment"""
        assert 'UPS_LICENSE_NO' in os.environ, \
            "UPS_LICENSE_NO not given. Hint:Use export UPS_LICENSE_NO=<number>"
        assert 'UPS_SHIPPER_NO' in os.environ, \
            "UPS_SHIPPER_NO not given. Hint:Use export UPS_SHIPPER_NO=<number>"
        assert 'UPS_USER_ID' in os.environ, \
            "UPS_USER_ID not given. Hint:Use export UPS_USER_ID=<user_id>"
        assert 'UPS_PASSWORD' in os.environ, \
            "UPS_PASSWORD not given. Hint:Use export UPS_PASSWORD=<password>"

    def setUp(self):
        """Initialise a AddressValidation.
        """
        logging.disable(logging.DEBUG)
        self.address_validation = AddressValidation(
            os.environ['UPS_LICENSE_NO'],
            os.environ['UPS_USER_ID'],
            os.environ['UPS_PASSWORD'],
            True            # Test must be performed in sandbox anyway
        )

    def test_010_address_validation_true(self):
        "Test the address validation of correct address"
        address_validation_type = AddressValidation.request_type(
            CountryCode="US", City="MIAMI", StateProvinceCode="FL",
            PostalCode="33101"
        )
        response = self.address_validation.request(address_validation_type)

        self.assertEqual(
            response.AddressValidationResult.Quality, 1.0
        )
        print etree.tostring(response, pretty_print=True)

    def test_020_address_validation_false(self):
        "Test the address validation of wrong address"
        address_validation_type = AddressValidation.request_type(
            CountryCode="US", City="MIAMI", StateProvinceCode="FL",
            PostalCode="12345"
        )
        response = self.address_validation.request(address_validation_type)

        self.assertTrue(
            len(response.AddressValidationResult) > 1
        )
        print etree.tostring(response, pretty_print=True)


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAddressValidation)
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
