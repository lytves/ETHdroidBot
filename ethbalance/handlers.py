from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ethbalance.languages import *
from ethbalance.reply_markups import reply_markup_en, reply_markup_es, reply_markup_ru, \
    reply_markup_back_en, reply_markup_back_es, reply_markup_back_ru

usr_language_array = ENGLISH
usr_keyboard = reply_markup_en


def get_usr_language_array():
    return usr_language_array


# !important: this import must be after of the variable "usr_language_array",
# for avoid a circular dependency, because "usr_language_array" is used in "ethbalance.utils"
from ethbalance.utils import *

last_menu_page = ''


# check what is users telegram language code
def set_usr_language_array(language_code):
    global usr_language_array

    if language_code == 'ru' or language_code == 'ru-RU':
        usr_language_array = RUSSIAN

    elif language_code == 'es' or language_code == 'es-ES':
        usr_language_array = SPANISH


# check what is users telegram language code
def set_user_usr_keyboard(language_code, usr_keyboard_type=''):
    global usr_keyboard

    # print(language_code)

    if usr_keyboard_type == 'go_back':
        if language_code == 'ru' or language_code == 'ru-RU':
            usr_keyboard = reply_markup_back_ru

        elif language_code == 'es' or language_code == 'es-ES':
            usr_keyboard = reply_markup_back_es

        else:
            usr_keyboard = reply_markup_back_en

    else:
        if language_code == 'ru' or language_code == 'ru-RU':
            usr_keyboard = reply_markup_ru

        elif language_code == 'es' or language_code == 'es-ES':
            usr_keyboard = reply_markup_es

        else:
            usr_keyboard = reply_markup_en


# bot's update error handler
def error(bot, update, error_msg):
    module_logger.warning('Update caused error "%s"', error)

    # TODO send a message for the admin with error from here


# send a start message, command handler
def start(bot, update):
    # logging
    send_to_log(update)

    usr_name = update.message.from_user.first_name

    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name

    usr_chat_id = update.effective_message.chat_id

    # TODO I should use the language definition function

    text_response = '🇷🇺 Привет, ' + usr_name + '. Я твой Эфириум Баланс Бот! Помогу тебе быть в курсе' \
                                                 ' актуального баланса Эфириум и ERC-20 токенов на твоём кошельке' \
                                                 '\n\n🇬🇧 Hello, ' + usr_name + '. I am your Ethereum Balance Bot! I would help you' \
                                                                                 ' to stay informed about your Ethereum and ERC-20 tokens wallet balance'

    # TODO send to user a correct keyboard
    bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")


# send a start message, command handler
def admin_say(bot, update):
    # logging
    send_to_log(update)

    usr_name = update.message.from_user.first_name

    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name

    usr_chat_id = update.effective_message.chat_id

    # TODO I should use the language definition function

    text_response = 'admin say here!'

    # TODO send to user a correct keyboard
    bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")


# general text messages handler
def text_input(bot, update):
    global usr_language_array
    global usr_keyboard
    global last_menu_page

    print('last_menu_page: ' + last_menu_page)

    # logging
    send_to_log(update, 'message')

    # check user language and set global variable 'usr_language_array'
    usr_lang_code = update.effective_message.from_user.language_code
    set_usr_language_array(usr_lang_code)

    usr_msg_text = update.effective_message.text
    usr_chat_id = update.effective_message.chat_id

    # print(usr_lang_code)
    # print(usr_msg_text.upper())
    # print(usr_language_array['MENU_ADD_ETH_WALLET'].upper())

    if usr_language_array['MENU_GO_BACK'].upper() == usr_msg_text.upper() \
            and last_menu_page == 'add_name_wallet':

        last_menu_page = ''

        txt_response = add_eth_wallet(last_menu_page)
        set_user_usr_keyboard(usr_lang_code)

        print(last_menu_page)

    elif usr_language_array['MENU_ADD_ETH_WALLET'].upper() == usr_msg_text.upper() \
            or last_menu_page == 'add_address_wallet':

        last_menu_page = 'add_name_wallet'

        txt_response = add_eth_wallet(last_menu_page)
        set_user_usr_keyboard(usr_lang_code, 'go_back')

        print(last_menu_page)

    elif last_menu_page == 'add_name_wallet':

        last_menu_page = 'add_address_wallet'

        txt_response = add_eth_wallet(last_menu_page)
        set_user_usr_keyboard(usr_lang_code, 'go_back')

        print(last_menu_page)

    elif usr_language_array['MENU_DEL_ETH_WALLET'].upper() == usr_msg_text.upper():

        last_menu_page = 'del_wallet'
        txt_response = del_eth_wallet()
        set_user_usr_keyboard(usr_lang_code, 'go_back')

        print(last_menu_page)

    elif usr_language_array['MENU_CHECK_ALL_BALANCE'].upper() == usr_msg_text.upper():

        txt_response = check_balance()
        set_user_usr_keyboard(usr_lang_code)

    elif usr_language_array['MENU_BOT_OPTIONS'].upper() == usr_msg_text.upper():

        txt_response = show_bot_options()
        set_user_usr_keyboard(usr_lang_code)

        print(last_menu_page)

    elif usr_language_array['MENU_SHARE_BOT'].upper() == usr_msg_text.upper():

        last_menu_page = 'share_bot'

        txt_response = usr_language_array['TXT_SHARE_BOT']

        usr_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=usr_language_array['LINK_SHARE_BOT'],
                                      switch_inline_query=usr_language_array['LINK_TEXT_SHARE_BOT'])]
            ],
        )

        print(last_menu_page)

    elif usr_language_array['MENU_FEEDBACK'].upper() == usr_msg_text.upper():

        send_feedback()

        txt_response = usr_language_array['TXT_FEEDBACK']
        set_user_usr_keyboard(usr_lang_code)

        print(last_menu_page)

    elif usr_language_array['MENU_GO_BACK'].upper() == usr_msg_text.upper():

        txt_response = usr_language_array['MENU_GO_BACK']
        set_user_usr_keyboard(usr_lang_code)

        print(last_menu_page)

    else:

        txt_response = usr_language_array['TXT_USE_KEYBOARD']
        set_user_usr_keyboard(usr_lang_code)

        print(last_menu_page)

    if update and txt_response:
        bot.send_message(chat_id=usr_chat_id, text=txt_response,
                         reply_markup=usr_keyboard)
