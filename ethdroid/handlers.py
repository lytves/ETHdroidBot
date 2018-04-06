from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction

import ethdroid.utils as utils
from ethdroid.database import MongoDatabase


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

    usr_username = ''
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
        print('DB don\'t connect successfully')
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

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # from "wait_wallet_address" input page ---->  * Main Menu" page if wallet address was added
    #                                         ---->  * repeat "wait_wallet_address" input page
    elif current_usr_bot_state == 'wait_wallet_address' and usr_msg_text \
            and usr_msg_text.upper() != usr_language_array['MENU_ADD_ETH_WALLET'].upper():

        # checks if user has a gap in NUMBER_OF_WALLETS to add one more
        if utils.is_full_wallets_list(user_object):

            # checks the wallet address length permitted and
            # checks the wallet address format "0x" + 40 alphanumeric characters
            if utils.is_valid_eth_address(usr_msg_text):

                usr_new_wallet_address = usr_msg_text

                # to check the address is already in BD
                exist_db_address_wallet = False

                for db_address_wallet in user_object['usr_wallets']:

                    if db_address_wallet['address'] == usr_new_wallet_address:

                        exist_db_address_wallet = True

                        txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_EXISTS']

                        break

                if not exist_db_address_wallet:

                    # to notify a user "printing..." on waiting response
                    bot.send_chat_action(chat_id=usr_chat_id, action=ChatAction.TYPING)

                    # the response from API with address all info
                    usr_wallet_api_dict = utils.api_check_balance(usr_new_wallet_address)

                    # here write balance of new added address ETH and tokens to BD
                    if usr_wallet_api_dict:

                        usr_wallet = {"address": usr_new_wallet_address,
                                      "balance": usr_wallet_api_dict['ETH']['balance'],
                                      "tokens": []}

                        # address has a tokens
                        if 'tokens' in usr_wallet_api_dict:

                            tokens = []

                            for token in usr_wallet_api_dict['tokens']:

                                tokens.append({"address": token['tokenInfo']['address'],
                                               "symbol": token['tokenInfo']['symbol'],
                                               "decimals": token['tokenInfo']['decimals'],
                                               "balance": token['balance']})

                            usr_wallet.update({"tokens": tokens})

                        # general block code if wallet added
                        txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_ADDED']

                        # check wallet balance now - pass here the response from API completed
                        txt_response += utils.text_wallet_info(usr_lang_code, usr_wallet_api_dict)

                        user_object['usr_wallets'].append(usr_wallet)
                        user_object['usr_bot_state'] = ''
                        mongo.edit_user(user_object)

            else:

                usr_keyboard = utils.set_user_usr_keyboard(usr_lang_code, 'go_back')
                txt_response = usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET_WRONG']

        else:

            user_object['usr_bot_state'] = ''
            mongo.edit_user(user_object)

            txt_response = usr_language_array['TXT_ADD_ETH_NAME_WALLETS_FULL']

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # pressed button "MENU_DEL_ETH_WALLET" from "Main Menu" page ---->  stay here
    elif usr_language_array['MENU_DEL_ETH_WALLET'].upper() == usr_msg_text.upper():

        if len(user_object['usr_wallets']) > 0:

            txt_response = usr_language_array['TXT_DEL_ETH_WALLET']

            keyboard = []
            i = 0

            for db_address_wallet in user_object['usr_wallets']:

                keyboard.append([InlineKeyboardButton(db_address_wallet['address'],
                                                      callback_data=db_address_wallet['address'])])
                i += 1

            usr_keyboard = InlineKeyboardMarkup(keyboard)

            user_object['usr_bot_state'] = 'wait_to_del_wallet_address'
            mongo.edit_user(user_object)

        else:

            txt_response = usr_language_array['TXT_NO_ETH_WALLET']

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # from "MENU_DEL_ETH_WALLET" page with inline "delete menu" ---->  process delete wallet from BD
    elif user_object['usr_bot_state'] == 'wait_to_del_wallet_address'\
            and update.callback_query:

        address_wallet = update.callback_query.data

        if address_wallet and utils.is_valid_eth_address(address_wallet):

            for db_address_wallet in user_object['usr_wallets'][:]:

                if address_wallet == db_address_wallet['address']:

                    user_object['usr_wallets'].remove(db_address_wallet)

                    break

            if len(user_object['usr_wallets']) > 0:

                txt_response = usr_language_array['TXT_DEL_ETH_WALLET']

                keyboard = []
                i = 0

                for db_address_wallet in user_object['usr_wallets']:

                    keyboard.append([InlineKeyboardButton(db_address_wallet['address'],
                                    callback_data=db_address_wallet['address'])])

                    i += 1

                usr_keyboard = InlineKeyboardMarkup(keyboard)

            else:

                user_object['usr_bot_state'] = ''

                usr_keyboard = ''
                txt_response = usr_language_array['TXT_NO_ETH_WALLET']

            # must do it for both case of if..else
            mongo.edit_user(user_object)

            usr_msg_id_to_edit = update.callback_query.message.message_id

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # pressed button "MENU_CHECK_ALL_BALANCE" from "Main Menu" page ---->  stay here
    elif usr_language_array['MENU_CHECK_ALL_BALANCE'].upper() == usr_msg_text.upper():

        if len(user_object['usr_wallets']) > 0:

            # to notify a user "printing..." on waiting response
            bot.send_chat_action(chat_id=usr_chat_id, action=ChatAction.TYPING)

            txt_response = '💲💲💲 *' + usr_language_array['MENU_CHECK_ALL_BALANCE'] \
                           + ':*\n`-------------------------`'

            i = 0
            for usr_wallet in user_object['usr_wallets'][:]:

                # the  API request to receive wallet actual balance info
                usr_wallet_api_dict = utils.api_check_balance(usr_wallet['address'])

                # here write balance of new added address ETH and tokens to BD
                if usr_wallet_api_dict:

                    # check all balances of the each wallet address in txt form - pass here the response from API completed
                    txt_response += utils.text_wallet_info(usr_lang_code, usr_wallet_api_dict)

                    # search changes in the wallets using actual info and DB infp
                    eth_wallet_changes = utils.eth_wallet_changes(usr_wallet, usr_wallet_api_dict)

                    # use case of - there is changes in wallet balances
                    if eth_wallet_changes['wallet_changes']:

                        # update BD wallet info
                        user_object['usr_wallets'][i] = eth_wallet_changes['usr_wallet']

                        # show wallet changed balances of ETH and tokens
                        txt_response += utils.text_wallet_changes(usr_language_array, eth_wallet_changes['wallet_changes'])

                # here is counter iteration !!!
                i += 1

        else:

            txt_response = usr_language_array['TXT_NO_ETH_WALLET']

        # must do it for both case of if..else
        user_object['usr_bot_state'] = ''
        mongo.edit_user(user_object)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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

        user_object['usr_bot_state'] = ''
        mongo.edit_user(user_object)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # this is a default condition if there is no correct command for the bot
    else:

        user_object['usr_bot_state'] = ''
        mongo.edit_user(user_object)

        txt_response = usr_language_array['TXT_USE_KEYBOARD']

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ sends a message for user @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    if update and txt_response:

        # this is a case of edit a message (InlineKeyboardMarkup --> InlineKeyboardButton's)
        if usr_msg_id_to_edit:

            bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  text=txt_response, message_id=usr_msg_id_to_edit,
                                  parse_mode="Markdown", reply_markup=usr_keyboard)

        else:

            bot.send_message(chat_id=usr_chat_id, text=txt_response,
                             parse_mode="Markdown", reply_markup=usr_keyboard)


################################################################################################################
############################  bot's job - ethplorer API wallets parser handler  ###################################################
################################################################################################################
def scheduler_balance_changes_check(bot, update):

    # logging
    utils.send_to_log(update, 'scheduler')

    # create user object from BD Mongo
    mongo = MongoDatabase()

    if not mongo.connectionOK:
        # TODO send a message for admin for DB error
        return

    # request all users from BD
    all_users_object = mongo.get_all_users()

    for user_object in all_users_object:

        # check user language from BD to form txt response
        usr_language_array = utils.set_usr_language_array(user_object['usr_lang_code'])

        txt_response = ''
        to_update_bd_user = False
        i = 0

        for usr_wallet in user_object['usr_wallets']:

            # the  API request to receive wallet actual balance info
            usr_wallet_api_dict = utils.api_check_balance(usr_wallet['address'])

            # here write balance of new added address ETH and tokens to BD
            if usr_wallet_api_dict:

                # search changes in the wallets using actual info and DB info
                eth_wallet_changes = utils.eth_wallet_changes(usr_wallet, usr_wallet_api_dict)

                # use case of there is changes in wallet balances
                if eth_wallet_changes['wallet_changes']:

                    if txt_response == '':

                        txt_response = usr_language_array['TXT_WALLET_UPDATES']

                    # update BD wallet info
                    user_object['usr_wallets'][i] = eth_wallet_changes['usr_wallet']
                    to_update_bd_user = True

                    # show wallet changed balances of ETH and tokens
                    txt_response += utils.text_wallet_changes(usr_language_array,
                                                              eth_wallet_changes['wallet_changes'],
                                                              usr_wallet['address'])

                # here is counter iteration !!!
                i += 1

        if to_update_bd_user:

            mongo.edit_user(user_object)

        if txt_response:
            bot.send_message(chat_id=user_object['usr_tg_id'], text=txt_response,
                             parse_mode="Markdown")
