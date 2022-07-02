import logging
import os

from telebot_bot import bot


logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGGING_LEVEL", "INFO").upper())


def main():
    current_webhook_url = bot.get_webhook_info().url
    if current_webhook_url != '':
        logger.critical("Removing webhook URL: %s", current_webhook_url)
    bot.remove_webhook()
    try:
        bot.infinity_polling()
    finally:
        if current_webhook_url != '':
            logger.critical("Restoring webhook URL: %s", current_webhook_url)
            bot.set_webhook(url=current_webhook_url)


if __name__ == "__main__":
    main()

