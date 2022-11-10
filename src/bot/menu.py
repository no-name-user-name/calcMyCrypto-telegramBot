from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import chunks

from src import db
from config import userStep, adminList, dtd
from src.bot import long_text as lt
from src.bot.base_functions import get_bot, check_spam
from tokens_config import tokens, TokenData

bot = get_bot()


def main(m, mid=None):
    if check_spam(m):
        return

    cid = m.from_user.id
    name = m.from_user.first_name

    userStep[cid] = 'main'

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Tokens', callback_data='briefcase'))

    msg = lt.start_message(name)

    if mid is None:

        with open('data/main.jpg', 'rb') as img:
            bot.send_photo(cid, img, caption=msg, reply_markup=markup, disable_notification=True)

    else:
        bot.edit_message_caption(msg, cid, mid, reply_markup=markup)


def briefcase(call):
    cid = call.from_user.id
    userStep[cid] = 'briefcase'
    user_tokens = db.get_user_tokens(cid)

    k = []
    args = []
    row_width = 3

    tc = 0

    t_balance = 0
    t_stake = 0
    t_rewards = 0
    t_stable = 0

    sort_data = []
    for ut in user_tokens:
        token_data: TokenData = [n for n in tokens if n.name == ut['token_name']][0]

        t_balance += token_data.price * ut['available_balance']
        t_stake += token_data.price * ut['staked_balance']
        t_rewards += token_data.price * ut['rewards_balance']

        if token_data.name in ['busd_bep2']:
            t_stable += token_data.price * ut['available_balance']

        sort_data.append({
            'balance': token_data.price * (ut['available_balance'] + ut['staked_balance'] + ut['rewards_balance']),
            'symbol': token_data.symbol,
            'id': ut["id"]
        })
        tc += 1

    sort_list = sorted(sort_data, key=lambda d: d['balance'], reverse=True)
    for el in sort_list:
        args.append(InlineKeyboardButton(
            f"{el['symbol']}: ${format(el['balance'], f'.2f')}", callback_data=f'user_token-{el["id"]}'))

    for row in chunks(args, row_width):
        button_array = [button for button in row]
        k.append(button_array)

    k.append([InlineKeyboardButton("🔄 Update", callback_data=f'refresh_briefcase')])
    k.append([InlineKeyboardButton("◀ Back", callback_data=f'main_menu'),
              InlineKeyboardButton("*️⃣ Add", callback_data=f'connect_token_menu')])

    markup = InlineKeyboardMarkup(k)

    full_balance = t_balance+t_stake+t_rewards

    t_balance_percents = round((float(t_balance * 100 / full_balance)), 2)
    t_stake_percents = round(float(t_stake * 100 / full_balance), 2)
    t_rewards_percents = round(float(t_rewards * 100 / full_balance), 2)
    t_stable_percents = round(float(t_stable * 100 / full_balance), 2)

    t_crypto = full_balance - t_stable - t_stake - t_rewards
    t_crypto_percents = round(float(t_crypto * 100 / full_balance), 2)

    if tc > 0:
        msg = lt.simple_msg('💎 Your tokens',
                            f'🔸 Total balance: ${format(full_balance, f".2f")}\n\n'
                            f'▫️ Available: ${format(t_balance, f".2f")} ({t_balance_percents}%)\n'
                            f' ┕ Crypto: ${format(t_crypto, f".2f")} ({t_crypto_percents}%)\n'
                            f' ┕ Stable: ${format(t_stable, f".2f")} ({t_stable_percents}%)\n'
                            f'▫️ In stake: ${format(t_stake, f".2f")} ({t_stake_percents}%)\n'
                            f'▫️ Rewards: ${format(t_rewards, f".2f")} ({t_rewards_percents}%)\n')

    else:
        msg = lt.simple_msg('Your tokens', 'Tokens not yet added')

    bot.edit_message_caption(msg, cid, call.message.id, reply_markup=markup)


def connect_token_menu(call):
    cid = call.from_user.id
    userStep[cid] = 'connect_token_menu'

    k = []
    args = []
    row_width = 3

    for t in tokens:
        args.append(InlineKeyboardButton(t.name, callback_data=f'token_connect-{t.name}'))

    for row in chunks(args, row_width):
        button_array = [button for button in row]
        k.append(button_array)

    k.append([InlineKeyboardButton("◀️ Назад", callback_data=f'briefcase')])

    markup = InlineKeyboardMarkup(k)

    msg = lt.simple_msg('List of available tokens:', '')
    bot.edit_message_caption(msg, cid, call.message.id, reply_markup=markup)


def user_token_menu(call, token_id):
    cid = call.from_user.id
    userStep[cid] = 'user_token_menu'

    ut = db.get_user_token_by_id(token_id)

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("◀ Back", callback_data='briefcase'),
               InlineKeyboardButton("❌ Delete", callback_data=f'delete_user_token-{token_id}'))

    td: TokenData = [n for n in tokens if n.name == ut['token_name']][0]

    abusd = '$' + format(float(ut['available_balance']) * td.price, f'.2f')
    sbusd = '$' + format(float(ut['staked_balance']) * td.price, f'.2f')
    rbusd = '$' + format(float(ut['rewards_balance']) * td.price, f'.2f')

    denom = td.symbol

    msg = f"🔸 Market price: 1 {denom} = ${td.price}\n\n" \
          f"▫️ <b>Available balance:</b> \n" \
          f" ┕ {ut['available_balance']} {denom} ({abusd})\n"

    if td.is_pos:
        msg += f"▫️ <b>In stake:</b> \n" \
               f" ┕ {ut['staked_balance']} {denom} ({sbusd})\n" \
               f"▫️ <b>Rewards:</b> \n" \
               f" ┕ {ut['rewards_balance']} {denom} ({rbusd})\n"

    msg += f"\n<b>Address:</b> \n" \
           f"<code>{ut['watch_address']}</code>"

    msg = lt.simple_msg(f'🔹 Token {ut["token_name"]} #{ut["id"]}:', msg)

    bot.edit_message_caption(msg, cid, call.message.id, reply_markup=markup)


def setup_new_token(call):
    cid = call.from_user.id
    userStep[cid] = 'setup_new_token'

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("◀ Back", callback_data='connect_token_menu'))

    msg = lt.simple_msg('Setting up a new token:', lt.new_token_info())

    bot.edit_message_caption(msg, cid, call.message.id, reply_markup=markup)
    dtd[cid]['mid'] = call.message.id


def user_connect_token(call, token_name):
    cid = call.from_user.id
    userStep[cid] = 'user_connect_token'

    token: TokenData = [n for n in tokens if n.name == token_name][0]

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("◀ Назад", callback_data='connect_token_menu'))

    msg = lt.simple_msg(f'Adding a token "{token.name}"',
                        'Set the number of tokens, or specify the wallet address')

    bot.edit_message_caption(msg, cid, call.message.id, reply_markup=markup)
    dtd[cid]['mid'] = call.message.id
    dtd[cid]['token_name'] = token_name
