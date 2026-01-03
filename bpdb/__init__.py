"""
BPDB Smart Meter API Client

A Python package for interacting with Bangladesh Power Development Board (BPDB)
smart meter API endpoints.

Example:
    >>> from bpdb import BPDBSmartMeterAPI
    >>> client = BPDBSmartMeterAPI()
    >>> client.send_otp(phone_number="01XXXXXXXXX")
    >>> client.login(phone_number="01XXXXXXXXX", otp="123456")
"""

from .bpdb import BPDBSmartMeterAPI

# Version will be updated by GitHub Actions during release
__version__ = "1.0.0"
__author__ = "Md Minhazul Haque"
__email__ = "mdminhazulhaque@gmail.com"

__all__ = ["BPDBSmartMeterAPI"]