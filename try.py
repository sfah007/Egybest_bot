import requests
from bs4 import BeautifulSoup
import urllib
import re
from fake_useragent import UserAgent

user = UserAgent()
headers = {'user-agent': user.random}

s = requests.Session()
s.cookies.set('PSSID', '1DJL3W5bGlXZshzXOqA3cltEJLzkUHehXfqKc3hEh5m3ZOH49lPX7grhwHFwuFSBTRfOJ0aAKMZw9ld3FM-JWL94aZYOy0Lf-uEsStm0WVArytEybnTLeS41i2Pob1%2Ct', domain='giga.egybest.kim', expires=None)
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



