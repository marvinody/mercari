import os
import random
import re
import urllib.parse
from enum import Enum
from math import ceil

import requests
from bs4 import BeautifulSoup

rootURL = "https://www.mercari.com"
searchURL = "{}/jp/search".format(rootURL)

SOLD_OUT_TEXT = "該当する商品が見つかりません"


class Item:
    def __init__(self, *args, **kwargs):
        self.productURL = "{}{}".format(rootURL, kwargs['productURL'])
        self.imageURL = kwargs['imageURL']
        self.productName = kwargs['productName']
        self.price = kwargs['price']
        self.productCode = kwargs['productCode']


pat = re.compile(r"/jp/items/(.*)[/\?]")


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
    productCodeSearch = pat.search(url)
    productCode = productCodeSearch.group(
        1) if productCodeSearch else productName
    productCode = productCode.rstrip('/')

    return Item(
        productURL=url,
        imageURL=imageUrl,
        productName=name,
        price=price,
        productCode=productCode)


def isSoldOut(html):
    try:
        desc = html.find("p", class_="search-result-description")
        return SOLD_OUT_TEXT in desc.text
    except AttributeError:
        return False


def parse(text):
    # returns [] if page has no items on it
    # returns [Item's] otherwise

    html = BeautifulSoup(text, "html.parser")
    soldOut = isSoldOut(html)
    if soldOut:
        return []
    items = html.find_all("section", class_="items-box")
    return [createItem(item) for item in items]


def fetch(url, data):
    # let's build up the url ourselves
    # I know requests can do it, but I need to do it myself cause we need
    # special encoding!
    url = "{}?{}".format(
        url,
        urllib.parse.urlencode(data)
    )
    # now we'll escape everything again so google doesn't parse it themselves
    # we need to pass these params into the mercari site, not google's
    url = urllib.parse.quote_plus(url)

    # use google's proxy because mercari blocks some servers it seems like?
    # they have a bunch, so let's pick a random one each time incase they're tracking us...
    num = random.randint(0, 32)
    url = "https://images{}-focus-opensocial.googleusercontent.com/gadgets/proxy?container=none&url={}".format(
        num,
        url)
    r = requests.get(url)
    return parse(r.text)


# returns an generator for Item objects
# keeps searching until no results so may take a while to get results back
def search(keywords):
    data = {
        "keyword": keywords,
        "page": 1,
        "status_on_sale": 1,
    }
    items = fetch(searchURL, data)

    while items:
        yield from items
        data['page'] += 1
        items = fetch(searchURL, data)
