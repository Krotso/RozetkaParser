import telebot
import json
import requests
from bs4 import BeautifulSoup

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

def save_file(url, path):
  list = parse(url)
  if list != 0:
    with open(path, 'w', encoding='utf-8') as file:
      json.dump(list, file, ensure_ascii=False, indent=4)
    return 1
  else:
    return list

HEADERS = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36', 
  'accept': '*/*'}

def get_html(url, params=None):
  try:
    r = requests.get(url, headers=HEADERS, params=params)
    return r
  except:
    return 0

def get_page_count(html):
  soup = BeautifulSoup(html, 'html.parser')
  pagination = soup.find_all('li', class_="pagination__item")
  if pagination:
    return int(pagination[-1].get_text())
  else:
    return 1

def get_content(html):
  soup = BeautifulSoup(html, 'html.parser')
  items = soup.find_all('div', class_="goods-tile")
  
  products = []
  for item in items:
    in_stock = item.find('div', class_="goods-tile__availability_type_available")
    if in_stock:
      in_stock = True
    else:
      in_stock = False
    reviews = item.find('div', class_="goods-tile__stars").get_text(strip=True).split(' ', 1)[0]
    if reviews == 'Залишити':
      reviews = 0
    else:
      reviews = int(reviews)
    products.append({
      'title': item.find('span', class_="goods-tile__title").get_text(strip=True),
      'price': item.find('span', class_="goods-tile__price-value").get_text(strip=True).replace(u'\xa0', u' '),
      'have': in_stock,
      'reviews': reviews,
      'link': item.find('a', class_="goods-tile__picture").get('href'),
      'img': item.find('img', class_="lazy_img_hover").get('src')
    })
  return products

def parse(url):
  html = get_html(url)
  if html == 0:
    return 0
  elif html.status_code == 200:
    products = []
    pages_count = get_page_count(html.text)
    for page in range(1, pages_count + 1):
      html = get_html(url, params={'page': page})
      products.extend(get_content(html.text))
    return products
  else:
    return 0
