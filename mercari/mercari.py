import uuid
import json
import requests

from .DpopUtils import generate_DPOP

rootURL = "https://api.mercari.jp/"
rootProductURL = "https://jp.mercari.com/item/"
searchURL = "{}v2/entities:search".format(rootURL)


class MercariSearchStatus:
    DEFAULT = "STATUS_DEFAULT"
    ON_SALE = "STATUS_ON_SALE"
    SOLD_OUT = "STATUS_SOLD_OUT"


class MercariSort:
    SORT_DEFAULT = 'SORT_DEFAULT'
    SORT_CREATED_TIME = 'SORT_CREATED_TIME'
    SORT_NUM_LIKES = 'SORT_NUM_LIKES'
    SORT_SCORE = 'SORT_SCORE'
    SORT_PRICE = 'SORT_PRICE'

class MercariOrder:
    ORDER_DESC = 'ORDER_DESC'
    ORDER_ASC = 'ORDER_ASC'

class MercariItemStatus:
    ITEM_STATUS_UNSPECIFIED = 'ITEM_STATUS_UNSPECIFIED'
    ITEM_STATUS_ON_SALE = 'ITEM_STATUS_ON_SALE'
    ITEM_STATUS_TRADING = 'ITEM_STATUS_TRADING'
    ITEM_STATUS_SOLD_OUT = 'ITEM_STATUS_SOLD_OUT'
    ITEM_STATUS_STOP = 'ITEM_STATUS_STOP'
    ITEM_STATUS_CANCEL = 'ITEM_STATUS_CANCEL'
    ITEM_STATUS_ADMIN_CANCEL = 'ITEM_STATUS_ADMIN_CANCEL'

class Item:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['productID']
        self.productURL = "{}{}".format(rootProductURL, kwargs['productID'])
        self.imageURL = kwargs['imageURL']
        self.productName = kwargs['name']
        self.price = kwargs['price']
        self.status = kwargs['status']
        self.soldOut = kwargs['status'] != MercariItemStatus.ITEM_STATUS_SOLD_OUT

    @staticmethod
    def fromApiResp(apiResp):
        return Item(
            productID=apiResp['id'],
            name=apiResp["name"],
            price=apiResp["price"],
            status=apiResp['status'],
            imageURL=apiResp['thumbnails'][0],
        )


# returns [] if resp has no items on it
# returns [Item's] otherwise
def parse(resp):
    if(len(resp["items"]) == 0):
        return [], False, None

    respItems = resp["items"]
    nextPageToken = resp["meta"]["nextPageToken"]
    return [Item.fromApiResp(item) for item in respItems], bool(nextPageToken), nextPageToken


def fetch(url, data):
    DPOP = generate_DPOP(
        # let's see if this gets blacklisted, but it also lets them track
        uuid="Mercari Python Bot",
        method="POST",
        url=url,
    )

    headers = {
        'DPOP': DPOP,
        'X-Platform': 'web',  # mercari requires this header
        'Accept': '*/*',
        'Accept-Encoding': 'deflate, gzip',
        'Content-Type': 'application/json; charset=utf-8',
        # courtesy header since they're blocking python-requests (returns 0 results)
        'User-Agent': 'python-mercari',
    }
    
    serializedData = json.dumps(data, ensure_ascii=False).encode('utf-8')

    r = requests.post(url, headers=headers, data=serializedData)

    r.raise_for_status()

    return parse(r.json())

# not sure if the v1 prefix ever changes, but from quick testing, doesn't seem like it
def pageToPageToken(page):
    return "v1:{}".format(page)

# returns an generator for Item objects
# keeps searching until no results so may take a while to get results back

def search(keywords, sort=MercariSort.SORT_CREATED_TIME, order=MercariOrder.ORDER_DESC, status=MercariSearchStatus.ON_SALE, exclude_keywords=""):

    # This is per page and not for the final result
    limit = 120

    data = {
        # this seems to be random, but we'll add a prefix for mercari to track if they wanted to
        "userId": "MERCARI_BOT_{}".format(uuid.uuid4()), 
        "pageSize": limit,
        "pageToken": pageToPageToken(0),
        # same thing as userId, courtesy of a prefix for mercari
        "searchSessionId": "MERCARI_BOT_{}".format(uuid.uuid4()),
        # this is hardcoded in their frontend currently, so leaving it
        "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
        "searchCondition": {
            "keyword": keywords,
            "sort": sort,
            "order": order,
            "status": [status],
            "excludeKeyword": exclude_keywords,
        },
        # I'm not certain what these are, but I believe it's what mercari queries against
        # this is the default in their site, so leaving it as these 2
        "defaultDatasets": [
            "DATASET_TYPE_MERCARI",
            "DATASET_TYPE_BEYOND"
        ]
    }

    has_next_page = True

    while has_next_page:
        items, has_next_page, next_page_token = fetch(searchURL, data)
        yield from items
        data['pageToken'] = next_page_token
