import os
import re
from enum import Enum
from math import ceil

import requests
from bs4 import BeautifulSoup

rootURL = "https://www.mercari.com/jp/search/"


class Item:
    def __init__(self, *args, **kwargs):
        self.productURL = kwargs['productURL']
        self.imageURL = kwargs['imageURL']
        self.productName = kwargs['productName']
        self.price = kwargs['price']
        self.productCode = kwargs['productCode']


def createItem(productHTML):
    # if this script breaks here, use the following line to see the new html and adjust it
    # print(productHTML)

    url = productHTML.find('a')['href']
    name = productHTML.find('h3').text
    imageUrl = productHTML.find('img')['data-src']
    # this will pull a bunch of junk with it like yen sign and weird chars
    priceText = productHTML.find('div', class_='items-box-price').text
    # so we just remove anything that's not a digit
    priceDigits = re.sub('[^0-9]', '', priceText)
    # and just parse into int
    price = int(priceDigits)

    return Item(
        productURL=url,
        imageURL=imageUrl,
        productName=name,
        price=price,
        productCode=url[url.rstrip('/').rindex("/")+1:],
    )


def parse(url, data):
    # returns [] if page has no items on it
    # returns [Item's] otherwise
    headers = {
        "Accept-Encoding": "deflate, gzip",
        "Host": "www.mercari.com",
        "User-Agent": "a user agent string is used to detect bots or something?",
    }
    r = requests.get(url, params=data, headers=headers)
    html = BeautifulSoup(r.text, "html.parser")
    return html.find_all("section", class_="items-box")


# returns an generator for Item objects
# keeps searching until no results so may take a while to get results back
def search(keywords):
    data = {
        "keyword": keywords,
        "page": 1,
        "status_on_sale": 1,
    }
    items = parse(rootURL, data)

    while items:
        yield from [createItem(item) for item in items]
        data['page'] += 1
        items = parse(rootURL, data)
