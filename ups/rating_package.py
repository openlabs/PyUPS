# -*- coding: utf-8 -*-
"""
    rating_package

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2014 by United Parcel Service of America (Documentation)

    :license: BSD, see LICENSE for more details.

    Rating Package XML API
    ~~~~~~~~~~~~~~~~~~~~~~~~

    .. note::
        The documentation is partly extracted from the UPS Developer guide and
        is hence covered by the copyright of United Parcel Service of America

    The Rating API gives applications the ability to look up rates for UPS
    services and compare the cost of service alternatives.


"""
from lxml.builder import E
from lxml import etree, objectify

from base import BaseAPIClient
from shipping_package import ShipmentMixin


class RatingService(ShipmentMixin, BaseAPIClient):
    """Implements the Rate Request"""

    # Indicates the action to be taken by the XML service.
    RequestAction = E.RequestAction('Rate')
    RequestOption = E.RequestOption('Shop')

    # TransactionReference identifies transactions between client and server.
    TransactionReference = E.TransactionReference(
        E.CustomerContext('unspecified')
    )

    @property
    def url(self):
        """Returns the API URL by concatenating the base URL provided
        by :attr:`BaseAPIClient.base_url` and the
        :attr:`BaseAPIClient.sandbox` flag
        """
        return '/'.join([
            self.base_url[self.sandbox and 'sandbox' or 'production'],
            'Rate']
        )

    @classmethod
    def customer_classification_type(cls, code):
        """
        Valid values are:

        * 00- Rates Associated with Shipper Number;
        * 01- Daily Rates;
        * 04- Retail Rates;
        * 53- Standard List Rates;

        The default value is 01 (Daily Rates) when the Pickup Type code is
        01 (Daily pickup). The default value is 04 (Retail Rates) when the
        Pickup Type code is:

        * 06 -One Time Pickup,
        * 07 - On Call Air,
        * 19 - Letter Center, or
        * 20 - Air Service Center

        .. note::

            If invalid value is provided, default will be used depending on
            the value of pickup type code. Length is not validated.
        """
        return E.CustomerClassification(E.Code(code))

    @classmethod
    def rating_request_type(cls, shipment, *args, **kwargs):
        """
        Builds a RateRequest xml from the given lxml elements

        :param Shipment: Container for Shipment
        :param CustomerClassification: Customerclassificationcontainer. Valid
                                       if ShipFrom country is US. See
                                       :meth:`customer_classification`
        :param PickupType: Pickup Type container tag (optional)
        """
        request = E.Request(
            cls.RequestAction,
            cls.RequestOption,
            cls.TransactionReference,
        )
        return E.RatingServiceSelectionRequest(
            request, shipment, *args, **kwargs
        )

    def request(self, rate_request):
        """Calls up UPS and send the request. Get the returned response
        and return an element built out of it.

        :param rate_request: lxml element with data for the rate request
        """
        full_request = '\n'.join([
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(self.access_request, pretty_print=True),
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(rate_request, pretty_print=True),
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
