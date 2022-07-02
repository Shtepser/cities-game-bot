import os
import logging
import telebot

from db import add_turns, get_turns, reset_game
from cities_game import handle_turn, TurnResult
from messages import *
from cli_interface import load_cities


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    raise Exception("Wrong configuration: BOT_TOKEN environment variable must be set")


logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGGING_LEVEL", "INFO").upper())

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_game(message):
    logger.info("Processing command /start from user %d", message.chat.id)
    turns = get_turns(message.chat.id)
    if len(turns) > 0:
        status = f"Игра уже идёт, прошлый ход: {turns[-1]}\n" +\
                 f"Бот ждёт вашего хода."
    else:
        status = "Отправьте свой первый ход, чтобы начать игру."
    bot.send_message(message.chat.id,
                     f"Игра в города\n\n{status}")


@bot.message_handler(commands=["surrender"])
def register_surrender(message):
    logger.info("Processing command /surrender from user %d", message.chat.id)
    reset_game(message.chat.id)
    bot.send_message(message.chat.id,
                     bot_victory_report())


@bot.message_handler(commands=["help"])
def send_help(message):
    logger.info("Processing command /help from user %d", message.chat.id)
    bot.send_message(message.chat.id,
                     "Бот для игры в города.\n\nКоманды:\n"
                     "/start — начать игру\n"
                     "/surrender — сдаться\n"
                     "/help — показать это сообщение\n"
                     "/info — показать информацию о боте")


@bot.message_handler(commands=["info"])
def send_info(message):
    logger.info("Processing command /info from user %d", message.chat.id)
    bot.send_message(message.chat.id,
                     "Бот для игры в города.\n"
                     "Автор бота: Анатолий Полетаев aka @Shtepser\n"
                     "Изображение на аватаре взято с сайта icons-icons.com, "
                     "автор: Safraz Shoukat")


@bot.message_handler()
def process_turn(message):
    logger.info("Processing turn %s from user %d", message.text, message.chat.id)
    player_id, player_turn = message.chat.id, message.text.strip()
    cities = load_cities()
    turns = get_turns(player_id)
    turn_result, ai_turn = handle_turn(player_turn, cities, turns)
    if turn_result is TurnResult.success:
        response = successful_turn_report(player_turn, ai_turn)
        add_turns(player_id, [player_turn, ai_turn])
    elif turn_result is TurnResult.player_wins:
        response = player_victory_report(player_turn)
    elif turn_result is TurnResult.unmatched_letters:
        response = unmatched_letters_report(player_turn, turns[-1])
    elif turn_result is TurnResult.already_taken:
        response = already_taken_report(player_turn)
    else:
        response = unknown_city_report(player_turn)
    bot.send_message(message.chat.id, response)

