from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import ethbalance.utils as utils
from ethbalance.config import LENGTH_WALLET_ADDRESS
from ethbalance.database import MongoDatabase


# bot's update error handler
def error(bot, update, error_msg):

    utils.module_logger.warning('Update caused error "%s"', error)
    # TODO send a message for the admin


################################################################################################################
####################   send a start message, command handler   #################################################
################################################################################################################
def start(bot, update):

    # logging
    utils.send_to_log(update)

    if update.effective_message.from_user.username:
        usr_username = '@' + update.effective_message.from_user.username

    usr_chat_id = update.effective_message.chat_id

    usr_lang_code = update.effective_message.from_user.language_code

    # create user object from BD Mongo
    mongo = MongoDatabase()

    if not mongo.connectionOK:
        # TODO send a message for admin for DB error
        return

    user_object = mongo.get_user(usr_chat_id)

    if user_object:
        user_object['usr_bot_state'] = ''
        user_object['usr_lang_code'] = usr_lang_code
        mongo.edit_user(user_object)

    else:
        mongo.insert_user(usr_chat_id, usr_username, usr_lang_code)

    # check user language and set variable 'usr_language_array'
    usr_language_array = utils.set_usr_language_array(usr_lang_code)

    # "Main Menu" user keyboard "by default"
    usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code)

    bot.send_message(chat_id=usr_chat_id, text=usr_language_array['TXT_START_MSG'],
                     parse_mode="Markdown", reply_markup=usr_keyboard)


################################################################################################################
####################   send an admin message, command handler   ################################################
################################################################################################################
def admin_say(bot, update):

    # logging
    utils.send_to_log(update)

    # TODO bot's command to send a message for all users


################################################################################################################
############################   common text messages handler  ###################################################
################################################################################################################
def text_handler(bot, update):

    # logging
    utils.send_to_log(update, 'message')

    usr_msg_text = update.effective_message.text
    usr_chat_id = update.effective_message.chat_id
    usr_lang_code = update.effective_message.from_user.language_code

    # create user object from BD Mongo
    mongo = MongoDatabase()

    if not mongo.connectionOK:
        # TODO send a message for admin for DB error
        return

    user_object = mongo.get_user(usr_chat_id)

    if not user_object:
        txt_response = utils.set_usr_language_array(usr_lang_code)['TXT_USE_START_BUTTON']
        bot.send_message(chat_id=usr_chat_id, text=txt_response,
                         parse_mode="Markdown", reply_markup=utils.set_user_usr_keyboard(usr_lang_code))
        return

    txt_response = ''
    usr_msg_id_to_edit = ''

    # to read from user_object its bot state
    current_usr_bot_state = user_object['usr_bot_state']

    # usr_lang_code functions
    if not usr_lang_code:
        usr_lang_code = user_object['usr_lang_code']
        mongo.edit_user(user_object)

    elif usr_lang_code and usr_lang_code != user_object['usr_lang_code']:
        user_object['usr_lang_code'] = usr_lang_code
        mongo.edit_user(user_object)

    # check user language and set global variable 'usr_language_array'
    usr_language_array = utils.set_usr_language_array(usr_lang_code)

    # "Main Menu" user keyboard "by default"
    usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MAIN MENU LOGICAL CONDITION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # pressed button "GO_BACK" from any page ---->  "Main Menu" page
    if usr_language_array['MENU_GO_BACK'].upper() == usr_msg_text.upper():

        user_object['usr_bot_state'] = ''
        mongo.edit_user(user_object)

        txt_response = usr_language_array['MENU_GO_BACK']

    # pressed button "ADD_ETH_WALLET" from "Main Menu" ---->  'wait_wallet_address' page
    elif usr_language_array['MENU_ADD_ETH_WALLET'].upper() == usr_msg_text.upper():

        # checks if user has a gap in NUMBER_OF_WALLETS to add one more
        if utils.is_full_wallets_list(user_object):

            user_object['usr_bot_state'] = 'wait_wallet_address'
            mongo.edit_user(user_object)

            usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code, 'go_back')
            txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET']

        else:

            txt_response = usr_language_array['TXT_ADD_ETH_NAME_WALLETS_FULL']

    # from "wait_wallet_address" input page ---->  * Main Menu" page if wallet address was added
    #                                         ---->  * repeat "wait_wallet_address" input page
    elif current_usr_bot_state == 'wait_wallet_address' and usr_msg_text \
            and usr_msg_text.upper() != usr_language_array['MENU_ADD_ETH_WALLET'].upper():

        # checks if user has a gap in NUMBER_OF_WALLETS to add one more
        if utils.is_full_wallets_list(user_object):

            # checks the wallet address length permitted
            if len(usr_msg_text) == LENGTH_WALLET_ADDRESS:

                # checks the wallet address format "0x" + 40 alphanumeric characters
                if utils.is_valid_eth_address(usr_msg_text):

                    usr_new_wallet_address = usr_msg_text

                    if usr_new_wallet_address in user_object['usr_wallets']:

                        user_object['usr_bot_state'] = ''

                        txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_EXISTS']

                    else:

                        user_object['usr_bot_state'] = ''
                        user_object['usr_wallets'].append(usr_new_wallet_address)

                        txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_ADDED']

                        # check wallet balance now
                        txt_response += utils.check_address(usr_lang_code, usr_new_wallet_address)

                    mongo.edit_user(user_object)

                else:

                    usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code, 'go_back')
                    txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_WRONG']

            else:

                usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code, 'go_back')
                txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_WRONG']

        else:

            user_object['usr_bot_state'] = ''
            mongo.edit_user(user_object)

            txt_response = usr_language_array['TXT_ADD_ETH_NAME_WALLETS_FULL']

    # pressed button "MENU_DEL_ETH_WALLET" from "Main Menu" page ---->  stay here
    elif usr_language_array['MENU_DEL_ETH_WALLET'].upper() == usr_msg_text.upper():

        if len(user_object['usr_wallets']) > 0:

            txt_response = usr_language_array['TXT_DEL_ETH_WALLET']

            keyboard = []
            i = 0

            for wallet in user_object['usr_wallets']:
                keyboard.append([InlineKeyboardButton(
                    wallet, callback_data=wallet)])
                i += 1

            usr_keyboard = InlineKeyboardMarkup(keyboard)

            user_object['usr_bot_state'] = 'wait_to_del_wallet_address'

            mongo.edit_user(user_object)

        else:

            txt_response = usr_language_array['TXT_NO_ETH_WALLET']

    # from "MENU_DEL_ETH_WALLET" page recieve inline ---->  process delete wallet from BD
    elif user_object['usr_bot_state'] == 'wait_to_del_wallet_address'\
            and update.callback_query:

        query_data = update.callback_query.data

        if query_data and utils.is_valid_eth_address(query_data):

            if query_data in user_object['usr_wallets']:

                user_object['usr_wallets'].remove(query_data)

                if len(user_object['usr_wallets']) > 0:

                    txt_response = usr_language_array['TXT_DEL_ETH_WALLET']

                    keyboard = []
                    i = 0

                    for wallet in user_object['usr_wallets']:
                        keyboard.append([InlineKeyboardButton(
                            wallet, callback_data=wallet)])
                        i += 1

                    usr_keyboard = InlineKeyboardMarkup(keyboard)

                else:

                    user_object['usr_bot_state'] = ''

                    txt_response = usr_language_array['TXT_NO_ETH_WALLET']

                    usr_keyboard = ''

                mongo.edit_user(user_object)

                usr_msg_id_to_edit = update.callback_query.message.message_id

    # pressed button "MENU_CHECK_ALL_BALANCE" from "Main Menu" page ---->  stay here
    elif usr_language_array['MENU_CHECK_ALL_BALANCE'].upper() == usr_msg_text.upper():

        if len(user_object['usr_wallets']) > 0:

            txt_response = '💲💲💲 *' + usr_language_array['MENU_CHECK_ALL_BALANCE'] \
                           + ':*\n`-------------------------`\n'

            for usr_wallet_address in user_object['usr_wallets']:
                txt_response += utils.check_address(usr_lang_code, usr_wallet_address)

        else:
            txt_response = usr_language_array['TXT_NO_ETH_WALLET']

            user_object['usr_bot_state'] = ''
            mongo.edit_user(user_object)

    elif usr_language_array['MENU_BOT_OPTIONS'].upper() == usr_msg_text.upper():

        txt_response = utils.show_bot_options()
        usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code)

    # pressed button "MENU_SHARE_BOT" from "Main Menu" page ---->  stay here
    #                                                              with inline menu showing
    elif usr_language_array['MENU_SHARE_BOT'].upper() == usr_msg_text.upper():

        txt_response = usr_language_array['TXT_SHARE_BOT']

        usr_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=usr_language_array['LINK_SHARE_BOT'],
                                      switch_inline_query=usr_language_array['LINK_TEXT_SHARE_BOT'])]
            ],
        )

    # this is a default condition if there is no correct command for the bot
    else:

        user_object['usr_bot_state'] = ''
        mongo.edit_user(user_object)

        txt_response = usr_language_array['TXT_USE_KEYBOARD']

    # to send a message for user
    if update and txt_response:

        # this is a case of edit a message (InlineKeyboardMarkup --> InlineKeyboardButton's)
        if usr_msg_id_to_edit:

            bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  text=txt_response, message_id=usr_msg_id_to_edit,
                                  parse_mode="Markdown", reply_markup=usr_keyboard)

        else:

            bot.send_message(chat_id=usr_chat_id, text=txt_response,
                             parse_mode="Markdown", reply_markup=usr_keyboard)
