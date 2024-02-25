#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from sys import argv
from datetime import date


def get_hours(name, config):
  headers = {
      'authority': 'tennis.paris.fr',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en,fa;q=0.9,fr;q=0.8,en-US;q=0.7',
      'cache-control': 'max-age=0',
      'dnt': '1',
      'origin': 'https://tennis.paris.fr',
      'referer': 'https://tennis.paris.fr/tennis/jsp/site/Portal.jsp?page=recherche&action=rechercher_creneau',
      'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }

  params = {
      'page': 'recherche',
      'view': 'rechercher_creneau',
  }

  data = {
      'page': 'recherche',
      'action': 'rechercher_creneau',
      'hourRange': {config['hours']},
      'selWhereTennisName': {name},
      'when': {config['date']},
      'selCoating': [
          '96',
          '2095',
          '94',
          '1324',
          '2016',
          '92',
      ],
      'selInOut': {'V' if config['couvert'] else 'F'}
  }

  response = requests.post(
      'https://tennis.paris.fr/tennis/jsp/site/Portal.jsp',
      params=params,
      headers=headers,
      data=data,
  )

  soup = BeautifulSoup(response.text, 'html.parser')
  res = list(map(lambda x: x.text, soup.select('.panel-title')))
  return res
  # print(soup.prettify())


def search_available(config):
  headers = {
      'authority': 'tennis.paris.fr',
      'accept': '*/*',
      'accept-language': 'en,fa;q=0.9,fr;q=0.8,en-US;q=0.7',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'dnt': '1',
      'origin': 'https://tennis.paris.fr',
      'referer': 'https://tennis.paris.fr/tennis/jsp/site/Portal.jsp?page=recherche&action=rechercher_creneau',
      'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest',
  }

  params = {
      'page': 'recherche',
      'action': 'ajax_disponibilite_map',
  }

  data = {
      'hourRange': {config['hours']},
      'when': {config['date']},
      'selCoating[]': [
          '96',
          '2095',
          '94',
          '1324',
          '2016',
          '92',
      ],
      'selInOut': {'V' if config['couvert'] else 'F'}
  }

  print(config['date'])

  response = requests.post(
      'https://tennis.paris.fr/tennis/jsp/site/Portal.jsp',
      params=params,
      headers=headers,
      data=data,
  )

  data = response.json()
  features = data['features']
  res = []
  for f in features:
    props = f['properties']
    available = props['available']
    general = props['general']
    arrond = general['_arrondissement']
    if available and (arrond in config['arronds']):
      name = general['_nomSrtm']
      res.append(
          f"Tennis {name}, arrondissement:{arrond}, {config['date']}, {get_hours(name, config)}".replace('\'', ''))
  return res
  # print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
  date = argv[1] if len(argv) > 1 else '18/02/2023'
  print(date)
  config = {
      'date': date,
      'hours': '10-20',
      'couvert': True,
      'arronds': range(1, 21)
  }
  res = search_available(config)
  print(res)
  # get_hours('Jules Ladoumègue')
