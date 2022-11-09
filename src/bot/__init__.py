from time import sleep

import coloring

from src.bot.base_functions import get_bot
from src.bot.base_functions import listener
from src.main_logger import logger
from src.bot.handlers import setup_handlers


def start():
    while 1:
        try:
            bot = get_bot()
            bot.set_update_listener(listener)
            setup_handlers(bot)
            bot.infinity_polling()

        except Exception as e:
            print(coloring.red("[!] An error in the bot. Attempt to restart after 5 seconds..."))
            logger.error({'type': 'bot_fatal', 'error': str(e)})
            sleep(5)
