import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async # rm
import schedule # rm
from selenium import webdriver # rm

import functions.Start_Sequence as StartSeq
import functions.hltv as hltv
import functions.formula1 as f1
import functions.thespike as thespike
import functions.mmoc as mmoc

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get token from .txt file
    token_file = open("BOT_TOKEN.txt", 'r')
    bot_token = token_file.readline().rstrip()
    token_file.close()

    # Create Updater, pass bot's token, and get dispatcher
    updater = Updater(token = bot_token, use_context = True)
    dispatcher = updater.dispatcher

    # Register handlers
    # Setup conversation handler with states:
    #   - utility.FIRST_SITE_SELECTED
    #   - utility.CONTINUE_SELECTING_SITES
    #   - utility.END_SITE_SELECTION
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("start", StartSeq.start)],

        states = {
            StartSeq.SITE_BUTTON_PRESSED: [CallbackQueryHandler(StartSeq.select_site)],
            StartSeq.FINISHED_SELECTING_SITES: [MessageHandler(Filters.text & ~Filters.command, StartSeq.select_blast_time)],
            StartSeq.INVALID_BLAST_TIME: [MessageHandler(Filters.text & ~Filters.command, StartSeq.select_blast_time)]
        },

        fallbacks = [CommandHandler("start", StartSeq.start)]
    )
    # Add ConversationHandler to dispatcher to handle start-up sequence
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()

    logging.log(level=logging.INFO, msg = "Bot is live and ready to roll.")

    # Run the bot until the user presses ctrl-C or the process receives SIG-INT/TERM/ABRT
    updater.idle()

if __name__ == "__main__":
    main()

