# -*- coding: utf-8 -*-
"""
    worldship_api

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2014 by United Parcel Service of America (Documentation)

    :license: BSD, see LICENSE for more details.

    API to create XML for worldship

    .. note::
        The documentation is partly extracted from the UPS Developer guide and
        is hence covered by the copyright of United Parcel Service of America

"""
from lxml.builder import E
from lxml import etree

from base import BaseAPIClient
from shipping_package import ShipmentMixin


class WorldShip(ShipmentMixin, BaseAPIClient):
    """Implements the WorldShip"""

    @classmethod
    def package_type(cls, *args, **kwargs):
        """
        :param PackageType: Package type code
        :param Weight: Weight of package
        :param Length: Length of package
        :param Width: Width of package
        :param Height: Height of package
        """
        elements = cls.make_elements(['PackageType', 'Weight'], args, kwargs)
        return E.Package(*elements)

    @classmethod
    def ship_to_type(cls, *args, **kwargs):
        """Returns the ship to data type.
        :param CompanyOrName: (Required)
        :param Attention: (Required)
        :param Address1: (Required)
        :param CountryTerritory: (Required)
        :param PostalCode: Depend on Country
        :param CityOrTown: (Required for US)
        :param StateProvinceCounty: (Required for US)
        :param Telephone: (Conditional)
        :param ResidentialAddressIndicator: (optional)
        """
        elements = cls.make_elements([], args, kwargs)
        return E.ShipTo(*elements)

    @classmethod
    def ship_from_type(cls, *args, **kwargs):
        """Returns the ship from data type.
        :param CompanyOrName: (Required)
        :param Attention: (Required)
        :param Address1: (Required)
        :param CountryTerritory: (Required)
        :param PostalCode: Depend on Country
        :param CityOrTown: (Required for US)
        :param StateProvinceCounty: (Required for US)
        :param Telephone: (Conditional)
        :param ResidentialAddressIndicator: (optional)
        """
        elements = cls.make_elements([], args, kwargs)
        return E.ShipFrom(*elements)

    @classmethod
    def shipment_information_type(cls, *args, **kwargs):
        """
        :param ServiceType: string service type
            Small Package Service Level or Service Type
            --------------------------------
            Valid Values        Service name
            --------------------------------
            1DM                 Next Day Air Early AM
            1DA                 Next Day Air
            1DP                 Next Day Air Saver
            2DM                 2nd Day Air AM
            2DA                 2nd Day Air
            3DS                 3 Day Select
            GND                 Ground Service
            FTX                 LTL Express
            FTS                 LTL Standard
            EP                  Express Plus or Worldwide Express Plus
            ES                  Express or Worldwide Express
            EX                  Expedited or Worldwide Expedited
            ST                  Standard
            SV                  Express Saver or Worldwide Saver
            BASIC               Basic
            ND                  UPS Express (NA1)

            Mail Innovations Service Level or Service Type
            --------------------------------
            Valid Values        Service name
            --------------------------------
            MIF                 First Class Mail
            MIT                 Priority Mail
            MID                 Expedited Mail Innovations
            MIP                 Priority Mail Innovations
            MIE                 Economy Mail Innovations

            Freight Service Level or Service Type
            --------------------------------
            Valid Values        Service name
            --------------------------------
            AMG                 Next Day Air Freight - Guaranteed
            AM                  Next Day Air Freight - Non-Guaranteed
            D2G                 2nd Day Air Freight - Guaranteed
            D2                  2nd Day Air Freight - Non-Guaranteed
            DFG                 3 Day Air Freight - Guaranteed
            DF                  3 Day Air Freight - Non-Guaranteed
            CX                  Express Freight
            CA                  Air Freight Direct
            EC                  Air Freight Consolidated
            FLT                 Freight LTL
            FLG                 Freight LTL - Guaranteed
            UFT                 Freight LTL - Guaranteed A.M.

            SurePost Service Level or Service Type
            --------------------------------
            Valid Values        Service name
            --------------------------------
            USL                 SurePost Less than 1 lb
            USG                 SurePost 1 lb or Greater
            USB                 SurePost Bound Printed Matter
            USM                 SurePost Media

        :param DescriptionOfGoods: Description of Goods
        :param GoodsNotInFreeCirculation: Flag if goods are not in free
            circulation
        :param BillingOption:
            Billing Options
            -------------------------------
            Valid Values        Description
            -------------------------------
            PP                  Bill Shipper's UPS Account
            TP                  Bill Third Party
            TF                  Bill Third Party: Freight, Duty, Taxes
            FB                  FOB
            CF                  C&F
            BR                  Bill Receiver
            DP                  Delivery Duty Paid, Tax Unpaid
            BD                  Delivery Duty, Tax and Shipping Charges Paid by
                                    Shipper
            CB                  Consignee
        :param BillTransportationTo: following are the valid values
            -------------------------------
            Valid Values        Description
            -------------------------------
            SHP                 Shipper
            REC                 Receiver
            TP                  Third Party
        """
        elements = cls.make_elements([], args, kwargs)
        return E.ShipmentInformation(*elements)

    @classmethod
    def get_xml(cls, *args, **kwargs):
        """Builds OpenShipments element.

        :param ShipTo: ShipTo element generated by :meth:`ship_to_type`
        :param ShipFrom: ShipFrom element generated by :meth:`ship_from_type`
        :param ShipmentInformation: ShipmentInformation element generated by
            :meth:`shipment_information_type`
        :param Package: Package element generated by
            :meth:`package_type`
        """
        elements = cls.make_elements(
            ['ShipTo', 'ShipFrom', 'ShipmentInformation', 'Package'],
            args, kwargs
        )
        open_shipment = E.OpenShipment(
            ProcessStatus="", ShipmentOption="", *elements
        )
        open_shipments = E.OpenShipments(
            open_shipment, xmlns="x-schema:OpenShipments.xdr"
        )
        full_xml = '\n'.join([
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(open_shipments, pretty_print=True),
        ])
        return full_xml
