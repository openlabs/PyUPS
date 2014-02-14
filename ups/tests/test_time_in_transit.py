# -*- coding: utf-8 -*-
"""
    test_time_in_transit_api

    Test suite for the time in transit API

    :copyright: (c) 2011 by COM.lounge GmbH
    :license: AGPL, see LICENSE for more details.
"""
import os
import logging
from datetime import datetime

import unittest2 as unittest

from ups import TimeInTransit, PyUPSException


class TestTimeInTransit(unittest.TestCase):
    """Test the :class:`TimeInTransit` class
    for various cases originating from D.
    """

    @classmethod
    def setUpClass(self):
        """Check if the variables for initialising the test case is available
        in the environment"""
        assert 'UPS_LICENSE_NO' in os.environ, \
            "UPS_LICENSE_NO not given. Hint:Use export UPS_LICENSE_NO=<number>"
        assert 'UPS_USER_ID' in os.environ, \
            "UPS_USER_ID not given. Hint:Use export UPS_USER_ID=<user_id>"
        assert 'UPS_PASSWORD' in os.environ, \
            "UPS_PASSWORD not given. Hint:Use export UPS_PASSWORD=<password>"

    def setUp(self):
        """Initialise a ShipmentConfirm and ShipmentAccept class each.
        """
        logging.disable(logging.DEBUG)
        self.time_in_transit_api = TimeInTransit(
            os.environ['UPS_LICENSE_NO'],
            os.environ['UPS_USER_ID'],
            os.environ['UPS_PASSWORD'],
            True            # Test must be performed in sandbox anyway
            )

    def test_time_in_transit(self):
        time_in_transit_request = TimeInTransit.time_in_transit_request_type(
            TimeInTransit.transit_to_type(
                PoliticalDivision2="Zapopan",
                PoliticalDivision1="JAL",
                CountryCode="MX",
                PostcodePrimaryLow="45150",            
            ),
            TimeInTransit.transit_from_type(
                PoliticalDivision2="Aachen",
                CountryCode="DE",
                PostcodePrimaryLow="52064", 
            ),
            TimeInTransit.shipment_weight_type('14.1',Code='KGS'),
            TimeInTransit.invoice_line_total_type(
                MonetaryValue='120',
                CurrencyCode='EUR',
            ),
            TotalPackagesInShipment='3',
            PickupDate=datetime.now().strftime('%Y%m%d'),
            Time='1830',
            DocumentsOnlyIndicator='02',
            MaximumListSize='45'            
        )
        resp = self.time_in_transit_api.request(time_in_transit_request)
        assert resp['Response']['ResponseStatusCode'] == 1
        assert resp['Response']['ResponseStatusDescription'] == 'Success'


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestTimeInTransit)
        )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
