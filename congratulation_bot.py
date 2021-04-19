import telebot
from envparse import env
from image_maker import congratulation_func
# from requests import ReadTimeout
import time


TOKEN = env.str("TOKEN")
bot = telebot.TeleBot(TOKEN)

bot.polling(none_stop=True)


# @bot.message_handler(content_types=['text'])
# def quote_message_handler(message):
#     image_to_send = congratulation_func(message.text)
#     bot.send_photo(chat_id=message.chat.id, photo=image_to_send)
#
#
def telegram_bot_runner():
    try:
        bot.polling(none_stop=True)
    except Exception:
        bot.stop_polling()
        time.sleep(3)
        telegram_bot_runner()


if __name__ == '__main__':
    telegram_bot_runner()