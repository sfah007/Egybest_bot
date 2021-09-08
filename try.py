import requests
from fake_useragent import UserAgent
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = 'https://giga.egybest.kim/movie/escape-room-tournament-of-champions-2021/?ref=home-trends'

chrome_options = webdriver.ChromeOptions()
user = UserAgent()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(r'C:\Users\MAMDO\.wdm\drivers\chromedriver\win32\93.0.4577.15\chromedriver.exe', options=chrome_options)

browser.get(url)
browser.add_cookie(cookies)
browser.refresh()
browser._switch_to.frame(browser.find_element_by_xpath('//*[@id="watch_dl"]/div[1]/iframe'))
print()
browser.quit()


# element = browser.find_element_by_xpath('//*[@id="watch_dl"]/div[1]/iframe')
# element.click()
# browser.switch_to_frame(element)
#
# # wait until disappear
# WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'ico-play-circle')))
# source = browser.find_element_by_xpath('//*[@id="video_html5_api"]/source').get_attribute('src')


