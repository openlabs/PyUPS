# -*- coding: utf-8 -*-
"""
    time_in_transit

    :copyright: (c) 2011 by COM.lounge GmbH
    :copyright: (c) 2010 by Carsten Rebbien.
    :copyright: (c) 2011 by United Parcel Service of America (Documentation)
    :license: AGPL, see LICENSE for more details.

"""
from __future__ import with_statement

from threading import Lock

from lxml import etree, objectify
from lxml.builder import E

from base import BaseAPIClient


_logger_lock = Lock()


class TimeInTransit(BaseAPIClient):
    """Implements the TimeInTransitRequest"""

    # Indicates the action to be taken by the XML service.
    RequestAction = E.RequestAction('TimeInTransit')

    # Optional Processing
    # nonvalidate = No address validation.
    # validate = Fail on failed address validation.
    #
    # Defaults to validate. Note: Full address validation is not performed.
    # Therefore, it is the responsibility of the Shipping Tool User to ensure
    # the address entered is correct to avoid an address correction fee.
    RequestOption = E.RequestOption('nonvalidate')

    # TransactionReference identifies transactions between client and server.
    TransactionReference = E.TransactionReference(
        E.CustomerContext('unspecified')
    )

    @classmethod
    def time_in_transit_request_type(cls, *args, **kwargs):
        """Builds a TimeInTransitRequest. All elements other than the
        description are required.
        :param TransitTo (Required): TransitTo element generated
            by :meth:`transit_to_type`
        :param TransitFrom (Required): TransitFrom element generated
            by :meth:`transit_from_type`
        :param ShipmentWeight (Optional): Service element generated
            by :meth:`shipment_weight_type`
        :param TotalPackagesInShipment (Optional): Default: 1
        :param PickupDate (Required): Format: YYYYMMDD
        :param Time (Optional): Format: HHMM
        :param InvoiceLineTotal (Optional): InvoiceLineTotal element generated
            by :meth: `invoice_line_total_type`
        :param DocumentsOnlyIndicator (Optional)
        :param MaximumListSize (Optional): Default: 35
        """

        # /TimeInTransitRequest/Request
        request = E.Request(
            cls.RequestAction,
            cls.RequestOption,
            cls.TransactionReference,
        )

        elements = cls.make_elements([
            'TransitTo', 'TransitFrom', 'PickupDate',
        ], args, kwargs)

        # The full request consists of the Request and all given elements
        # /TimeInTransitRequest/
        return E.TimeInTransitRequest(
            request, *elements)

    @classmethod
    def transit_to_type(cls, *args, **kwargs):
        """Returns the transit to data type. (/TimeInTransitRequest/TransitTo)
        :param PoliticalDivision3 (Optional) Town Accepted for
         International requests.
        :param PoliticalDivision2 (Optional) City Required for
         International if Postal
             Code is not used in the Origin Country.
        :param PoliticalDivision1 (Optional) State/Province Accepted
         if provided.
        :param Country (Optional)
        :param CountryCode (Required)
        :param PostcodePrimaryHigh (Optional)
        :param PostcodePrimaryLow (Optional)
        :param ResidentialAddressIndicator (Required)
        """
        required_args = (
            'CountryCode',
        )
        elements = cls.make_elements(required_args, args, kwargs)
        # Construct the AddressArtifactFormat Element
        # /TimeInTransitRequest/TransitTo/AddressArtifactFormat
        address_element = E.AddressArtifactFormat(*elements)
        return E.TransitTo(address_element)

    @classmethod
    def transit_from_type(cls, *args, **kwargs):
        """Returns the transit from data type
         (/TimeInTransitRequest/TransitFrom)
        :param PoliticalDivision3 (Optional)
        :param PoliticalDivision2 (Optional)
        :param PoliticalDivision1 (Optional)
        :param Country (Optional)
        :param CountryCode (Required)
        :param PostcodePrimaryHigh (Optional)
        :param PostcodePrimaryLow (Optional)
        :param ResidentialAddressIndicator (Required)
        """
        required_args = (
            'CountryCode',
        )
        elements = cls.make_elements(required_args, args, kwargs)
        # Construct the AddressArtifactFormat Element
        # /TimeInTransitRequest/TransitFrom/AddressArtifactFormat
        address_element = E.AddressArtifactFormat(*elements)
        return E.TransitFrom(address_element)

    @classmethod
    def shipment_weight_type(cls, Weight, *args, **kwargs):
        """Returns the shipment weight data type.
         (/TimeInTransitRequest/ShipmentWeight)
        :param Weight (Required)
        :param Code (Required)
        :param Description (Optional)
        """
        return E.ShipmentWeight(
            E.UnitOfMeasurement(*cls.make_elements(['Code'], args, kwargs)),
            E.Weight(Weight)
        )

    @classmethod
    def invoice_line_total_type(cls, *args, **kwargs):
        """Returns the invoice line total
        (shipment value) ( /TimeInTransitRequest/InvoiceLineTotal)
        :param CurrencyCode (Optional)
        :param MonetaryValue (Required)
        """
        elements = cls.make_elements(['MonetaryValue'], args, kwargs)
        return E.InvoiceLineTotal(*elements)

    @property
    def url(self):
        """Returns the API URL by concatenating the base URL provided
        by :attr:`BaseAPIClient.base_url` and the
        :attr:`BaseAPIClient.sandbox` flag
        """
        return '/'.join([
            self.base_url[self.sandbox and 'sandbox' or 'production'],
            'TimeInTransit']
        )

    def request(self, time_in_transit_request):
        """Calls up UPS and send the request. Get the returned response
        and return an element built out of it.

        :param time_in_transit_request: lxml element with data for the
            time_in_transit_request

        """
        full_request = '\n'.join([
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(self.access_request, pretty_print=True),
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(time_in_transit_request, pretty_print=True),
        ])
        self.logger.debug("Request XML: %s", full_request)

        # Send the request
        result = self.send_request(self.url, full_request)
        self.logger.debug("Response Received: %s", result)

        response = objectify.fromstring(result)
        self.look_for_error(response, full_request)

        # Return request ?
        if self.return_xml:
            return full_request, response
        else:
            return response


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
