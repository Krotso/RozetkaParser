from rozetka_parser import parse
import json

def save_file(url, path):
  list = parse(url)
  if list != 0:
    with open(path, 'w', encoding='utf-8') as file:
      json.dump(list, file, ensure_ascii=False, indent=4)
    return 1
  else:
    return list
