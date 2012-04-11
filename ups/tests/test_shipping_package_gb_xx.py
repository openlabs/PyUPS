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
from datetime import datetime

import unittest2 as unittest

from ups import ShipmentConfirm, ShipmentAccept, PyUPSException
from helper import ShippingPackageHelper as Helper


class TestShippingPackage(unittest.TestCase):
    """Test the :class:`ShipmentConfirm` and :class:`ShipmentAccept` classes
    for various cases originating from GB.
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
        self.shipment_confirm_api = ShipmentConfirm(
            os.environ['UPS_LICENSE_NO'],
            os.environ['UPS_USER_ID'],
            os.environ['UPS_PASSWORD'],
            True            # Test must be performed in sandbox anyway
            )

        self.shipment_accept_api = ShipmentAccept(
            os.environ['UPS_LICENSE_NO'],
            os.environ['UPS_USER_ID'],
            os.environ['UPS_PASSWORD'],
            True            # Test must be performed in sandbox anyway
            )

    def test_0010_blow_up(self):
        """Send a stupid request which should blow up because its valid in the
        client but not in UPS server. Example: dont send packages"""
        with self.assertRaises(PyUPSException):
            ship_confirm_request = ShipmentConfirm.shipment_confirm_request_type(
                Helper.get_shipper(self.shipper_number, "GB"),
                Helper.get_ship_to("GB"),
                Helper.get_ship_from("GB"),

                Helper.get_payment_info(AccountNumber=self.shipper_number),
                ShipmentConfirm.service_type(Code='11'),    # UPS Standard
                Description = __doc__[:50]
                )
            self.shipment_confirm_api.request(ship_confirm_request)

    def test_0020_gb_gb(self):
        "GB to GB UPS Standard with 2 packages"
        ship_confirm_request = ShipmentConfirm.shipment_confirm_request_type(
            Helper.get_shipper(self.shipper_number, "GB"),
            Helper.get_ship_to("GB"),
            Helper.get_ship_from("GB"),

            # Package 1
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            # Package 2
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            Helper.get_payment_info(AccountNumber=self.shipper_number),
            ShipmentConfirm.service_type(Code='11'),    # UPS Standard
            Description = __doc__[:50]
            )
        response = self.shipment_confirm_api.request(ship_confirm_request)
        digest = self.shipment_confirm_api.extract_digest(response)

        # now accept the package
        accept_request = ShipmentAccept.shipment_accept_request_type(digest)
        result = self.shipment_accept_api.request(accept_request)

    @unittest.skipUnless(datetime.today().weekday() == 4, "since not a friday")
    def test_0030_gb_gb_saturday(self):
        "GB to GB UPS Standard with 2 packages and Saturday delivery"
        ship_confirm_request = ShipmentConfirm.shipment_confirm_request_type(
            Helper.get_shipper(self.shipper_number, "GB"),
            Helper.get_ship_to("GB"),
            Helper.get_ship_from("GB"),

            # Package 1
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            # Package 2
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            ShipmentConfirm.shipment_service_option_type(SaturdayDelivery="1"),

            Helper.get_payment_info(AccountNumber=self.shipper_number),
            ShipmentConfirm.service_type(Code='11'),    # UPS Standard
            Description = __doc__[:50]
            )
        response = self.shipment_confirm_api.request(ship_confirm_request)
        digest = self.shipment_confirm_api.extract_digest(response)

        # now accept the package
        accept_request = ShipmentAccept.shipment_accept_request_type(digest)
        result = self.shipment_accept_api.request(accept_request)

    def test_0040_gb_us(self):
        "GB to US UPS Standard with 2 packages"
        ship_confirm_request = ShipmentConfirm.shipment_confirm_request_type(
            Helper.get_shipper(self.shipper_number, "GB"),
            Helper.get_ship_to("US"),
            Helper.get_ship_from("GB"),

            # Package 1
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            # Package 2
            Helper.get_package("GB", weight='15.0', 
                package_type_code='02'),    # Customer Supplied Package

            Helper.get_payment_info(AccountNumber=self.shipper_number),
            ShipmentConfirm.service_type(Code='07'),    # UPS Standard
            Description = __doc__[:50]
            )
        response = self.shipment_confirm_api.request(ship_confirm_request)
        digest = self.shipment_confirm_api.extract_digest(response)

        # now accept the package
        accept_request = ShipmentAccept.shipment_accept_request_type(digest)
        result = self.shipment_accept_api.request(accept_request)


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestShippingPackage)
        )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
