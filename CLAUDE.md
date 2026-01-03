# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool for interacting with Bangladesh Power Development Board (BPDB) smart meter APIs. It provides OTP-based authentication and allows users to retrieve consumer information and recharge history through a command-line interface.

## Architecture

### Core Components

**bpdb/bpdb.py** - API Client Layer
- `BPDBSmartMeterAPI` class handles all HTTP communication with BPDB endpoints
- Base URL: `http://202.51.186.182:33262/api/v1`
- Token-based authentication using Bearer tokens
- Token persistence via configparser stored at `~/.python-bpdb-api-config`
- Methods: `send_otp()`, `login()`, `consumer_info()`, `recharge_info()`

**bpdb/main.py** - CLI Layer
- Click-based CLI with command group pattern
- Commands registered via `app.add_command()` pattern
- Error handling through `handle_api_error` decorator wrapper
- Entry point: `app()` function mapped to `bpdb-cli` in pyproject.toml
- Uses tabulate for formatted output display

**bpdb/__init__.py** - Package Entry Point
- Exports `BPDBSmartMeterAPI` class for programmatic use
- Version controlled by GitHub Actions during release (format: `1.{run_number}.0`)

### Authentication Flow

1. User calls `send-otp` with phone number → API sends OTP
2. User calls `login` with phone number and OTP → API returns Bearer token
3. Token saved to `~/.python-bpdb-api-config` using configparser
4. Subsequent commands (`consumer-info`, `recharge-info`) auto-load token from config file
5. Token passed as `Authorization: Bearer {token}` header

## Development Commands

### Setup
```bash
# Install in development mode
pip install -e .

# Or create virtual environment first
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Testing the CLI
```bash
# Test OTP send
bpdb-cli send-otp 01710123456

# Test login
bpdb-cli login 01710123456 123456

# Test consumer info (requires prior login)
bpdb-cli consumer-info

# Test recharge info (requires prior login)
bpdb-cli recharge-info 01710123456 0120100112233
```

### Building
```bash
# Build distribution packages
python -m pip install build
python -m build

# Output: dist/*.whl and dist/*.tar.gz
```

## Version Management

- Version is defined in `bpdb/__init__.py` as `__version__ = "1.0.0"`
- GitHub Actions workflow (`.github/workflows/pypi.yml`) auto-updates version on push to main
- Version format: `1.{github.run_number}.0`
- Workflow uses sed to replace version string: `sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" bpdb/__init__.py`

## Publishing

Automated via GitHub Actions on push to main:
1. Version number updated automatically
2. Build artifacts created with `python -m build`
3. Published to PyPI using trusted publisher with OIDC token

Manual workflow dispatch also available via GitHub Actions UI.

## API Response Structures

### Consumer Info Response
Extracts these fields from `response.json()["user"]["prepaid_data"]`:
- division, meterType, accountType, sndDivision
- sanctionLoad, customerName, customerAddress, tariffCategory

### Recharge Info Response
Parses `response.json()["message"]["orders"]["order"]` array:
- Each order contains: date, grossAmount, energyCost, tokens

## CLI Design Pattern

All commands follow this pattern:
1. Click decorator defines command with arguments
2. `@handle_api_error` decorator catches exceptions and exits with error code 1
3. Print status message with emoji
4. Instantiate `BPDBSmartMeterAPI()`
5. Call API method
6. Format output with tabulate (or simple echo for OTP/login)

## Important Notes

- This is part of a multi-repository project with sibling repositories: `python-desco` and `python-nesco` (similar utility tools for other Bangladesh power companies)
- All three repositories share similar structure and patterns
- Token storage uses simple configparser format (not encrypted)
- No test suite currently exists
- API endpoints are HTTP (not HTTPS)
