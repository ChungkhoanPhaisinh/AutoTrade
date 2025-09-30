# 📈 AutoTrade

A modular system to **automatically connect to DNSE/Entrade, receive price data and execute trades** based on **user-defined strategies**.

## Features
- 🧠 Define and plug in your own trading strategies
- ⚡ Automated trade execution when signals are triggered
- 📊 Real-time market data
- 🛠 Modular design for brokers, strategies, and risk modules

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/ChungkhoanPhaisinh/AutoTrade.git
cd AutoTrade
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your settings
Create a .env file like this and fill-in your data
```bash
usernameEntrade=
passwordEntrade=

gmailDNSE=<email used to register to DNSE>
passwordDNSE=
appPasswordDNSE=
```

### 4. Run the system
```bash
python main.py
```

## 🤖 Creating Your Own Agent
All trading bots (agents) are stored in the `agents/` folder.
To build your own bot:

1. Create a new file inside the `agents/` folder.
2. Inherit from the `Agent` class.
3. Implement your custom trading logic.
4. Add the bot to `ACTIVE_BOT` variable inside `logic_processor.py`.
5. Change logic in `logic_processor.py` to execute more complex logic.

## ⚠️ Disclaimer
This project is for educational and research purposes only.
Trading involves risk, and past performance does not guarantee future results.
Use at your own responsibility.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to open a PR.
