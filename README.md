# SupremeBot README

## Overview
WBot is a Discord bot built using the `py-cord` library. It has some gambling and economy commands for people to play with. 

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

2. **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables:**
    Rename the `template.env` file to `.env` and configure appropriately:
    
    ```ini
    DISC_TOKEN=your_discord_bot_token
    MONG_USER=your_mongo_username
    MONG_PASSWORD=your_mongo_password
    MONG_HOSTNAME=your_mongo_hostname
    ```
    
    - `DISC_TOKEN`: the token for your bot that can be taken from the [Discord Developer Portal](https://discord.com/developers/applications)
    - `MONG_USER`: the username of the MongoDB user
    - `MONG_PASSWORD`: the password for the MongoDB user
    - `MONG_HOSTNAME`: the hostname of your MongoDB server (everything after the @)

## Running the Bot
To start the bot, execute the `main.py` file:

```bash
python main.py
```


## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.