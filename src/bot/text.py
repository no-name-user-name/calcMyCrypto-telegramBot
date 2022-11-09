import asyncio

from config import adminList, userStep, dtd
from src.async_req import multi_requests_balance
from src.bot.base_functions import get_bot, check_spam
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.bot import long_text as lt
from src.tools import get_req, async_get_req
from src import db
from tokens_config import tokens, TokenData

bot = get_bot()


def handler(m):
    cid = m.chat.id
    step = userStep[cid]
    text: str = m.text
    entities = m.entities

    if check_spam(m):
        return

    bot.delete_message(cid, m.message_id)

    if step == 'ANONS_SET_UP':
        userStep[cid] = f'{step}_OK'
        bot2 = get_bot(parse_mode=None)
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton('📢 Отправить', callback_data='send_anons'))
        markup.row(InlineKeyboardButton('⬅️ Назад', callback_data='anons'))
        bot2.edit_message_caption(text=text, chat_id=cid, entities=entities, message_id=dtd[cid]['mid'],
                                  reply_markup=markup)

    elif step == 'user_connect_token':
        markup = InlineKeyboardMarkup()

        try:
            amount = float(text)
            db.add_user_token(cid, dtd[cid]['token_name'], amount)

        except Exception as e:
            address = text
            token: TokenData = [n for n in tokens if n.name == dtd[cid]['token_name']][0]
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                multi_requests_balance(
                    user_tokens=[{'id': 1, 'token_name': token.name,
                                  'chat_id': cid, 'amount': 0, 'watch_address': address}], tokens_data=tokens))

            if result == [None]:
                msg = lt.simple_msg('❗️ Ошибка данных:', '')
                markup.row(InlineKeyboardButton('⬅️ Назад', callback_data='connect_token_menu'))
                bot.edit_message_caption(msg, chat_id=cid, message_id=dtd[cid]['mid'], reply_markup=markup)
                return

            db.add_user_token(cid, dtd[cid]['token_name'], result[0]['balance'], watch_address=address)

        msg = lt.simple_msg('✅ Токен добавлен', '')
        markup.row(InlineKeyboardButton('⬅️ Назад', callback_data='briefcase'))
        bot.edit_message_caption(msg, chat_id=cid, message_id=dtd[cid]['mid'], reply_markup=markup)
        userStep[cid] = f'{step}_OK'
