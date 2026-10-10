#!/usr/bin/env python3
"""
BPDB Smart Meter CLI

Command-line interface for BPDB smart meters.

The CLI (not the core engine) owns token persistence: `login` saves the bearer
token to ~/.python-bpdb-api-config, and the authenticated commands read it back.
The core `BPDBSmartMeterAPI` class stays stateless so it can be reused in web apps.
"""

import os
import sys
import functools
import configparser

import click
import requests
from tabulate import tabulate

from .bpdb import BPDBSmartMeterAPI
from . import __version__

CONFIG_FILE = os.path.expanduser("~/.python-bpdb-api-config")


def save_token(token):
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"token": token}
    with open(CONFIG_FILE, "w") as fh:
        config.write(fh)


def load_token():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config["DEFAULT"].get("token")
    return None


def client():
    """Build a core client using the saved token (if any)."""
    token = load_token()
    if not token:
        raise click.ClickException("Not logged in. Run `bpdb-cli login <phone> <otp>` first.")
    return BPDBSmartMeterAPI(token=token)


def handle_api_error(func):
    """Decorator to handle API errors gracefully."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            click.echo(
                f"❌ Could not reach the BPDB API at {BPDBSmartMeterAPI.BPDB_BASE_URL}.\n"
                "   The service may be down or temporarily unreachable from your network. "
                "Please try again later.",
                err=True,
            )
            sys.exit(1)
        except click.ClickException:
            raise
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}", err=True)
            sys.exit(1)
    return wrapper


@click.group()
@click.version_option(version=__version__, prog_name="bpdb-cli")
def app():
    """
    🔌 BPDB Smart Meter CLI

    A command-line tool for managing BPDB smart meter accounts.
    Access consumer information, recharge history, and more.
    """
    pass


@click.command()
@click.argument("phone_number")
@handle_api_error
def send_otp(phone_number):
    """Send OTP to phone number for authentication."""
    click.echo(f"📱 Sending OTP to {phone_number}...")
    BPDBSmartMeterAPI().send_otp(phone_number=phone_number)
    click.echo(f"✅ OTP sent to {phone_number}")


@click.command()
@click.argument("phone_number")
@click.argument("otp")
@handle_api_error
def login(phone_number, otp):
    """Login with phone number and OTP, then save the token."""
    click.echo(f"🔐 Logging in with phone number {phone_number}...")
    token = BPDBSmartMeterAPI().login(phone_number=phone_number, otp=otp)
    save_token(token)
    click.echo(f"✅ Logged in. Token saved to {CONFIG_FILE}")


@click.command()
@click.argument("customer_number")
@click.argument("meter_number")
@handle_api_error
def recharge_info(customer_number, meter_number):
    """Get recharge history for customer and meter number."""
    click.echo("💳 Fetching recharge history...")
    data = client().recharge_info(customer_number=customer_number, meter_number=meter_number)

    if data:
        table = [
            [e["date"], e["gross_amount"], e["energy_cost"], e["tokens"]]
            for e in data
        ]
        click.echo("\n📊 Recharge History:")
        click.echo(tabulate(table, headers=["Date", "Gross Amount", "Energy Cost", "Tokens"], tablefmt="simple"))
    else:
        click.echo("⚠️  No recharge history found.")


@click.command()
@handle_api_error
def consumer_info():
    """Get consumer information for logged-in account."""
    click.echo("👤 Fetching consumer information...")
    data = client().consumer_info()

    table = [
        ["Division", data["division"]],
        ["Meter Type", data["meter_type"]],
        ["Account Type", data["account_type"]],
        ["S&D Division", data["snd_division"]],
        ["Sanction Load", data["sanction_load"]],
        ["Customer Name", data["customer_name"]],
        ["Customer Address", data["customer_address"]],
        ["Tariff Category", data["tariff_category"]],
    ]
    click.echo("\n📋 Consumer Information:")
    click.echo(tabulate(table, tablefmt="simple"))


app.add_command(send_otp)
app.add_command(login)
app.add_command(recharge_info)
app.add_command(consumer_info)

if __name__ == "__main__":
    app()
