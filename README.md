# ETHdroidBot

This is a telegram bot to control balance of your Ethereum wallets, you can add your ethereum addresses (wallets)
 and control your balance of Ethereum and ERC tokens on it, also bot are going to check balance of your
 wallets and are going to keep you informed about all changes on it.
 
 
* Had been used [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot API Library GitHub Repository") API Library, 
you can use *start_polling* or *webhook* updates methods to recieve the messages (see ethdroidbot.py code and pyTelegramBotAPI Library manual)

* [MongoBD database](https://github.com/mongodb/mongo) and [PyMongo](https://github.com/mongodb/mongo-python-driver "PyMongo") - the Python driver for MongoDB had been used
to store user's wallets and balances

* “Powered by [Ethplorer.io](https://ethplorer.io/ "Ethplorer.io")” for view ethereum tokens balances. I would recommend you to get personal Ethplorer API key, see [Ethplorer's public API](https://github.com/EverexIO/Ethplorer/wiki/ethplorer-api "Ethplorer's public API")

* To show current Ethereum market price is used API - [CryptoCompare API](https://www.cryptocompare.com/api/ "CryptoCompare API")

### Install:

You need to install:

+ python (tested on 3.5+ version)
 
+ python-telegram-bot with:

`$ pip install python-telegram-bot --upgrade`

+ mongod - The database server

+ pymongo with:

`$ python -m pip install pymongo`

But in any case you must read authentic modules documentation to use it in your own operating system
 and environment
 
### Settings:

Bot Settings are in the file **ethdroid/config.py:**

* put your *TOKEN_BOT*
* admin telegram alias *YOUR_TELEGRAM_ALIAS*
* some your API urls settings
* put your MongoDB settings: *MONGO_DB_NAME* and *MONGO_DB_COLLECTION*

### Run:

`$ python ethdroidbot.py`

- you must use your python correct command depend of your python version and install path

---

Screenshot of the working bot:

![ETHdroidbot](ethdroidbot.jpg "ETHdroidbot")
