#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
# if you move this file anywhere, move it with same permissions!!!!
# cp --rp telegram-bot.py locationTOCopy
# -rw-r--r-- 1 root root 5100 Jun  2 09:22 telegram-bot.py

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

import face_recognition
import json
import os
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

NAME, PHOTO, NEW_NAME, NEW_PHOTO, NAUCI = range(5)


def start(bot, update):

    update.message.reply_text(
        'Lijep pozdrav! Ja sam HomeIOT asistent namjenjen za kućnu automatizaciju.\n\n'
        'Znam prepoznavati objekte i ljude na svim Vašim kamerama.\n'
    	'Trenutno imam postavljeno da Vam javljam ako se pojavi golub na balkonu i javljam sve ljude koje prepoznam, a i one koje ne prepoznam.\n'
        'Pošaljite /kraj za kraj razgovora.\n\n'
        'Sada bih htio naučiti kako se zovete i kako izgledate.\nMožete li mi reći kako se zovete?')

    return NAME


def name(bot, update):
    user = update.message.from_user
    global user_name
    user_name = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Ok! Još mi treba Vaša slika. \n'
                              'Molim jedan selfie gdje Vam se vidi lice!',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    logger.info(user_name)
    image_path = "known_people/" + user_name + '.jpg'
    photo_file.download(image_path)
    img = face_recognition.load_image_file(image_path)

    known_persons = {}
    data = []

    #if file of known persons exists, open it and load all persons into know_person dict
    if (os.path.getsize("known_people/known_people.json") > 0):
      with open('known_people/known_people.json') as data_file:
            known_persons = json.load(data_file)
    new_person = {}  
    new_person["name"] = user_name
    new_person["face_encoding"] = json.dumps(face_recognition.face_encodings(img)[0].tolist())
    person_exists = False
    try:
         for person in known_persons['data']:
               if(person["name"] == new_person["name"]):
                   person_exists = True
                   person["face_encoding"] = new_person["face_encoding"]
         if person_exists == False:
            known_persons['data'].append(new_person)
         
    except:
        known_persons['data'] = []
        known_persons['data'].append(new_person)

    # write persons back to json file        
    with open('known_people/known_people.json', 'w') as file:
        file.write(str(known_persons).replace("'","\""))


    update.message.reply_text('Odlično! Sad ću Vas znati prepoznati..\n'
                              'Ako želite da naučim još ljudi upišite njihovo ime, a ako zelite zavrsiti razgovor upišite /kraj :)')

    return NEW_NAME



def new_name(bot, update):
    user = update.message.from_user
    global new_user_name
    new_user_name = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Ok. Molim selfie, tj. sliku lica!',
                              reply_markup=ReplyKeyboardRemove())

    return NEW_PHOTO

def new_photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    logger.info(new_user_name)
    image_path = "known_people/" + new_user_name + '.jpg'
    photo_file.download(image_path)
    img = face_recognition.load_image_file(image_path)
    
    known_persons = {}

    if (os.path.getsize("known_people/known_people.json") > 0):
        with open('known_people/known_people.json') as data_file:    
            known_persons = json.load(data_file)

    new_person = {}  
    new_person["name"] = new_user_name
    new_person["face_encoding"] =  json.dumps(face_recognition.face_encodings(img)[0].tolist())
    person_exists = False
    try:
     for person in known_persons['data']:
        if(person["name"] == new_person["name"]):
            logger.info("Same person!")
            person_exists = True
            person["face_encoding"] = new_person["face_encoding"]
     if person_exists == False:
            known_persons['data'].append(new_person)
    except:
        known_persons['data'] = []
        known_persons['data'].append(new_person)

    with open('known_people/known_people.json', 'w') as file:
        file.write(str(known_persons).replace("'","\""))

    update.message.reply_text('Odlično! \n'
                              'Ako želite da naučim još ukućana upišite njihovo ime, a ako zelite zavrsiti razgovor upišite /kraj :)')

    return NEW_NAME

def nauci(bot, update):

    update.message.reply_text('Ime osobe?')

    return NEW_NAME

def cancel(bot, update):
    user = update.message.from_user

    update.message.reply_text('Javim kad prepoznam nešto. Lijep pozdrav! :)',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("595748741:AAGJrKY7EJTqJSvFP5r6dSnQ5C50YCn873U")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('nauci', nauci)],

        states={
            NAME: [MessageHandler(Filters.text, name)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('kraj', cancel)],

	    NEW_NAME: [MessageHandler(Filters.text, new_name	)],


	    NEW_PHOTO: [MessageHandler(Filters.photo, new_photo),
                    CommandHandler('kraj', cancel)],

        },

        fallbacks=[CommandHandler('kraj', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
