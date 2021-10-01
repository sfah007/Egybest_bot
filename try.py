import requests
from bs4 import BeautifulSoup
import urllib
import re
from fake_useragent import UserAgent

user = UserAgent()
headers = {'user-agent': user.random}

s = requests.Session()
s.cookies.set('PSSID', 'B-0MebEG5cd-WReJN4OM%2CHsKlJKhYoXgPjhYsAHh-qDFj3EoatMBwuTXUTfQ-ADSPNCzDX2UhaTW9-ZyzbuTpLEkRsA7r6E8jWVaExFgpkFcgDy%2CFzEjF3jDmTYL3mGC', domain='giga.egybest.kim', expires=None)
s.headers.update(headers)

r = s.get('https://giga.egybest.kim/movie/my-name-is-pauli-murray-2021/?ref=movies-p1')

soup = BeautifulSoup(r.content, 'html.parser')
iframe_src = soup.iframe.attrs["src"]

r = s.get(f"https://giga.egybest.kim{iframe_src}")

soup = BeautifulSoup(r.content, "html.parser")
source = f'https://giga.egybest.kim{soup.source.attrs["src"]}'


file = requests.get(url=source)
links = [re.search(b'(http.*?)/stream/', line).group(1) + b'/watch/' + re.search(b'/stream/(.*?)/stream.m3u8', line).group(1) for line in file.iter_lines() if b'http' in line] # re.search('(http.*?)/stream/', str(line)).group(1) + f'/{type}/' + re.search('/stream/(.*?)/stream.m3u8', str(line)).group(1)
print(links)



