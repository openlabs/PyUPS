# -*- coding: utf-8 -*-
"""
    helper

    General Test Helpers

    :copyright: (c) 2011 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPL, see LICENSE for more details.
"""
from ups.shipping_package import ShipmentConfirm


class ShippingPackageHelper(object):
    """A convenient helper class to execute the boiler plate code which gener-
    ates the TestCode data to keep the Test Suites more readable and easy to
    extend.
    """

    @staticmethod
    def get_shipper(shipper_number, country="GB"):
        """Returns a shipper from a known country"""
        if country == "GB":
            shipper_address = ShipmentConfirm.address_type(
                AddressLine1="2,Hope Rd",
                AddressLine2="Anson Road",
                City="Manchester",
                CountryCode="GB",
                PostalCode="M145EU"
            )
        elif country == "US":
            shipper_address = ShipmentConfirm.address_type(
                AddressLine1="245 NE 24th Street",
                AddressLine2="Suite 108",
                City="Miami",
                StateProvinceCode="FL",
                CountryCode="US",
                PostalCode="33137"
            )
        else:
            raise Exception("This country is not supported")

        return ShipmentConfirm.shipper_type(
            shipper_address,
            Name="Openlabs",
            AttentionName="Openlabs",
            TaxIdentificationNumber="33065",
            PhoneNumber='0987654321',
            ShipperNumber=shipper_number,
        )

    @staticmethod
    def get_ship_from(country="GB"):
        """Returns a shipfrom from a known country"""
        if country == "GB":
            ship_from_address = ShipmentConfirm.address_type(
                AddressLine1="2,Hope Rd",
                AddressLine2="Anson Road",
                City="Manchester",
                CountryCode="GB",
                PostalCode="M145EU"
            )
        elif country == "US":
            ship_from_address = ShipmentConfirm.address_type(
                AddressLine1="245 NE 24th Street",
                AddressLine2="Suite 108",
                City="Miami",
                StateProvinceCode="FL",
                CountryCode="US",
                PostalCode="33137"
            )
        else:
            raise Exception("This country is not supported")

        return ShipmentConfirm.ship_from_type(
            ship_from_address,
            CompanyName="Openlabs",
            AttentionName="Someone other than Sharoon",
            TaxIdentificationNumber="33065",
            PhoneNumber='0987654321',
        )

    @staticmethod
    def get_ship_to(country="GB"):
        """Returns a shipto to a known country"""
        if country == "GB":
            ship_to_address = ShipmentConfirm.address_type(
                AddressLine1="205, Copper Gate House",
                AddressLine2="16 Brune Street",
                City="London",
                #StateProvinceCode="E1 7NJ",
                CountryCode="GB",
                PostalCode="E1 7NJ"
            )
        elif country == "US":
            ship_to_address = ShipmentConfirm.address_type(
                AddressLine1="1 Infinite Loop",
                City="Cupertino",
                StateProvinceCode="CA",
                CountryCode="US",
                PostalCode="95014"
            )
        else:
            raise Exception("This country is not supported")

        return ShipmentConfirm.ship_to_type(
            ship_to_address,
            CompanyName="Apple",
            AttentionName="Someone other than Steve",
            TaxIdentificationNumber="123456",
            PhoneNumber='4089961010',
        )

    @staticmethod
    def get_package(
        country="GB", package_type_code='02', weight='14.1', dimensions=None
    ):
        """UPS really expects units that are used in the country

        :param package_type_code: Str of the Code
        :param weight: Str eg '14.1'
        :param dimensions: A dict with length, width and height
            eg {'length': 10, 'width': 10, 'height': 10}
        """
        if dimensions is None:
            dimensions = {
                'length': '10',
                'width': '10',
                'height': '10',
            }
        if country == "GB":
            package_weight = ShipmentConfirm.package_weight_type(
                Weight=weight, Code="KGS", Description="Kilograms")
            dimensions = ShipmentConfirm.dimensions_type(
                Code="CM",
                Length=dimensions['length'],
                Width=dimensions['width'],
                Height=dimensions['height'],
            )
        elif country == "US":
            package_weight = ShipmentConfirm.package_weight_type(
                Weight=weight, Code="LBS", Description="Pounds")
            dimensions = ShipmentConfirm.dimensions_type(
                Code="IN",
                Length=dimensions['length'],
                Width=dimensions['width'],
                Height=dimensions['height'],
            )
        else:
            raise Exception("This country is not supported")

        package_type = ShipmentConfirm.packaging_type(Code=package_type_code)

        return ShipmentConfirm.package_type(
            package_type,
            package_weight,
            dimensions,
        )

    @staticmethod
    def get_payment_info(type="prepaid", **kwargs):
        """Returns the payment info filled

        :param type: The payment type.

        .. note::
            if payment type is prepaid AccountNumber must be provided.
        """
        if type == 'prepaid':
            assert 'AccountNumber' in kwargs
            return ShipmentConfirm.payment_information_type(
                ShipmentConfirm.payment_information_prepaid_type(
                    AccountNumber=kwargs['AccountNumber'])
            )
        else:
            raise Exception("Type %s is not supported" % type)
