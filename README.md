# 🔌 BPDB Smart Meter CLI

[![PyPI version](https://badge.fury.io/py/bpdb.svg)](https://badge.fury.io/py/bpdb)
[![Python Versions](https://img.shields.io/pypi/pyversions/bpdb.svg)](https://pypi.org/project/bpdb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/bpdb)](https://pepy.tech/project/bpdb)

A Python CLI tool to collect information about **Bangladesh Power Development Board (BPDB)** prepaid electricity accounts. Get real-time consumer details, recharge history, and manage your smart meter directly from your terminal.

## ✨ Features

- 📱 **OTP Authentication**: Secure login with phone number verification
- 👤 **Consumer Info**: Retrieve detailed customer and meter information
- 🔄 **Recharge History**: Track your payment and token generation records
- ⚡ **Smart Meter Integration**: Direct API integration with BPDB's official endpoints
- 🚀 **Fast & Lightweight**: Built with Python and designed for speed
- 🔒 **Secure**: Phone number-based authentication with OTP

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install bpdb
```

### From Source
```bash
git clone https://github.com/mdminhazulhaque/python-bpdb.git
cd python-bpdb
pip install -e .
```

## 🚀 Quick Start

After installation, use the `bpdb-cli` command:

```bash
# Get help
bpdb-cli --help

# Send OTP to your phone
bpdb-cli send-otp 01710123456

# Login with OTP
bpdb-cli login 01710123456 123456

# Get consumer information
bpdb-cli consumer-info
```

## 📖 Usage

```
Usage: bpdb-cli [OPTIONS] COMMAND [ARGS]...

  A CLI tool for BPDB Smart Meter management.

Options:
  --help  Show this message and exit.

Commands:
  send-otp       Send OTP to phone number for authentication
  login          Login with phone number and OTP
  consumer-info  Get detailed consumer and meter information
  recharge-info  Get recharge and token generation history
```

## 💡 Examples

### 📱 Send OTP

Send an OTP to your registered phone number:

```bash
$ bpdb-cli send-otp 01710123456
```

**Sample Output:**
```
OTP sent to 01710123456
```

### 🔐 Login

Login using your phone number and the OTP received:

```bash
$ bpdb-cli login 01710123456 123456
```

**Sample Output:**
```
Logged in with phone number 01710123456
```

### 👤 Get Consumer Information

Retrieve comprehensive customer and meter details:

```bash
$ bpdb-cli consumer-info
```

**Sample Output:**
```
+------------------+--------------------+
|     Division     |      Mymensingh    |
|    Meter Type    |          1P        |
|   Account Type   |   Active (Prepaid) |
|   S&D Division   |   S&D Kishoreganj  |
|  Sanction Load   |          4         |
|  Customer Name   | MD. ABDUL HANNAN   |
| Customer Address |      BOTTIRISH     |
| Tariff Category  |    Tariff : LT-A   |
+------------------+--------------------+
```

### 🔄 Get Recharge History

View your recent payment and token generation records:

```bash
$ bpdb-cli recharge-info 01710123456 0120100112233
```

**Sample Output:**
```
+---------------------+--------------+-------------+--------------------------+
|        Date         | Gross Amount | Energy Cost |          Tokens          |
+---------------------+--------------+-------------+--------------------------+
| 2024-05-01 16:15:04 |     5000     |   4662.19   | 1111-2222-3333-4444-5555 |
| 2024-10-01 17:47:27 |     5000     |   4281.47   | 1111-2222-3333-4444-5555 |
| 2025-01-01 23:41:46 |     5000     |   4785.47   | 1111-2222-3333-4444-5555 |
+---------------------+--------------+-------------+--------------------------+
```

## 🛠️ Development

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Setting up for Development

1. Clone the repository:
```bash
git clone https://github.com/mdminhazulhaque/python-bpdb.git
cd python-bpdb
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

### Dependencies

- `requests` - HTTP library for API calls
- `click` - Command line interface framework
- `tabulate` - Pretty-print tabular data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an independent, unofficial tool and is not affiliated with, endorsed by, or connected to the Bangladesh Power Development Board (BPDB).

Every piece of information this tool retrieves is **already publicly available** to any consumer through the official customer portal and mobile app. This project does **not** reverse engineer, bypass, or circumvent anything — it simply accesses the same publicly accessible consumer information programmatically and presents it in a convenient format.

Please only look up accounts you are authorized to access. Use at your own discretion; the authors are not responsible for any issues that may arise from using this tool.