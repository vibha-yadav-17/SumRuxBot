

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
	update.message.from_user
	logger.info("City of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
        'Hi! Welcome to SumRuxBookExchange. We at Sumrux identify people in the same pincode and exchange books.' 
        'We help create a community of readers who are physically proximate to each other.'
        'Which city do you live in?',
        reply_markup=ReplyKeyboardRemove())

	return CITY

def pincode(update, context):
	user=update.message.from_user
	logger.info("Pincode of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'Thankyou, you have made it easier for us to find you a match'
		'We do need some more information to help you find a suitable bookmatch.'
		'What is your pincode?',
		reply_markup=ReplyKeyboardRemove())

	return PINCODE 

def standard(update, context):
	user=update.message.from_user
	logger.info("Books of Standard %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'Thankyou for trusting us with your information.'
		'We are on our way to connect you with other readers around you.'
		'Which standard books are you looking for?',
		 reply_markup=ReplyKeyboardRemove())

	return STANDARD

def board(update, context):
	user=update.message.from_user
	logger.info("Books of Board %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'Almost there. Do you have any specific board in mind?',
		 reply_markup=ReplyKeyboardRemove())

	return BOARD

def medium(update, context):
	reply_keyboard = [['English' , 'Hindi']]

	user=update.message.from_user
	logger.info("Books of Medium %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
    	'Do you want English Medium or Hindi Medium Books?',
    	 reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	return MEDIUM

def subjects(update, context):
	user=update.message.from_user
	logger.info("Books of Subject %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		 'One last thing. Which subjects are you look for?',
		 reply_markup=ReplyKeyboardRemove())

	return SUBJECTS

def email(update, context):
	user=update.message.from_user
	logger.info("Email of %s; %s", user.first_name, update.message.text)
	update.message.reply_text(
		'We are glad you are trusting us with your information'
		'If you could give us your email ID, it would help us send you the relevant information'
		'What is your email?', 
		reply_markup=ReplyKeyboardRemove())

	return EMAIL 

def end(update,context):
	user=update.message.from_user
	logger.info("User %s ended the conversation.", user.first_name)
	update.message.reply_text('I hope we are of help to you. Happy reading!',
		                       reply_markup=ReplyKeyboardRemove())

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
             # CommandHandler('skip', skip_photo)],

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

    #    press ctrl c for stopping the bot 
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()


if __name__ == '__main__':
    main()
