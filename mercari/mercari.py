import uuid
import json
import requests

from enum import StrEnum
from typing import Iterator

from .DpopUtils import generate_DPOP

rootURL = "https://api.mercari.jp/"
rootProductURL = "https://jp.mercari.com/item/"
searchURL = "{}v2/entities:search".format(rootURL)
brandsUrl = "{}services/productcatalog/v1/get_item_brands".format(rootURL)
categoriesUrl = "{}services/productcatalog/v1/get_item_categories".format(
    rootURL)


class MercariSearchStatus(StrEnum):
    DEFAULT = "STATUS_DEFAULT"
    ON_SALE = "STATUS_ON_SALE"
    SOLD_OUT = "STATUS_SOLD_OUT"


class MercariSort(StrEnum):
    SORT_DEFAULT = 'SORT_DEFAULT'
    SORT_CREATED_TIME = 'SORT_CREATED_TIME'
    SORT_NUM_LIKES = 'SORT_NUM_LIKES'
    SORT_SCORE = 'SORT_SCORE'
    SORT_PRICE = 'SORT_PRICE'


class MercariOrder(StrEnum):
    ORDER_DESC = 'ORDER_DESC'
    ORDER_ASC = 'ORDER_ASC'


class MercariItemStatus(StrEnum):
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


class Brand:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.subname = kwargs['subname']

    @staticmethod
    def fromApiResp(apiResp):
        return Brand(
            id=apiResp["id"],
            name=apiResp["name"],
            subname=apiResp["subname"],
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return "Brand(id={}, name={}, subname={})".format(self.id, self.name, self.subname)


class Category:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

    @staticmethod
    def fromApiResp(apiResp):
        return Category(
            id=apiResp["id"],
            name=apiResp["name"],
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return "Category(id={}, name={})".format(self.id, self.name)


def makeHeaders(url):
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

    return headers


def fetch(url, data):

    headers = makeHeaders(url)

    r = requests.post(url, headers=headers, json=data)

    r.raise_for_status()

    return r.json()


def search_page(
    *noneArgs,
    pageToken: str = "",
    keywords: str = "",
    exclude_keywords: str = "",
    brandIds: list[int] = [],
    categoryIds: list[int] = [],
    sort: MercariSort = MercariSort.SORT_CREATED_TIME,
    order: MercariOrder = MercariOrder.ORDER_DESC,
    status: MercariSearchStatus = MercariSearchStatus.ON_SALE,
    limit: int = 120,
) -> tuple[list[Item], str]:
    if len(noneArgs) > 0:
        raise ValueError("Don't pass in unnamed parameters to search")

    data = {
        # this seems to be random, but we'll add a prefix for mercari to track if they wanted to
        "userId": "MERCARI_BOT_{}".format(uuid.uuid4()),
        "pageSize": limit,
        "pageToken": pageToken,
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
            "brandId": brandIds,
            "categoryId": categoryIds,
        },
        # I'm not certain what these are, but I believe it's what mercari queries against
        # this is the default in their site, so leaving it as these 2
        "defaultDatasets": [
            "DATASET_TYPE_MERCARI",
            "DATASET_TYPE_BEYOND"
        ]
    }

    apiResp = fetch(searchURL, data)

    return (
        [Item.fromApiResp(item) for item in apiResp["items"]],
        apiResp["meta"]["nextPageToken"],
    )


def search_all(
    *noneArgs,
    keywords: str = "",
    exclude_keywords: str = "",
    brandIds: list[int] = [],
    categoryIds: list[int] = [],
    sort: MercariSort = MercariSort.SORT_CREATED_TIME,
    order: MercariOrder = MercariOrder.ORDER_DESC,
    status: MercariSearchStatus = MercariSearchStatus.ON_SALE,
) -> Iterator[Item]:
    if len(noneArgs) > 0:
        raise ValueError("Don't pass in unnamed parameters to search")

    nextPageToken = ""
    hasNextPage = True

    while hasNextPage:
        (items, nextPageToken) = search_page(
            pageToken=nextPageToken,
            keywords=keywords,
            exclude_keywords=exclude_keywords,
            brandIds=brandIds,
            categoryIds=categoryIds,
            sort=sort,
            order=order,
            status=status,
        )
        yield from items
        hasNextPage = nextPageToken


def search(
    keywords="",
    exclude_keywords="",
    brandIds: list[int] = [],
    categoryIds: list[int] = [],
    sort=MercariSort.SORT_CREATED_TIME,
    order=MercariOrder.ORDER_DESC,
    status=MercariSearchStatus.ON_SALE,
) -> Iterator[Item]:
    yield from search_all(
        keywords=keywords,
        exclude_keywords=exclude_keywords,
        brandIds=brandIds,
        categoryIds=categoryIds,
        sort=sort,
        order=order,
        status=status,
    )


def brands_page(*noneArgs, pageToken: str = "") -> tuple[list[Brand], str]:
    if len(noneArgs) > 0:
        raise ValueError("Don't pass in unnamed parameters to search")

    data = {
        "pageToken": pageToken
    }

    apiResp = fetch(url=brandsUrl, data=data)

    return (
        [Brand.fromApiResp(brand) for brand in apiResp["itemBrands"]],
        apiResp["nextPageToken"],
    )


def brands_all() -> Iterator[Brand]:
    nextPageToken = ""
    hasNextPage = True

    while hasNextPage:
        (brands, nextPageToken) = brands_page(pageToken=nextPageToken)
        yield from brands
        hasNextPage = nextPageToken


def categories_page(*noneArgs, pageToken: str = "") -> tuple[list[Category], str]:
    if len(noneArgs) > 0:
        raise ValueError("Don't pass in unnamed parameters to search")

    data = {
        "pageToken": pageToken,
        "pageSize":	0,
        "flattenResponse": True,
    }

    apiResp = fetch(url=categoriesUrl, data=data)

    return (
        [Category.fromApiResp(category)
         for category in apiResp["itemCategories"]],
        apiResp["nextPageToken"],
    )


def categories_all() -> Iterator[Category]:
    nextPageToken = ""
    hasNextPage = True

    while hasNextPage:
        (categories, nextPageToken) = categories_page(pageToken=nextPageToken)
        yield from categories
        hasNextPage = nextPageToken
