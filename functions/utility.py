import telegram

from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction
from telegram.ext import CallbackQueryHandler

import datetime

import logging

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

# Stages
SITE_BUTTON_PRESSED = "SITE_BUTTON_PRESSED"
FINISHED_SELECTING_SITES = "FINISHED_SELECTING_SITES"

INVALID_BLAST_TIME = "INVALID_BLAST_TIME"

# Commands for pulling headlines from sites
SITE_NEWS_COMMANDS = {
    "HLTV.org": "/hltv",
    "THESPIKE.GG": "/thespike",
    "F1.com": "/f1",
    "MMO-Champion.org": "/mmoc"
}

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
    context.user_data["site_list"] = list()

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

    if query.data in context.user_data["site_list"]:
        # Send a response to the user to echo their selection
        # Then send message with text and appended InlineKeyboard for user to keep selecting sites
        query.edit_message_text(text = "You've already subscribed to the {} news feed.\n\nYou can keep selecting more"
                                       " sites to subscribe to! Tap on the \"Stop selecting sites\" button when you're"
                                       " done.".format(query.data),
                                reply_markup = reply_markup)

        return SITE_BUTTON_PRESSED
    elif query.data == "$stop_site_selection":
        # Send a response to the user to echo their selection
        #   and then ask the user to input a time for their
        #   daily "news blast"
        query.edit_message_text(text="Okay, you don't want to select anymore sites.\n\n"
                                     "Your currently subscribed sites (and the commands to pull their news headlines)"
                                     " are:\n" + get_user_sites_in_bullets_with_commands(context) +  "\n"
                                                                                                     
                                     "In the future, if you want to edit your site subscriptions, you can use the"
                                     " /changesites command.\n\n"
                                                                                                     
                                     "Now we can continue and select your daily \"news blast\" time!\n\n"
                                                                                                     
                                     "Please send me a message of the time you would like to have your daily \"news"
                                     " blast\" (for 9am, type 0900 or 900; for 1:25pm, type 1300; for 12am, type 0000"
                                     " or 0)")

        return FINISHED_SELECTING_SITES
    else:
        # Add the selected site
        context.user_data["site_list"].append(query.data)
        # Send a response to the user to echo their selection
        # Then send message with text and appended InlineKeyboard for user to keep selecting sites
        query.edit_message_text(text = "Great! You've just subscribed to the {} news feed.\n\nYou can keep selecting more"
                                       " sites to subscribe to! Tap on the \"Stop selecting sites\" button when you're"
                                       " done.".format(query.data),
                                reply_markup = reply_markup)

        return SITE_BUTTON_PRESSED


def get_user_sites_in_bullets_with_commands(context):
    sites = ""

    for curr_site in context.user_data["site_list"]:
        sites = sites + "  - " + curr_site + " (" + SITE_NEWS_COMMANDS[curr_site] + ")" +"\n"

    return(sites)


def select_blast_time(update, context):
    """
        Take the message the user sent and find out what time they
        want their daily news blast to be sent
    """
    chat_id = update.effective_chat.id

    # Get the message the user sent
    time_str = update.message.text
    time = int(time_str)

    # Get hours from time
    hrs = int(time / 100)
    # Get mins from time
    mins = time % 100

    validTime = False

    # Check if the user passed a valid time by using a try-except
    try:
        time_obj = datetime.time(hrs, mins, 0)
        validTime = True
    except:
        logger.critical("User %s did not input a valid time. Prompting them for another time...",
                        update.message.from_user.first_name)

    # If the user input wasn't valid, make them input another time
    if not validTime:
        context.bot.send_message(chat_id=chat_id, text="That's not a valid time. Please enter a valid time"
                                                       " (for 9am, type 0900 or 900; for 1:25pm, type 1325; for 12am,"
                                                       " type 0000 or 0")
        return INVALID_BLAST_TIME

    # If the user input was valid, store their "blast" time in user_data
    context.user_data["blast_time"] = time_obj
    update.message.reply_text("Okay! You've chosen to receive your \"news blasts\" at " + str(time_obj.hour) + ":" +
                              str(time_obj.minute) + " everyday.")

    context.bot.send_message(chat_id=chat_id,
                             text="Alright! I now have all the information I need to send you your daily"
                                  " \"news blasts\".")
    context.bot.send_message(chat_id=chat_id,
                             text="You can also manually request the latest headlines from your subscribed sites using"
                                  " their respective \"pull\" commands. To see these again, use the /mysites command.")
    context.bot.send_message(chat_id=chat_id,
                             text="If you need further command help, use /help to see a list of available commands and"
                                  " their functions.")
