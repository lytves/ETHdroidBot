import os
import sys
from threading import Thread

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from ethdroid.config import TOKEN_BOT, YOUR_TELEGRAM_ALIAS
from ethdroid.handlers import start, admin_say, error, text_handler, scheduler_balance_changes_check

from ethdroid.utils import module_logger, api_check_eth_price


def main():
    module_logger.info("Start the @ETHdroidBot bot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT, workers=10)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command start handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # bot's command to send a message for all users
    # put your Telegram alias here!
    dispatcher.add_handler(CommandHandler('admin_say', admin_say,
                                          filters=Filters.user(username=YOUR_TELEGRAM_ALIAS)))

    # bot's text handler
    text_update_handler = MessageHandler(Filters.text, text_handler)
    dispatcher.add_handler(text_update_handler)

    # CallbackQueryHandler to catch InlineKeyboardMarkup "callback_data"
    updater.dispatcher.add_handler(CallbackQueryHandler(text_handler))

    # here put the jobs for the bot
    job_queue = updater.job_queue
    # check ETHEREUM price each 30sec, from 5sec of the bot's start
    job_queue.run_repeating(api_check_eth_price, 60, 5)
    # check wallets balance changes each 5 min, from 15 sec of the bot's start
    job_queue.run_repeating(scheduler_balance_changes_check, 300, 15)

    ####################### bot's service handlers
    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()
        update.message.reply_text('Bot had been restarted!')

    dispatcher.add_handler(CommandHandler('restart', restart,
                                          filters=Filters.user(username=YOUR_TELEGRAM_ALIAS)))


    # Start the Bot start_polling() method
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.start_polling()
    updater.idle()


    # Start the Bot set_webhook() method
    # put your server IP adress instead 0.0.0.0
    # and see this page https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
    # updater.start_webhook(listen='127.0.0.1', port=5005, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://51.15.75.117/' + TOKEN_BOT,
    #                         certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()
