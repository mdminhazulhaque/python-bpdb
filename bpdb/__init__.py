"""
BPDB Smart Meter API Client

A Python package for interacting with Bangladesh Power Development Board (BPDB)
smart meter API endpoints.

Example:
    >>> from bpdb import BPDBSmartMeterAPI
    >>> api = BPDBSmartMeterAPI()
    >>> api.send_otp(phone_number="01XXXXXXXXX")
    >>> token = api.login(phone_number="01XXXXXXXXX", otp="123456")
    >>> client = BPDBSmartMeterAPI(token=token)   # stateless; pass token back in
    >>> client.consumer_info()
"""

from .bpdb import BPDBSmartMeterAPI

# Version will be updated by GitHub Actions during release
__version__ = "1.0.0"
__author__ = "Md Minhazul Haque"
__email__ = "mdminhazulhaque@gmail.com"

__all__ = ["BPDBSmartMeterAPI"]