import telegram
import telegram
from telegram.ext.dispatcher import run_async # rm

@run_async
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id = chat_id, text = "Hello there! I'm the CustomNews_bot, here to provide you" +
                             "the lastest news from some of your favourite gaming and sport sites!")

    