

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INFO, LOCATION, BIO, CLASSNAMES = range(4)


def start(update, context):
    reply_keyboard = [['Need', 'Have']]

    update.message.reply_text(
        'Hi! Welcome to SumRuxBookExchange. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Do you need book or have book?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return INFO


def info(update, context):
    user = update.message.from_user
    logger.info("Requirement of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Please enter your location,'
                              'or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return LOCATION



def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Please enter your name!')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
    'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! What class/standard book do you want?')

    return CLASSNAMES

def classnames(update, context):
    user = update.message.from_user
    logger.info("Classname of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again.')



    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # will Create the Updater and pass it our bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states INFO, LOCATION, BIO, CLASSNAMES
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INFO: [MessageHandler(Filters.regex('^(Need|Have)$'), info)],

            #PHOTO: [MessageHandler(Filters.photo, photo),
             #       CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.text, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)],

            CLASSNAMES:[MessageHandler(Filters.text, classnames)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

#ctrl c for stopping the bot
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()


if __name__ == '__main__':
    main()