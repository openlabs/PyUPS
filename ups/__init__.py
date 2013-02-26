'''
    ups.__init__

    XML Based API to UPS

    :copyright: (c) 2010-2013 by Openlabs Technologies & Consulting (P) LTD
    :copyright: (c) 2010 by Sharoon Thomas.
    :license: AGPL, see LICENSE for more details
'''
from .shipping_package import ShipmentConfirm, ShipmentAccept, ShipmentVoid
from .shipping_package import PyUPSException
