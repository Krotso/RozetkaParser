import telebot
import json
from converter import save_file

# Create bot objekt
bot = telebot.TeleBot('1646200204:AAGJfUyym3Rmyynvr8WLWnwJQgHbD_1su1A')

# Create file path
PATH = 'items.json'

# Open answers for bot commands and
# returns JSON object as a dictionary
with open('comand_answer.json', encoding='utf-8') as file:
  answers = json.load(file)
  answers = answers[0]

# Create handler for help command
@bot.message_handler(commands=['help'])
def help_answer(message):
  bot.reply_to(message, answers['help'])

# Create handler for start command
@bot.message_handler(commands=['start'])
def start_answer(message):
  bot.reply_to(message, answers['start'])

@bot.message_handler(content_types=['text'])
def get_link_return_file(message):
  bot.send_message(message.from_user.id, "Секунду")
  file_ready = save_file(message.text, PATH)
  if file_ready:
    bot.send_message(message.from_user.id, answers['converted'])
    items_file = open('items.json')
    bot.send_document(message.chat.id, items_file)
  else:
    bot.send_message(message.from_user.id, answers['unconverted'])

# Start bot
bot.polling(none_stop=True)