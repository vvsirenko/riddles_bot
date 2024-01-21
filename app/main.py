import os

from dotenv import load_dotenv

from app.logging.logging_utils import log, LogLevel
from telegram_bot import ChatTelegramBot


def main():
    # Read .env file
    load_dotenv()

    log(message="%(label)s App started", level=LogLevel.info, params={"label": "MyTelegramApp"})

    # Setup configuration
    telegram_config = {
        'token': os.environ.get('TELEGRAM_BOT_TOKEN')
    }

    # Setup and run
    telegram_bot = ChatTelegramBot(config=telegram_config)
    telegram_bot.run()


if __name__ == "__main__":
    main()