import requests
import urllib
import re
import os
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from EgyFucntions.Function import inline
from telegram.files.inputmedia import InputMediaPhoto
from telegram import InlineKeyboardButton
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

user = UserAgent()
headers = {'user-agent': user.random}
s = requests.Session()
s.cookies.set('PSSID', os.environ.get('PSSID'), domain='giga.egybest.kim', expires=None)
s.headers.update(headers)

def get_shows(key_word):
    moviesDict = {}
    imgs = []
    buttons = []

    r = requests.get(f'https://giga.egybest.kim/explore/?q={key_word}').text
    soup = BeautifulSoup(r, 'html.parser')
    movies = soup.find_all('a', class_='movie', limit=10)
    for i in range(len(movies)):
        id = i
        name = movies[i].find('span', class_='title').text
        type = re.search('/(series|movie)/', movies[i].get('href')).group(1)
        url = movies[i].get('href')
        img = movies[i].find('img').get('src')

        moviesDict[str(id)] = {
            'id' : id,
            'name' : name,
            'type': type,
            'url' : url,
            'img' : img,
        }

        imgs.append(InputMediaPhoto(media=img, caption=f'#{id+1} {name} - {type}'))
        buttons.append(InlineKeyboardButton(text=f'#{id+1} {name} - {type}', callback_data=id))

    moviesDict['display'] = {'imgs':imgs, 'buttons':inline(buttons)}

    return moviesDict if moviesDict['display']['imgs'] else None

def get_info(show):
    r = requests.get(show['url']).text
    soup = BeautifulSoup(r, 'html.parser')
    soup_xpath = etree.HTML(str(soup))
    movieTable = soup.select('table.movieTable tr:not(:where(tr:nth-child(1),tr:last-child)) td')
    movieTable_text = [movieTable[i].text for i in range(0,len(movieTable))]
    rate = soup_xpath.xpath('//*[@id="mainLoad"]/div[1]/div[3]/div[2]/span[1]/span[1]/text()')
    story = soup_xpath.xpath('//*[@id="mainLoad"]/div[1]/div[4]/div[2]/text()')

    return {'show':show, 'info':movieTable_text, 'story':story, 'rate':rate}

def get_season(show):
    r = requests.get(show).text
    soup = BeautifulSoup(r, 'html.parser')
    soup_xpath = etree.HTML(str(soup))
    seasons = soup_xpath.xpath('//*[@id="mainLoad"]/div[2]/div[2]/div/a/@href')

    return seasons[::-1]

def get_episode(show):
    r = requests.get(show).text
    soup = BeautifulSoup(r, 'html.parser')
    soup_xpath = etree.HTML(str(soup))
    episode = soup_xpath.xpath('//*[@id="mainLoad"]/div[3]/div[2]/a/@href')

    return episode[::-1]

def get_links(show, type):

    # for none found movies
    # try:
    r = s.get(show)

    soup = BeautifulSoup(r.content, 'html.parser')
    soup_xpath = etree.HTML(str(soup))
    links_table = soup_xpath.xpath('//*[@id="watch_dl"]/table/tbody/tr/td[position()<=3 and position()>1]/text()')
    iframe_src = soup.iframe.attrs["src"]

    r = s.get(f"https://giga.egybest.kim{iframe_src}")
    soup = BeautifulSoup(r.content, "html.parser")
    source = f'https://giga.egybest.kim{soup.source.attrs["src"]}'

    file = s.get(url=source)
    links = [re.search('(http.*?)/stream/', str(line)).group(1) + f'/{type}/' + re.search('/stream/(.*?)/stream.m3u8',str(line)).group(1) for line in file.iter_lines() if b'http' in line]
    # except:
    #     return None
    # else:
    return {'links': links[::-1], 'links_table': links_table}