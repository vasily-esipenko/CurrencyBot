from bs4 import BeautifulSoup as bs
import requests as r
from urllib.parse import urlparse
import lxml

usd = "https://www.google.com/search?q=dollar+to+ruble&oq=doll&aqs=chrome.1.69i59l3j0l3j46j0.1757j0j7&sourceid=chrome&ie=UTF-8"
eur = "https://www.google.com/search?q=eur+to+ruble&oq=eur+&aqs=chrome.0.69i59j69i57j0l6.1302j1j7&sourceid=chrome&ie=UTF-8"
btc = "https://www.google.com/search?q=btc+to+dollar&oq=btc&aqs=chrome.0.69i59j69i57j35i39j0l5.1828j1j7&sourceid=chrome&ie=UTF-8"


def currency(ccy):
    url = r.get(ccy)
    soup = bs(url.content, "lxml")
    res = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
    return str(res[1])
