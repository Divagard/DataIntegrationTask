from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

url = ['https://www.circl.lu/doc/misp/feed-osint/','https://www.botvrij.eu/data/feed-osint/']
change = True
urls1 = []
urls2 = []
for i in url:
    reqs = requests.get(i)
    soup = BeautifulSoup(reqs.text, 'html.parser')


    for link in soup.find_all('a'):
        if link.get('href').endswith('.json'):
            if change:
                if len(urls1)==100:
                    change = False
                    break
                else:
                    urls1.append(i + link.get('href'))
            else:
                if len(urls2)==100:
                    break
                else:
                    urls2.append(i+link.get('href'))

