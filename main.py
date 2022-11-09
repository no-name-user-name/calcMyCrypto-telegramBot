import threading

import src.bot as bot
from src import db
from src.loops import price_parser, parse_addresses_balance, parse_addresses_stake, parse_addresses_rewards

print('[*] Bot Start')

db.init()
threading.Thread(target=price_parser).start()
threading.Thread(target=parse_addresses_balance).start()
threading.Thread(target=parse_addresses_stake).start()
threading.Thread(target=parse_addresses_rewards).start()
bot.start()



