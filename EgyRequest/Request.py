import requests
import urllib
import re
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pprint import pprint
from EgybestBot.EgyFucntions.Function import inline
from telegram.files.inputmedia import InputMediaPhoto
from telegram import InlineKeyboardButton

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
    movieTable = soup.select('table.movieTable tr:not(tr:nth-child(1)) td')
    movieTable_text = [movieTable[i].text for i in range(0,len(movieTable))]
    rate = soup_xpath.xpath('//*[@id="mainLoad"]/div[1]/div[3]/div[2]/span[1]/span[1]/text()')
    story = soup_xpath.xpath('//*[@id="mainLoad"]/div[1]/div[4]/div[2]/text()')
    links_table = soup_xpath.xpath('//*[@id="watch_dl"]/table/tbody/tr/td[position()<=3 and position()>1]/text()')

    return {'show':show, 'info':movieTable_text, 'story':story, 'rate':rate, 'links_table':links_table}


def get_links(show):
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    chrome_options = webdriver.ChromeOptions()
    user = UserAgent()
    chrome_options.add_argument(f'user-agent={user.random}')
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(r'C:\Users\MAMDO\.wdm\drivers\chromedriver\win32\92.0.4515.107\chromedriver.exe', options=chrome_options)
    browser.get(show['url'])

    element = browser.find_element_by_xpath('//*[@id="watch_dl"]/div[1]/iframe')
    element.click()
    browser.switch_to_frame(element)

    # wait until disappear
    WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'ico-play-circle')))
    source = browser.find_element_by_xpath('//*[@id="video_html5_api"]/source').get_attribute('src')

    headers = {'user-agent': user.random}

    request=urllib.request.Request(source,None,headers) #The assembled request
    file = urllib.request.urlopen(request)
    links = [re.search('(http.*?)/stream/', str(line)).group(1) + '/watch/' + re.search('/stream/(.*?)/stream.m3u8', str(line)).group(1) for line in file if 'http' in str(line)]

    return links[::-1]