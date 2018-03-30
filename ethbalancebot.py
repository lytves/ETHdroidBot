import os
import sys
from threading import Thread

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from ethbalance.config import TOKEN_BOT, YOUR_TELEGRAM_ALIAS
from ethbalance.handlers import start, admin_say, error, text_handler

from ethbalance.utils import module_logger


def main():
    module_logger.info("Start the @ETHbalanceBot bot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT)
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


    ####################### bot's service handlers
    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart(updater)).start()
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
    # updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://0.0.0.0/' + TOKEN_BOT,
    #                   certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()
