import re
import telebot
from config import BOT_TOKEN, knownUsers, antispam


def get_bot(parse_mode="HTML"):
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode=parse_mode)
    return bot


def listener(messages):
    for m in messages:
        log = {
            'cid': m.from_user.id,
            'username': m.from_user.username,
            'type': 'text',
            'text': m.text
        }
        if check_spam(m):
            continue
        print(log)


min_spam_delay = 1
freeze_time = 5
max_attempts = 10


def check_spam(message):
    cid = message.from_user.id
    try:
        date = message.date
    except:
        date = message.message.date

    if cid not in antispam:
        antispam[cid] = {
            'last_time': date,
            'attempts': 1,
            'is_block': False,
            'unblock_time': 0
        }

    else:
        if date - antispam[cid]['last_time'] < min_spam_delay:
            antispam[cid]['attempts'] += 1
            antispam[cid]['date'] = date

            if antispam[cid]['attempts'] >= max_attempts:
                antispam[cid]['is_block'] = True
                antispam[cid]['unblock_time'] = date + min_spam_delay

        else:
            antispam[cid]['attempts'] = 1
            antispam[cid]['last_time'] = date

    if antispam[cid]['is_block']:
        if antispam[cid]['unblock_time'] < date:
            antispam[cid]['is_block'] = False
            return 0
        else:
            return 1
    return 0
