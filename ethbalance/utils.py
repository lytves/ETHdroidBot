import requests
import locale
import logging

from decimal import Decimal

from ethbalance.config import API_URL, API_KEY, YOUR_ETH_ADDRESS
from ethbalance.handlers import get_usr_language_array

locale.setlocale(locale.LC_NUMERIC, 'en_GB.utf8')

# start logging to the file of current directory or º it to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
module_logger = logging.getLogger(__name__)

# start logging to the file with log rotation at midnight of each day
# formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
# handler = TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + '/../cryptocoinsinfobot.log',
#                                    when='midnight',
#                                    backupCount=10)
# handler.setFormatter(formatter)
# module_logger = logging.getLogger(__name__)
# module_logger.addHandler(handler)
# module_logger.setLevel(logging.INFO)
# end of log section


# the functions for logging handlers
def send_to_log(update, msg_type='command'):

    if update:
        usr_message = str(update.effective_message.text) if update.effective_message.text else 'None'

        usr_name = update.message.from_user.first_name
        if update.message.from_user.last_name:
            usr_name += ' ' + update.message.from_user.last_name

        if update.message.from_user.username:
            usr_name += ' (@' + update.message.from_user.username + ')'

        usr_chat_id = str(update.message.from_user.id) if update.message.from_user.id else 'None'

        module_logger.info("Has received a {} \"{}\" from user {}, with id {}"
                           .format(msg_type, usr_message, usr_name, usr_chat_id))

        # TODO put here a function to send a message for the admin (/start from new users and if somebody
        # TODO are trying to send a command to the bot)


def add_eth_wallet(last_menu_page):

    usr_language_array = get_usr_language_array()

    if last_menu_page == 'add_name_wallet':
        return usr_language_array['TXT_ADD_ETH_NAME_WALLET']

    elif last_menu_page == 'add_address_wallet':
        return usr_language_array['TXT_ADD_ETH_ADDRESS_WALLET']

    else:
        return usr_language_array['MENU_GO_BACK']


def del_eth_wallet():
    print('del_eth_wallet() under developing')
    return 'del'


def check_balance():

    url = API_URL + YOUR_ETH_ADDRESS + '?apiKey=' + API_KEY

    module_logger.info("API request URL: %s", url)
    response = requests.get(url)

    usr_language_array = get_usr_language_array()

    text = usr_language_array['TXT_ERROR']

    if response.status_code == requests.codes.ok:

        # extract a json from response to a class "dict"
        response_dict = response.json()

        if 'error' in response_dict:
            errors = response_dict['error']
            module_logger.error('api.ethplorer.io error! %s', errors)

            text += "\n`" + errors['message'] + '`'

        else:
            str_general_balance = ''
            address = str(response_dict['address'])

            # check ETH balance
            eth_balance = round(Decimal(response_dict['ETH']['balance']), 9).normalize()

            # eth_balance = ("%.9f" % eth_balance)
            # eth_balance = round(eth_balance,9).normalize()

            # check all tokens balance
            if 'tokens' in response_dict:
                str_tokens_balance = 'Tokens balance:'

                if (len(response_dict['tokens'])) > 0:

                    for token in response_dict['tokens']:

                        # to convert a balance into a correct form to show
                        token_balance = Decimal(token['balance']) / 10 ** int(token['tokenInfo']['decimals'])

                        if (token_balance * 1000 - int(token_balance * 1000)) == 0:
                            token_balance = '%.2f' % token_balance
                        else:
                            token_balance = round(token_balance,9).normalize()

                        str_tokens_balance += '\n`' + token['tokenInfo']['name'] + \
                            ' (' + token['tokenInfo']['symbol'] + ')`: ' + str(token_balance)

            else:
                str_tokens_balance = "You don't have any token"

            text = '`Ethereum adress`: \n' + address + '\nETH balance: '\
                   + str(eth_balance) + '\n' + str_tokens_balance

    else:
        module_logger.error('Error while request API: "%s". Error code: "%s"' % (url, response.status_code))
        # TODO send here a message to admin for inform him about a trouble

    return text


def show_bot_options():
    print('show_bot_options() under developing')


def send_feedback():
    print('send_feedback() under developing')
