# -*- coding: utf-8 -*-
"""
    test_shipping_api

    Test suite for the shipping API

    .. note::
        UPS will only allow shippings to originate from the country where the
        shipper account belongs to. Hence, if you have an account in the UK
        then then you cannot test packages with that account originating from
        the USA.

    :copyright: (c) 2011 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPL, see LICENSE for more details.
"""
import os
import logging

import unittest2 as unittest
from lxml import etree
from lxml.builder import E

from ups.rating_package import RatingService
from helper import ShippingPackageHelper as Helper


class TestRatingPackage(unittest.TestCase):
    """
    Test the :class:`RatingService`
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
        """Initialise a ShipmentConfirm and ShipmentAccept class each.
        """
        logging.disable(logging.DEBUG)
        self.shipper_number = os.environ['UPS_SHIPPER_NO']
        self.rating_api = RatingService(
            os.environ['UPS_LICENSE_NO'],
            os.environ['UPS_USER_ID'],
            os.environ['UPS_PASSWORD'],
            True            # Test must be performed in sandbox anyway
        )

    def test_rate_fetching(self):
        "Test the rate fetching"
        rating_request = RatingService.rating_request_type(
            E.Shipment(
                Helper.get_shipper(self.shipper_number, "US"),
                Helper.get_ship_to("US"),
                Helper.get_ship_from("US"),
                RatingService.service_type(Code='03'),    # UPS Ground
                Helper.get_package("US", package_type_code="00")
            ),
        )
        response = self.rating_api.request(rating_request)

        self.assertTrue(
            response.RatedShipment.RatedPackage.TotalCharges.MonetaryValue
        )
        print etree.tostring(response, pretty_print=True)

    def test_rate_chart_fetching(self):
        "Test the rate fetching"
        rating_request = RatingService.rating_request_type(
            E.Shipment(
                Helper.get_shipper(self.shipper_number, "US"),
                Helper.get_ship_to("US"),
                Helper.get_ship_from("US"),
                Helper.get_package("US", package_type_code="00"),
            ),
        )
        response = self.rating_api.request(rating_request)

        self.assertTrue(
            len([s for s in response.iterchildren(tag='RatedShipment')]) > 1
        )

        self.assertTrue(
            response.RatedShipment.RatedPackage.TotalCharges.MonetaryValue
        )
        print etree.tostring(response, pretty_print=True)

    @unittest.expectedFailure
    def test_negotiated_rate_fetching(self):
        """
        Test the rate fetching with negotiated rates.
        This will fail if your shipper number is not eligible for negotaited
        rates
        """
        rating_request = RatingService.rating_request_type(
            E.Shipment(
                Helper.get_shipper(self.shipper_number, "US"),
                Helper.get_ship_to("US"),
                Helper.get_ship_from("US"),
                RatingService.service_type(Code='03'),    # UPS Ground
                Helper.get_package("US", package_type_code="00"),
                RatingService.rate_information_type(negotiated=True)
            ),
        )
        response = self.rating_api.request(rating_request)

        self.assertTrue(
            hasattr(response.RatedShipment, 'NegotiatedRates')
        )
        self.assertTrue(
            response.RatedShipment.RatedPackage.TotalCharges.MonetaryValue
        )
        print etree.tostring(response, pretty_print=True)


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestRatingPackage)
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
