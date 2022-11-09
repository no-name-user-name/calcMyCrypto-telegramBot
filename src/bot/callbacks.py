from src.bot.base_functions import get_bot
from src.bot import menu
from src import db

bot = get_bot()


def handlers(call):
    cid = call.from_user.id
    mid = call.message.id
    params = call.data.split('-')

    log = {
        'cid': call.from_user.id,
        'username': call.from_user.username,
        'type': 'callback',
        'callback': call.data
    }

    print(log)

    if params[0] == 'close':
        bot.delete_message(cid, mid)

    elif params[0] == 'briefcase':
        menu.briefcase(call)

    elif params[0] == 'main_menu':
        menu.main(call, mid)

    elif params[0] == 'connect_token_menu':
        menu.connect_token_menu(call)

    elif params[0] == 'user_token':
        menu.user_token_menu(call, params[1])

    elif params[0] == 'setup_new_token':
        menu.setup_new_token(call)

    elif params[0] == 'token_connect':
        menu.user_connect_token(call, params[1])

    elif params[0] == 'delete_user_token':
        db.delete_user_token(params[1])
        bot.answer_callback_query(call.id, 'Токен удалён!')
        menu.briefcase(call)

    elif params[0] == 'refresh_briefcase':
        try:
            menu.briefcase(call)
        except:
            pass





