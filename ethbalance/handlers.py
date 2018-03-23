import os
import requests

from ethbalance.languages import *
from ethbalance.reply_markups import reply_markup_en, reply_markup_es, reply_markup_ru

usr_language_array = ENGLISH
usr_keyboard = reply_markup_en


def get_usr_language_array():
    return usr_language_array


# !important: this import must be after of the variable "usr_language_array",
# for avoid a circular dependency, because "usr_language_array" is used in "ethbalance.utils"
from ethbalance.utils import *


# check what is users telegram language code
def set_user_language(language_code):

    global usr_language_array
    global usr_keyboard

    if language_code == 'ru':
        usr_language_array = RUSSIAN
        usr_keyboard = reply_markup_ru

    elif language_code == 'es':
        usr_language_array = SPANISH
        usr_keyboard = reply_markup_es


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

    # TODO Here have to use a new language definition function
    # TODO language_code = str(update.message.from_user.language_code)

    text_response = '🇷🇺 Привет, ' + usr_name + '. Я твой Эфереум Баланс Бот! Помогу тебе быть в курсе' \
                    ' актуального баланса Эфереума и ERC-20 токенов на твоём кошельке' \
                    '\n\n🇬🇧 Hello, ' + usr_name + '. I am your Ethereum Balance Bot! I would help you' \
                    ' to stay informed about your Ethereum and ERC-20 tokens wallet balance'

    # TODO send to user a correct keyboard
    # bot.send_message(usr_chat_id, text_response, parse_mode="Markdown", reply_markup=reply_markup_p1)
    bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")


# send a start message, command handler
def admin_say(bot, update):

    # logging
    send_to_log(update)

    usr_name = update.message.from_user.first_name

    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name

    usr_chat_id = update.effective_message.chat_id

    # TODO Here have to use a new language definition function
    # TODO language_code = str(update.message.from_user.language_code)

    text_response = 'admin say here!'

    # TODO send to user a correct keyboard
    # bot.send_message(usr_chat_id, text_response, parse_mode="Markdown", reply_markup=reply_markup_p1)
    bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")


# text messages handler for send users keyboard for all users
def text_input(bot, update):

    global usr_language_array
    global usr_keyboard

    # logging
    send_to_log(update, 'message')

    # check users language and set global variables 'usr_language_array' and 'usr_keyboard'
    set_user_language(update.effective_message.from_user.language_code)

    usr_msg_text = update.effective_message.text
    usr_chat_id = update.effective_message.chat_id

    if usr_language_array['MENU_ADD_ETH_WALLET'].upper() == usr_msg_text.upper():
        txt_response = add_eth_wallet()

    elif usr_language_array['MENU_DEL_ETH_WALLET'].upper() == usr_msg_text.upper():
        txt_response = del_eth_wallet()

    elif usr_language_array['MENU_CHECK_ALL_BALANCE'].upper() == usr_msg_text.upper():
        txt_response = check_balance()

    elif usr_language_array['MENU_BOT_OPTIONS'].upper() == usr_msg_text.upper():
        txt_response = show_bot_options()

    elif usr_language_array['MENU_SHARE_BOT'].upper() == usr_msg_text.upper():
        share_bot()
        txt_response = usr_language_array['TXT_SHARE_BOT']

    elif usr_language_array['MENU_FEEDBACK'].upper() == usr_msg_text.upper():
        send_feedback()
        txt_response = usr_language_array['TXT_FEEDBACK']

    else:
        txt_response = usr_language_array['TXT_USE_KEYBOARD']

    if update and txt_response:
        bot.send_message(chat_id=usr_chat_id, text=txt_response,
                         parse_mode="Markdown", reply_markup=usr_keyboard)
