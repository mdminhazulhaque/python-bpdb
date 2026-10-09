#!/usr/bin/env python3
"""
BPDB Smart Meter CLI

A command-line interface for interacting with BPDB smart meters.
Provides commands to send OTP, login, check recharge info, and view consumer details.
"""

import click
import sys
import functools
import requests
from tabulate import tabulate
from .bpdb import BPDBSmartMeterAPI
from . import __version__


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
@click.argument('phone_number')
@handle_api_error
def send_otp(phone_number):
    """Send OTP to phone number for authentication."""
    click.echo(f"📱 Sending OTP to {phone_number}...")
    apiclient = BPDBSmartMeterAPI()
    apiclient.send_otp(phone_number=phone_number)
    click.echo(f"✅ OTP sent to {phone_number}")

@click.command()
@click.argument('phone_number')
@click.argument('otp')
@handle_api_error
def login(phone_number, otp):
    """Login with phone number and OTP."""
    click.echo(f"🔐 Logging in with phone number {phone_number}...")
    apiclient = BPDBSmartMeterAPI()
    apiclient.login(phone_number=phone_number, otp=otp)
    click.echo(f"✅ Successfully logged in with {phone_number}")

@click.command()
@click.argument('customer_number')
@click.argument('meter_number')
@handle_api_error
def recharge_info(customer_number, meter_number):
    """Get recharge history for customer and meter number."""
    click.echo("💳 Fetching recharge history...")
    apiclient = BPDBSmartMeterAPI()
    data = apiclient.recharge_info(customer_number=customer_number, meter_number=meter_number)

    if data:
        table = [
            [entry['date'], entry['gross_amount'], entry['energy_cost'], entry['tokens']]
            for entry in data
        ]
        click.echo("\n📊 Recharge History:")
        click.echo(tabulate(table, headers=['Date', 'Gross Amount', 'Energy Cost', 'Tokens'], tablefmt='simple'))
    else:
        click.echo("⚠️  No recharge history found.")

@click.command()
@handle_api_error
def consumer_info():
    """Get consumer information for logged-in account."""
    click.echo("👤 Fetching consumer information...")
    apiclient = BPDBSmartMeterAPI()
    data = apiclient.consumer_info()

    if data:
        table = [
            ['Division', data['division']],
            ['Meter Type', data['meterType']],
            ['Account Type', data['accountType']],
            ['S&D Division', data['sndDivision']],
            ['Sanction Load', data['sanctionLoad']],
            ['Customer Name', data['customerName']],
            ['Customer Address', data['customerAddress']],
            ['Tariff Category', data['tariffCategory']]
        ]
        click.echo("\n📋 Consumer Information:")
        click.echo(tabulate(table, tablefmt='simple'))
    else:
        click.echo("⚠️  No consumer information found.")

app.add_command(send_otp)
app.add_command(login)
app.add_command(recharge_info)
app.add_command(consumer_info)

if __name__ == '__main__':
    app()