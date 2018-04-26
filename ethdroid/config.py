# put your bot's token here
TOKEN_BOT = 'put_your_bot_token_here'
YOUR_TELEGRAM_ALIAS = '@put_your_telegram_username_here'


# Ethplorer.io API
ETHPLORER_API_KEY = 'freekey'
ETHPLORER_API_URL = 'https://api.ethplorer.io/getAddressInfo/{}?apiKey=' + ETHPLORER_API_KEY


# ETHERSCAN.io API
ETHERSCAN_API_KEY = 'put_your_api_token_here'
ETHERSCAN_API_URL = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + ETHERSCAN_API_KEY


# CryptoCompare API
CRYPTOCOMPARE_API_URL = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR'


# number of ETH wallets user can to add
NUMBER_WALLETS = 5
# ETH address format
LENGTH_WALLET_ADDRESS = 42
# to split long send_message (Telegram restrictions 4096 UTF8 characters,
# to use parse_mode="Markdown" method we must increase it for 1600-1700 characters)
MAX_MESSAGE_LENGTH = 1600


# put your DB name and collection name here
MONGO_DB_NAME = 'put_your_db_name_here'
MONGO_DB_COLLECTION = 'put_your_db_connection_here'
