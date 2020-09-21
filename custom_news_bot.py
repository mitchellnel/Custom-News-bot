import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async # rm
import schedule # rm
from selenium import webdriver # rm

import functions.utility
import functions.hltv
import functions.formula1 as f1
import functions.thespike as spike

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)

token_file = open("BOT_TOKEN.txt", 'r')
bot_token = token_file.readline()
token_file.close()

updater = Updater(token = bot_token, use_context = True)
dispatcher = updater.dispatcher

# intialise commands using CommandHandlers
start_handler = CommandHandler("start", utility.start)