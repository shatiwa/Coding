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

from db import DB
import sqlite3
import logging
import os
import re
from telegram import User, TelegramObject
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence, BasePersistence, Dispatcher)
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


START, NAME, COLLEGE, SIDEPROJECT, LANGUAGE, FRAMEWORK,CONFIRM, CONFIDENT= range(8)


SIDEPROJECT_OPTIONS = ['Friend','Facebook','Whatsapp', 'LinkedIn']
LANGUAGE_OPTIONS = ['Java', 'C', 'C++','c#','Javascript','Python','HTML','HTML5','PHP','SQL','Ruby']
YES_NO_OPTIONS = ['Yes', 'No']
#MEDIUM_OPTIONS = ['English','Hindi','Kannada']


def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    update.message.reply_text(
        f'''
	Hello!Please enter your Name
        ''')
    return NAME

def name(update, context):
    context.user_data['Name'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z A-Z]+$"

    if(re.search(regex, context.user_data['Name'])):
        logger.info("Name: %s", update.message.text)
        update.message.reply_text(
            ''' Please enter your college''',
            reply_markup=ReplyKeyboardRemove())

    return COLLEGE

def college(update, context):
    context.user_data['College'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z A-Z]+$"

    if(re.search(regex, context.user_data['College'])):
        logger.info("College: %s", update.message.text)
        update.message.reply_text(
            'How do you get to know about sideproject',
            reply_markup=ReplyKeyboardRemove())

    return SIDEPROJECT

def sideproject(update, context):
    context.user_data['Sideproject'] = update.message.text
    user = update.message.from_user

    if(context.user_data['Sideproject'] in SIDEPROJECT_OPTIONS):
        logger.info("Sideproject: %s", update.message.text)

        update.message.reply_text(
            '''
		Which programming language do you know ?''',
            reply_markup=ReplyKeyboardMarkup([LANGUAGE_OPTIONS], one_time_keyboard=True))
        return LANGUAGE


def language(update, context):
    context.user_data['Language'] = update.message.text
    user = update.message.from_user
    if(context.user_data['Language']in LANGUAGE_OPTIONS):
        logger.info("Language: %s",update.message.text)
        update.message.reply_text(
            '''Do you know any framework ?''',
            reply_markup=ReplyKeyboardRemove())
    return FRAMEWORK


def framework(update, context):
    context.user_data['Framework'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z,-:A-Z 0-9]+$"

    if(re.search(regex, context.user_data['Framework'])):
        logger.info("Framework: %s", update.message.text)
        update.message.reply_text(
            'Have you done any project before ?',
            reply_markup=ReplyKeyboardMarkup([DEAL_OPTIONS], one_time_keyboard=True))

    return CONFIRM


def confirm(update, context):
    context.user_data['Confirm'] = update.message.text
    user = update.message.from_user
    logger.info("Confirm: %s",update.message.text)

    if context.user_data['Confirm'] == "Yes":
        logger.info("Confirmation: %s", update.message.text)
       
        update.message.reply_text(f'''
		How confident are you ?''',
                                  reply_markup=ReplyKeyboardMarkup([YES_NO_OPTIONS], one_time_keyboard=True))
        return NAME




def main():
    # will Create the Updater and pass it our bot's token.
    # Make sure to set use_context=True to use the new context based callbacks

    updater = Updater(
        os.getenv("TELEGRAM_TOKEN", ""), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states INFO, LOCATION, BIO, CLASSNAMES
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [MessageHandler(Filters.text, start)],

            COLLEGE: [MessageHandler(Filters.text, college)],

            NAME: [MessageHandler(Filters.text, name)],

            SIDEPROJECT: [MessageHandler(Filters.text, sideproject)],

            LANGUAGE: [MessageHandler(Filters.text, language)],

            FRAMEWORK: [MessageHandler(Filters.text, framework)],

            CONFIRM: [MessageHandler(Filters.text, confirm)],

        },

        fallbacks=[CommandHandler('confirm', confirm)], )

    dp.add_handler(conv_handler)

    # log all errors
#    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #    press ctrl c for stopping the bot
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()
    # d.add_item(CITY, PINCODE, STANDARD, BOARD, MEDIUM, SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)
    # print(CITY, PINCODE, STANDARD, BOARD, MEDIUM,
    #       SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)

    # d.get_items()


if __name__ == '__main__':
    main()
