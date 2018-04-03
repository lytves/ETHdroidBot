import requests
import logging
import re

from decimal import Decimal

from ethbalance.config import ETHPLORER_API_URL, ETHERSCAN_API_URL, LENGTH_WALLET_ADDRESS
from ethbalance.languages import *
from ethbalance.reply_markups import reply_markup_en, reply_markup_es, reply_markup_ru, \
    reply_markup_back_en, reply_markup_back_es, reply_markup_back_ru

# start logging to the file of current directory or º it to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
module_logger = logging.getLogger(__name__)

# start logging to the file with log rotation at midnight of each day
# formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
# handler = TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + '/../ethbalancebot.log',
#                                    when='midnight',
#                                    backupCount=10)
# handler.setFormatter(formatter)
# module_logger = logging.getLogger(__name__)
# module_logger.addHandler(handler)
# module_logger.setLevel(logging.INFO)
# end of log section


price_ethusd = 0.0
price_ethbtc = 0.0


# to put correct conversation/menu language
def set_usr_language_array(language_code):

    if language_code == 'ru' or language_code == 'ru-RU':
        usr_language_array = RUSSIAN

    elif language_code == 'es' or language_code == 'es-ES':
        usr_language_array = SPANISH

    else:
        usr_language_array = ENGLISH

    return usr_language_array


# to put correct keyboard language
def set_user_usr_keyboard(language_code, usr_keyboard_type=''):

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

    return usr_keyboard


# checks if user has a gap in NUMBER_OF_WALLETS to add one more
def is_full_wallets_list(user_object):

        # True when: * user has a gap in NUMBER_OF_WALLETS to add one more
        if len(user_object['usr_wallets']) < NUMBER_WALLETS:
            return True


# the functions for logging handlers
def send_to_log(update, msg_type='command'):

    if update:
        usr_message = str(update.effective_message.text) if update.effective_message.text else 'None'

        usr_name = update.effective_message.from_user.first_name
        if update.effective_message.from_user.last_name:
            usr_name += ' ' + update.effective_message.from_user.last_name

        if update.effective_message.from_user.username:
            usr_name += ' (@' + update.effective_message.from_user.username + ')'

        usr_chat_id = str(update.effective_message.from_user.id) if update.effective_message.from_user.id else 'None'

        module_logger.info("Has received a {} \"{}\" from user {}, with id {}"
                           .format(msg_type, usr_message, usr_name, usr_chat_id))


# the request for ethereum API
def api_check_balance(usr_wallet_address):

    url = ETHPLORER_API_URL.format(usr_wallet_address)
    response = requests.get(url)

    module_logger.info("API request URL: %s", url)

    if response.status_code == requests.codes.ok:

        # extract a json from response to a class "dict"
        response_dict = response.json()

        return response_dict

    else:

        module_logger.error('Error while request API: "%s". Error code: "%s"' % (url, response.status_code))
        # TODO send here a message to admin to inform about a trouble


# form the text message with individual wallet address information
def text_wallet_info(usr_lang_code, usr_wallet_api_dict):

    global price_ethusd

    usr_language_array = set_usr_language_array(usr_lang_code)

    address = usr_wallet_api_dict['address']

    str_eth_price = ''

    # check ETH balance & price
    eth_balance = round(Decimal(usr_wallet_api_dict['ETH']['balance']), 9).normalize()

    if price_ethusd:

        str_eth_price = ' `($' + str('%.2f' % (eth_balance * price_ethusd)) + ')`'

    # check all tokens balance & price
    if 'tokens' in usr_wallet_api_dict:

        all_tokens_balance = '\n' + usr_language_array['TXT_ETH_TOKENS']

        for token in usr_wallet_api_dict['tokens']:

            ############  TOKEN BALANCE
            # to convert a balance into a correct form to show
            token_balance = Decimal(token['balance']) / 10 ** int(token['tokenInfo']['decimals'])

            if (token_balance * 1000 - int(token_balance * 1000)) == 0:

                # token_balance = '%.2f' % token_balance
                str_token_balance = str(token_balance)

                str_token_balance = str_token_balance.rstrip('0').rstrip('.')\
                    if '.' in str_token_balance else str_token_balance

            else:

                str_token_balance = str(round(token_balance,9)).rstrip('0')

            ############  TOKEN PRICE
            str_token_price = ''

            if type(token['tokenInfo']['price']) is dict and 'rate' in token['tokenInfo']['price']:

                str_token_price = ' `($' + str('%.2f' % (token_balance * Decimal(token['tokenInfo']['price']['rate']))) + ')`'

            ############  TOKEN NAME
            if token['tokenInfo']['name']:

                str_token_name = token['tokenInfo']['name']

            else:

                str_token_name = '...'

            ############  TOKEN SYMBOL
            if token['tokenInfo']['symbol']:

                str_token_symbol = token['tokenInfo']['symbol']

            else:

                str_token_symbol = '...'

            ############  FINAL ONE TOKEN STRING INFORMTION
            all_tokens_balance += '\n`' + str_token_name\
                                  + '` (*' + str_token_symbol + '*): '\
                                  + str_token_balance + str_token_price

    else:

        all_tokens_balance = '\n' + usr_language_array['TXT_ETH_TOKENS_EMPTY']

    # to show 6 characters from start and from end of the address
    msg_text = '\n' + usr_language_array['TXT_ETH_ADDRESS']\
               + '*' + address[:6] + '....' + address[-6:]\
               + '*\n`Ethereum` (*ETH*): '\
               + str(eth_balance) + str_eth_price\
               + '\n' + all_tokens_balance + \
               '\n`-------------------------`\n'

    return msg_text


# to check a string is a really an ethereum address
def is_valid_eth_address(usr_msg_text):

    if re.search('^0x[a-zA-Z0-9]{40}', usr_msg_text) and len(usr_msg_text) == LENGTH_WALLET_ADDRESS:
        return True


# to parse current ETHEREUM usd and btc prices
def api_check_eth_price(bot, job):

    global price_ethusd, price_ethbtc

    response = requests.get(ETHERSCAN_API_URL)

    module_logger.info("API request URL: %s", ETHERSCAN_API_URL)

    if response.status_code == requests.codes.ok and response.json()['message'] == 'OK':

        # extract a json from response to a class "dict"
        response_dict = response.json()

        price_ethusd = Decimal(response_dict['result']['ethusd'])
        price_ethbtc = Decimal(response_dict['result']['ethbtc'])

    else:

        module_logger.error('Error while request ETHERSCAN.io API. Error code: "%s"' % (response.json()['message']))
        # TODO send here a message to admin to inform about a trouble
