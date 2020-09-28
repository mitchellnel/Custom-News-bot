import telegram

from telegram.ext.dispatcher import run_async # rm
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction
from telegram.ext import CallbackQueryHandler

import logging
import threading

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)

global user_sites
user_sites = dict()

#@run_async
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)

    user_first_name = update.message.from_user.first_name

    user_sites[chat_id] = list()

    context.bot.send_message(chat_id = chat_id, text = "Hello there, " + user_first_name + "! I'm the CustomNews_bot, "
                                                                                           "here to provide you with "
                                                                                           "the latest news from some "
                                                                                           "of your favourite gaming "
                                                                                           "and sport sites!")

    context.bot.send_message(chat_id = chat_id, text = "In order to provide you with daily news updates from your "
                                                       "favourite sites, I want to know which websites you want to "
                                                       "\"subscribe\" to.")

    # create inline keyboard
    keyboard = [[InlineKeyboardButton("HLTV", callback_data = "HLTV.org"),
                 InlineKeyboardButton("THESPIKE.GG", callback_data = "THESPIKE.GG")],

                [InlineKeyboardButton("F1.com", callback_data = "F1.com"),
                 InlineKeyboardButton("MMO-Champion", callback_data = "MMO-Champion.org")]]

    # get user to select their first site to subscribe to
    # open thread to help do non-busy waiting
    first_thread = threading.Thread(target = add_site, args = [update, context, chat_id, keyboard, True])
    first_thread.start()

    # wait here for the first site to be added before continuing
    first_thread.join()

    # continue getting the user to add sites if they wish
    # create inline keyboard
    keyboard = [[InlineKeyboardButton("HLTV", callback_data="HLTV.org"),
                 InlineKeyboardButton("THESPIKE.GG", callback_data="THESPIKE.GG")],

                [InlineKeyboardButton("F1.com", callback_data="F1.com"),
                 InlineKeyboardButton("MMO-Champion", callback_data="MMO-Champion.org")],

                [InlineKeyboardButton("Stop selecting sites", callback_data = "$end_selection")]]

    # open thread to help do non-busy waiting
    thread = threading.Thread(target = add_site, args = [update, context, chat_id, keyboard])
    while True:
        thread.start()

        # wait here for a response
        thread.join()

        # check if the user chose to stop selecting sites
        if "$end_selection" in user_sites[chat_id]:
            user_sites[chat_id].remove("$end_selection")

    remove_site_duplicates(chat_id)

    context.bot.send_message(chat_id = chat_id, text = "You are currently subscribed to the following news feeds:\n" +
                                                            get_user_sites_in_bullets(chat_id))

def add_site(update, context, chat_id, keyboard, call_from_start = False):
    reply_markup = InlineKeyboardMarkup(keyboard)

    if call_from_start:
        update.message.reply_text("Use the buttons below to tell me which sites you want news updates from:",
                                  reply_markup = reply_markup)
        return True
    else:
        update.message.reply_text("You can keep selecting more sites to subscribe to! Tap on the \"Stop selecting"
                                  " sites\" button when you're done.",
                                  reply_markup = reply_markup)


def site_selection_button(update, context):
    chat_id = update.effective_chat.id

    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is required
    query.answer()

    if query.data != "$end_selection":
        if query.data in user_sites[chat_id]:
            query.edit_message_text(text = "You've already subscribed to the {} news feed.".format(query.data))
        else:
            query.edit_message_text(text = "Great! You've just subscribed to the {} news feed.".format(query.data))
    else:
        query.edit_message_text(text = "Okay, you don't want to select anymore sites.\nIn the future, if you want to"
                                       " edit your site preferences, you can use the /changesites command.")

    user_sites[chat_id].append(query.data)
    print(user_sites)

def remove_site_duplicates(chat_id):
    user_sites[chat_id] = list(set(user_sites[chat_id]))


def get_user_sites_in_bullets(chat_id):
    sites = ""

    for curr_site in user_sites[chat_id]:
        sites = sites + " - " + curr_site + "\n"

    return(sites)

