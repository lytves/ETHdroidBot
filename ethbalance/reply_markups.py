from telegram import KeyboardButton, ReplyKeyboardMarkup
from ethbalance.languages import *

# create userkeyboard, resize = true, autohide=false
keyboard_ru = [[KeyboardButton(RUSSIAN['MENU_CHECK_ALL_BALANCE']), KeyboardButton(RUSSIAN['MENU_ADD_ETH_WALLET'])],
            [KeyboardButton(RUSSIAN['MENU_BOT_OPTIONS']), KeyboardButton(RUSSIAN['MENU_DEL_ETH_WALLET'])],
            [KeyboardButton(RUSSIAN['MENU_SHARE_BOT']), KeyboardButton(RUSSIAN['MENU_FEEDBACK'])]]

keyboard_es = [[KeyboardButton(SPANISH['MENU_CHECK_ALL_BALANCE']), KeyboardButton(SPANISH['MENU_ADD_ETH_WALLET'])],
            [KeyboardButton(SPANISH['MENU_BOT_OPTIONS']), KeyboardButton(SPANISH['MENU_DEL_ETH_WALLET'])],
            [KeyboardButton(SPANISH['MENU_SHARE_BOT']), KeyboardButton(SPANISH['MENU_FEEDBACK'])]]

keyboard_en = [[KeyboardButton(ENGLISH['MENU_CHECK_ALL_BALANCE']), KeyboardButton(ENGLISH['MENU_ADD_ETH_WALLET'])],
            [KeyboardButton(ENGLISH['MENU_BOT_OPTIONS']), KeyboardButton(ENGLISH['MENU_DEL_ETH_WALLET'])],
            [KeyboardButton(ENGLISH['MENU_SHARE_BOT']), KeyboardButton(ENGLISH['MENU_FEEDBACK'])]]

reply_markup_ru = ReplyKeyboardMarkup(keyboard_ru, True, False)
reply_markup_es = ReplyKeyboardMarkup(keyboard_es, True, False)
reply_markup_en = ReplyKeyboardMarkup(keyboard_en, True, False)