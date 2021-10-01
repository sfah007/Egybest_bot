import requests
from bs4 import BeautifulSoup
import urllib
import re
from fake_useragent import UserAgent

user = UserAgent()
headers = {'user-agent': user.random}
# cookies = {'PSSID':'sqrO3-GC3jTyM-5q6IYPW0JW4xSiTIXR-FDd5TUkSoi8UOkoKKMdWmpyW8gz2uykrsxZzrgiKrjq6dsY61o7ROVjfWZ6CYFpmuX1rNFX70x5C6AFIHuiQaYiFUuEvN-H',
#             'JS_TIMEZONE_OFFSET':'-7200',
#             'push_subscribed':'ignore',
#             'EGUDI':'lFcVBIvskXzPyFs2.0ad44e25a1446d2e6865b4354c9976399fa56d066fcc84280ff1da36eb1570848a23a4d2b368ba8169e733d3228b5ade37dab226078640be8abcaa7b000696ae',
#             'c952f23a':'KRRRzlZQsRzRVRzPiPPrYbpPYrzVzRzopEKYrzRVPniPPPPPIwRPCzVqzRzSZlRzRVRzwyMErrqnAPVqMRMTzRi-30bdf693b334c6c6a6ed74c553ddeadc',
#            }

s = requests.Session()
s.cookies.set('PSSID', 'iYj6tfPiwvrajztIdPAFQwXxyobbStVUrJl9lsbHBu1ryYi9Zf2qmwh%2CnOBLATHlD%2Ccy5cplJNDyX0eYJFTRw00Szwa9pVrLFBnMXZBL-gznKUKlDFhHoDdY6nXsad-t', domain='giga.egybest.kim', expires=None)
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



