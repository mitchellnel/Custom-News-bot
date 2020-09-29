import telegram

from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction
from telegram.ext import CallbackQueryHandler

import logging
import threading

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

# Stages
SITE_BUTTON_PRESSED = "SITE_BUTTON_PRESSED"
FINISHED_SELECTING_SITES = "FINISHED_SELECTING_SITES"

SELECTED_BLAST_TIME = "SELECTED_BLAST_TIME"

global user_sites
user_sites = dict()

@run_async
def start(update, context):
    """ /start sequence:
            1. Welcome the user, state purpose
            2. Get user to subscribe to sites
    """
    chat_id = update.effective_chat.id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)

    # Get user that sent /start and log name
    user = update.message.from_user
    logger.info("User %s started the conversation with the bot.", user.first_name)

    # Initialise site list for current chat (using chat_id as key)
    user_sites[chat_id] = list()

    # Welcome user and state purpose
    context.bot.send_message(chat_id = chat_id, text = "Hello there, " + user.first_name + "! I'm the CustomNews_bot, "
                                                                                           "here to provide you with "
                                                                                           "the latest news from some "
                                                                                           "of your favourite gaming "
                                                                                           "and sport sites!")

    # Get user to select first site to subscribe to
    context.bot.send_message(chat_id = chat_id, text = "In order to provide you with daily news updates from your "
                                                       "favourite sites, I want to know which websites you want to "
                                                       "\"subscribe\" to.")

    # Create inline keyboard
    keyboard = [[InlineKeyboardButton("HLTV", callback_data = "HLTV.org"),
                 InlineKeyboardButton("THESPIKE.GG", callback_data = "THESPIKE.GG")],

                [InlineKeyboardButton("F1.com", callback_data = "F1.com"),
                 InlineKeyboardButton("MMO-Champion", callback_data = "MMO-Champion.org")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    update.message.reply_text("User the buttons below to tell me which sites you want news updates from:",
                              reply_markup = reply_markup)

    # Tell ConversationHandler that we're in state "FIRST_SITE_SELECTED" now
    return SITE_BUTTON_PRESSED


def select_site(update, context):
    """ Add first site to the user's site list,
        then show a new choice of buttons to continue selecting sites
    """
    chat_id = update.effective_chat.id

    # Get data from the query
    query = update.callback_query
    query.answer()

    # Create the new inline keyboard
    keyboard = [[InlineKeyboardButton("HLTV", callback_data = "HLTV.org"),
                 InlineKeyboardButton("THESPIKE.GG", callback_data = "THESPIKE.GG")],

                [InlineKeyboardButton("F1.com", callback_data = "F1.com"),
                 InlineKeyboardButton("MMO-Champion", callback_data = "MMO-Champion.org")],

                [InlineKeyboardButton("Stop selecting sites", callback_data = "$stop_site_selection")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data in user_sites[chat_id]:
        # Send a response to the user to echo their selection
        # Then send message with text and appended InlineKeyboard for user to keep selecting sites
        query.edit_message_text(text = "You've already subscribed to the {} news feed.\n\nYou can keep selecting more"
                                       " sites to subscribe to! Tap on the \"Stop selecting sites\" button when you're"
                                   " done.".format(query.data),
                                reply_markup = reply_markup)

        return SITE_BUTTON_PRESSED
    elif query.data == "$stop_site_selection":
        # Send a response to the user to echo their selection
        query.edit_message_text(text = "Okay, you don't want to select anymore sites.")

        context.bot.send_message(chat_id = chat_id,
                                 text="Your currently subscribed sites are:\n" + get_user_sites_in_bullets(chat_id))
        context.bot.send_message(chat_id = chat_id,
                                 text = "In the future, if you want to edit your site subscriptions, you can use the"
                                      " /changesites command.")

        return FINISHED_SELECTING_SITES
    else:
        # Add the selected site
        user_sites[chat_id].append(query.data)
        # Send a response to the user to echo their selection
        # Then send message with text and appended InlineKeyboard for user to keep selecting sites
        query.edit_message_text(text = "Great! You've just subscribed to the {} news feed.\n\nYou can keep selecting more"
                                       " sites to subscribe to! Tap on the \"Stop selecting sites\" button when you're"
                                       " done.".format(query.data),
                                reply_markup = reply_markup)

        return SITE_BUTTON_PRESSED


def get_user_sites_in_bullets(chat_id):
    sites = ""

    for curr_site in user_sites[chat_id]:
        sites = sites + "  - " + curr_site + "\n"

    return(sites)


def select_blast_time(update, context):
    # TODO: Implement function to select the daily "news blast" time
    context.bot.send_message(update.effective_chat.id, "This hasn't been implemented yet...")

