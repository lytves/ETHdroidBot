import logging
from logging.handlers import TimedRotatingFileHandler

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

from ethbalance.config import TOKEN_BOT
from ethbalance.handlers import start, admin_say, error, text_input

# start logging to the file of current directory or print it to console
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# start logging to the file with log rotation at midnight of each day
# formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
# handler = TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + '/ethbalancebot.log',
#                                    when='midnight',
#                                    backupCount=10)
# handler.setFormatter(formatter)
# logger = logging.getLogger(__name__)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)
# end of log section


def main():
    logger.info("Start the @ETHbalanceBot bot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # bot's command handlers
    start_handler = CommandHandler('admin_say', admin_say)
    dispatcher.add_handler(start_handler)

    # bot's text handlers
    text_update_handler = MessageHandler(Filters.text, text_input)
    dispatcher.add_handler(text_update_handler)

    # here put the job for the bot
    # job_queue = updater.job_queue
    # job_queue.run_repeating(download_api_coinslists_handler, 150, 10, context='coinmarketcap')
    # job_queue.run_repeating(download_api_coinslists_handler, 150, 40, context='cryptocompare')

    updater.start_polling()

    # put your server IP adress instead 0.0.0.0
    # and see this page https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
    # updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://0.0.0.0/' + TOKEN_BOT,
    #                   certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()
