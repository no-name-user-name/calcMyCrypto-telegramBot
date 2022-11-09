import os
from datetime import datetime
from src import db
from config import userStep, dtd
from src.bot import menu


def get_bot_input_docs(bot):
    @bot.message_handler(content_types=['document'])
    def photo(m):
        cid = m.from_user.id
        mid = m.message_id 
        bot.delete_message(cid, mid)
        step = userStep[cid]