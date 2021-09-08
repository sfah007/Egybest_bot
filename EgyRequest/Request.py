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

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
user = UserAgent()
chrome_options.add_argument(f'user-agent={user.random}')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
cookies = [{'name':'PSSID','value':'P2pu246tCRpEc3wHLdE4NxfA1u8Ywdvvexl9INvgFifu1%2CJBHb0V32gmu9yKDTGK25TAFuRNr8FFl2iPxHo7AQdmlNnvXf6PKbu3Q4BS%2CGsGwW%2CVK6ENsMIXBLMocqZU'}]

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
    browser = webdriver.Chrome(os.environ.get('CHROMEDRIVER_PATH'), options=chrome_options)  # os.environ.get('CHROMEDRIVER_PATH')
    browser.get(show)
    browser.delete_all_cookies()
    global cookies
    print(cookies)
    set_cookies = [browser.add_cookie(i) for i in cookies]
    browser.refresh()
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    soup_xpath = etree.HTML(str(soup))
    links_table = soup_xpath.xpath('//*[@id="watch_dl"]/table/tbody/tr/td[position()<=3 and position()>1]/text()')

    # for none found movies
    try:
        element = browser.find_element_by_xpath('//*[@id="watch_dl"]/div[1]/iframe')
        browser._switch_to.frame(element)
    except:
        browser.quit()
        return None,None

    try:
        source = browser.find_element_by_xpath('//*[@id="video_html5_api"]/source').get_attribute('src')
    except:
        browser._switch_to.default_content()
        element.click()
        browser._switch_to.frame(element)

        # wait until disappear
        WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'ico-play-circle')))
        source = browser.find_element_by_xpath('//*[@id="video_html5_api"]/source').get_attribute('src')
        cookies_list = browser.get_cookies()
        cookies = cookies_list

    headers = {'user-agent': user.random}
    request = urllib.request.Request(source, None, headers)  # The assembled request
    file = urllib.request.urlopen(request)
    links = [re.search('(http.*?)/stream/', str(line)).group(1) + f'/{type}/' + re.search('/stream/(.*?)/stream.m3u8',
                                                                                          str(line)).group(1) for line
             in file if 'http' in str(line)]

    return {'links': links[::-1], 'links_table': links_table}, browser