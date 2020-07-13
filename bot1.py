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
CONFIRM_OPTIONS = ['Yes', 'No']



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
            reply_markup=ReplyKeyboardMarkup([SIDEPROJECT_OPTIONS], one_time_keyboard=True))

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
            '''Do you know any framework ? Please list them''',
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
            reply_markup=ReplyKeyboardMarkup([CONFIRM_OPTIONS], one_time_keyboard=True))

    return CONFIRM


def confirm(update, context):
    context.user_data['Confirm'] = update.message.text
    user = update.message.from_user
    logger.info("Confirm: %s",update.message.text)
       
    return NAME




def main():
  

    updater = Updater(
        os.getenv("TELEGRAM_TOKEN", ""), use_context=True)


    dp = updater.dispatcher


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


    updater.start_polling()

   
    updater.idle()
    

if __name__ == '__main__':
    main()

