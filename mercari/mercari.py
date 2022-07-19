import os
import random
import re
import urllib.parse
from enum import Enum
from math import ceil

import requests
from .DpopUtils import generate_DPOP

rootURL = "https://api.mercari.jp/"
rootProductURL = "https://jp.mercari.com/item/"
searchURL = "{}search_index/search".format(rootURL)


class Item:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['productID']
        self.productURL = "{}{}".format(rootProductURL, kwargs['productID'])
        self.imageURL = kwargs['imageURL']
        self.productName = kwargs['name']
        self.price = kwargs['price']
        self.status = kwargs['status']
        self.soldOut = kwargs['status'] != "on_sale"

    @staticmethod
    def fromApiResp(apiResp):
        return Item(
            productID=apiResp['id'],
            name=apiResp["name"],
            price=apiResp["price"],
            status=apiResp['status'],
            imageURL=apiResp['thumbnails'][0],
            condition=apiResp['item_condition']["id"],
            itemCategory=apiResp['item_category']['name'],
        )


def parse(resp):
    # returns [] if resp has no items on it
    # returns [Item's] otherwise
    if resp["meta"]["num_found"] == 0:
        return [], False

    respItems = resp["data"]
    return [Item.fromApiResp(item) for item in respItems], resp["meta"]["has_next"]


def fetch(baseURL, data):
    # let's build up the url ourselves
    # I know requests can do it, but I need to do it myself cause we need
    # special encoding!
    url = "{}?{}".format(
        baseURL,
        urllib.parse.urlencode(data)
    )

    DPOP = generate_DPOP(
        # let's see if this gets blacklisted, but it also lets them track
        uuid="Mercari Python Bot",
        method="GET",
        url=baseURL

    )

    headers = {
        'DPOP': DPOP,
        'X-Platform': 'web',  # mercari requires this header
        'Accept': '*/*',
        'Accept-Encoding': 'deflate, gzip'
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return parse(r.json())


# returns an generator for Item objects
# keeps searching until no results so may take a while to get results back
def search(keywords, sort="created_time", order="desc", status="on_sale", limit=120):
    data = {
        "keyword": keywords,
        "limit": 120,
        "page": 0,
        "sort": sort,
        "order": order,
        "status": status,
    }
    has_next_page = True

    while has_next_page:
        items, has_next_page = fetch(searchURL, data)
        yield from items
        data['page'] += 1
