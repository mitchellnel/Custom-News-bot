import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async # rm
import schedule # rm
from selenium import webdriver # rm

import functions.utility as utility
import functions.hltv as hltv
import functions.formula1 as f1
import functions.thespike as thespike
import functions.mmoc as mmoc

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # get token from .txt file
    token_file = open("BOT_TOKEN.txt", 'r')
    bot_token = token_file.readline().rstrip()
    token_file.close()

    updater = Updater(token = bot_token, use_context = True)
    dispatcher = updater.dispatcher

    # intialise and add "Handlers"
    # start_handler to handle first-time start sequence
    start_handler = CommandHandler("start", utility.start)
    dispatcher.add_handler(start_handler)

    # site_selection_handler to handle user input from site selection buttons
    site_selection_handler = CallbackQueryHandler(utility.site_selection_button)
    dispatcher.add_handler(site_selection_handler)

    # start the bot
    updater.start_polling()

    logging.log(level=logging.INFO, msg = "Bot is live and ready to roll.")

    # run the bot until the user presses ctrl-C or the process receives SIG-INT/TERM/ABRT
    updater.idle()

if __name__ == "__main__":
    main()

