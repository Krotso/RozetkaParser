import requests
from bs4 import BeautifulSoup

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
