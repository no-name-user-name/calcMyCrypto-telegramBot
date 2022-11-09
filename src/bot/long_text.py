def simple_msg(title, msg):
    if msg != '':
        msg = '➖➖➖➖➖➖➖➖➖➖➖\n' + msg
    return f"""
<b>{title}</b>
{msg}
"""


def start_message(name):
    return f"""
Hi, {name}!

The bot is made to calculate the total balance of all your tokens.
"""