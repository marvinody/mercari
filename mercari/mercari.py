import os
import random
import re
import urllib.parse
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
