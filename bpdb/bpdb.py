#!/usr/bin/env python3
"""
BPDB (Bangladesh Power Development Board) smart-meter API client.

Stateless core engine: construct with an optional bearer token, call methods,
get back plain dicts. No file or environment I/O happens here, so the class is
safe to instantiate per-request inside FastAPI, Django, or any web framework.
Token persistence (file, DB, Redis) is the caller's responsibility -- see the
`examples/` directory.
"""

import requests


class BPDBSmartMeterAPI:
    BPDB_BASE_URL = "http://202.51.186.182:33262/api/v1"
    TIMEOUT = 30

    def __init__(self, token=None):
        """
        Args:
            token: a bearer token obtained from `login()`. Required for the
                   authenticated calls (`consumer_info`, `recharge_info`).
        """
        self.token = token

    # --- auth ---------------------------------------------------------------

    def send_otp(self, phone_number):
        """Request an OTP be sent to the given phone number."""
        url = f"{self.BPDB_BASE_URL}/generate-otp?phone={phone_number}"
        response = requests.post(url, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def login(self, phone_number, otp):
        """
        Validate an OTP and return a bearer token.

        The token is stored on `self.token` for convenience but is NOT persisted
        anywhere -- persist the returned value yourself.
        """
        url = f"{self.BPDB_BASE_URL}/validate-otp?phone={phone_number}&otp={otp}"
        response = requests.post(url, timeout=self.TIMEOUT)
        response.raise_for_status()

        payload = response.json()
        if payload.get("message") != "OTP verified successfully":
            raise RuntimeError(payload.get("message", "OTP validation failed"))

        self.token = payload.get("token")
        return self.token

    def _auth_headers(self):
        if not self.token:
            raise RuntimeError("Not authenticated. Pass token= or call login() first.")
        return {"Authorization": f"Bearer {self.token}"}

    # --- data ----------------------------------------------------------------

    def consumer_info(self):
        """Return consumer/meter details for the logged-in account as a dict."""
        url = f"{self.BPDB_BASE_URL}/auth/consumer"
        response = requests.get(url, headers=self._auth_headers(), timeout=self.TIMEOUT)
        response.raise_for_status()

        prepaid = response.json()["user"]["prepaid_data"]
        return {
            "division": prepaid.get("division"),
            "meter_type": prepaid.get("meterType"),
            "account_type": prepaid.get("accountType"),
            "snd_division": prepaid.get("sndDivision"),
            "sanction_load": prepaid.get("sanctionLoad"),
            "customer_name": prepaid.get("customerName"),
            "customer_address": prepaid.get("customerAddress"),
            "tariff_category": prepaid.get("tariffCategory"),
        }

    def recharge_info(self, customer_number, meter_number):
        """Return recharge history for a customer/meter as a list of dicts."""
        url = (
            f"{self.BPDB_BASE_URL}/prepaid-consumer-info"
            f"?customer_number={customer_number}%2C&meter_number={meter_number}"
        )
        response = requests.post(url, headers=self._auth_headers(), timeout=self.TIMEOUT)
        response.raise_for_status()

        orders = response.json()["message"]["orders"]["order"]
        return [
            {
                "date": order.get("date"),
                "gross_amount": order.get("grossAmount"),
                "energy_cost": order.get("energyCost"),
                "tokens": order.get("tokens"),
            }
            for order in orders
        ]
