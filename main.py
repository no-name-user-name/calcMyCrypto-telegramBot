import threading

import src.bot as bot
from src import db
from src.loops import loop_parsers

print('[*] Bot Start')

db.init()
threading.Thread(target=loop_parsers).start()
bot.start()



