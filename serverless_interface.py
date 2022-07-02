import telebot

from telebot_bot import bot 


def handler(event, _):
    message = telebot.types.Update.de_json(event["body"])
    bot.process_new_updates([message])
    return {"statusCode": 200, "body": f"Processed message: {message}"}

