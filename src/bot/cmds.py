import random
import string

from config import userStep, knownUsers, dtd
from src import db
from src.bot import menu


def start(m):
    cid = m.from_user.id
    first_name = m.from_user.first_name
    username = m.from_user.username
    last_name = m.from_user.last_name
    language_code = m.from_user.language_code
    is_premium = m.from_user.is_premium

    if cid not in knownUsers:
        reflink = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        db.add_user(cid, first_name, username, last_name, language_code, reflink, is_premium)
        knownUsers[cid] = 1
        userStep[cid] = 'HOME'
        dtd[cid] = {}

    menu.main(m)
