# ETHdroidBot

[@ETHdroidBot](https://t.me/ETHdroidBot "@ETHdroidBot") - enjoy it!

This is a telegram bot to control balance of your Ethereum wallets, you can add your ethereum addresses (wallets)
 and control your balance of Ethereum and ERC tokens on it, also bot are going to check balance of your
 wallets and are going to keep you informed about all changes on it.
 
 
* Had been used [pyTelegramBotAPI Library](https://github.com/eternnoir/pyTelegramBotAPI "pyTelegramBotAPI Library GitHub Repository"), 
you can use *start_polling* or *webhook* updates methods to recieve the messages (see ethdroidbot.py code and pyTelegramBotAPI Library manual)

* [MongoBD database](https://github.com/mongodb/mongo) and [PyMongo](https://github.com/mongodb/mongo-python-driver "PyMongo") - the Python driver for MongoDB had been used
to store user's wallets and balances

* To receive Ethereum balances is used API - “Powered by [Ethplorer.io](https://ethplorer.io/ "Ethplorer.io")” 

* To show current Ethereum market price is used API - [The Etherscan Ethereum Developer APIs](https://etherscan.io/apis "The Etherscan Ethereum Developer APIs")

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

![ETHdroidbot](ethdroidbot.png "ETHdroidbot")