# -*- coding: utf-8 -*-
"""
    address_validation

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2014 by United Parcel Service of America (Documentation)

    :license: BSD, see LICENSE for more details.

    Address Validation XML API
    ~~~~~~~~~~~~~~~~~~~~~~~~

    .. note::
        The documentation is partly extracted from the UPS Developer guide and
        is hence covered by the copyright of United Parcel Service of America

    The Address Validation API gives applications the ability to varify address
    for UPS services.

"""
from lxml.builder import E
from lxml import etree, objectify

from base import BaseAPIClient


class AddressValidation(BaseAPIClient):
    """Implements the Address Validation"""

    # Indicates the action to be taken by the XML service.
    RequestAction = E.RequestAction('AV')

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
            'AV']
        )

    @classmethod
    def request_type(cls, *args, **kwargs):
        """
        Builds a AddressValidation xml from the given lxml elements

        :param City: U.S. city to be validated. (A valid city/state/postal code
                     combination must be included as input)
        :param StateProvinceCode: State to be validated. (A valid
                                  city/state/postal code combination must be
                                  included as input)
        :param CountryCode: Country code 2 Digits
        :param PostalCode: Postal code
        ::
        """
        request = E.Request(
            cls.RequestAction,
            cls.TransactionReference,
        )
        elements = cls.make_elements(['CountryCode'], args, kwargs)
        return E.AddressValidationRequest(
            request, E.Address(*elements)
        )

    def request(self, address_validation_request):
        """Calls up UPS and send the request. Get the returned response
        and return an element built out of it.

        :param rate_request: lxml element with data for the rate request
        """
        full_request = '\n'.join([
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(self.access_request, pretty_print=True),
            '<?xml version="1.0" encoding="UTF-8" ?>',
            etree.tostring(address_validation_request, pretty_print=True),
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
