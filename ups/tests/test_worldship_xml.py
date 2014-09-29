# -*- coding: utf-8 -*-
"""
    test_worldship xml export

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPL, see LICENSE for more details.
"""
import unittest2 as unittest
from lxml import objectify

from ups.worldship_api import WorldShip


class TestWorldShipXML(unittest.TestCase):
    """
    Test the :class:`Worldship`
    """

    def test_creating_xml(self):
        "Test worldship"
        package = WorldShip.package_type(
            PackageType='CP',
            Weight='15',
            Length='10',
            Width='15',
            Height='8'
        )
        ship_to = WorldShip.ship_to_type(
            CompanyOrName="Openlabs",
            Attention="Tarun Bhardwaj",
            Address1="48 Bismark St.",
            CountryTerritory="US",
            PostalCode="07712",
            CityOrTown="Asbury Park",
            StateProvinceCounty="NJ",
            Telephone="1234567891",
            ReceiverUpsAccountNumber="123456",
        )
        ship_from = WorldShip.ship_from_type(
            CompanyOrName="Amazon LLC",
            Attention="Amazon India",
            Address1="123 Main Street",
            CountryTerritory="US",
            PostalCode="59484",
            CityOrTown="Sweet Grass",
            StateProvinceCounty="MT",
            Telephone="9876543211",
            UpsAccountNumber="654321",
        )
        shipment_information = WorldShip.shipment_information_type(
            ServiceType="1DA",
            DescriptionOfGoods="Super Cool Stuff",
            GoodsNotInFreeCirculation="0",
            BillTransportationTo="Shipper",
        )
        final_xml = WorldShip.get_xml(
            ship_to, ship_from, shipment_information, package
        )

        print final_xml
        xml = objectify.fromstring(final_xml)
        self.assertTrue(xml.tag.endswith('OpenShipments'))


def suite():
    "Create a test suite and return it for better manageability"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestWorldShipXML)
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
