# WBot

## Overview
WBot is a Discord bot built using the `py-cord` library. It features various gambling and economy commands for users to enjoy.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Discord bot token
- MongoDB instance

### Installation Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/kerkpower/wbot.git
    cd wbot
    ```

2. **Create and Activate a Python Virtual Environment:**
   ```bash
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

3. **Install Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**    
    Rename the `template.env` file to `.env` and update the values:
    
    ```env
    DISC_TOKEN=your_discord_bot_token
    MONG_USER=your_mongo_username
    MONG_PASSWORD=your_mongo_password
    MONG_HOSTNAME=your_mongo_hostname
    ```
    
    - `DISC_TOKEN`: Your bot token from the [Discord Developer Portal](https://discord.com/developers/applications)
    - `MONG_USER`: The username for your MongoDB instance
    - `MONG_PASSWORD`: The password for your MongoDB instance
    - `MONG_HOSTNAME`: The hostname of your MongoDB server (everything after the @)

## Running the Bot
To start the bot, execute the `main.py` file:

```bash
# Ensure the virtual environment is activated
python main.py
```

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
