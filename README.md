# Mercari Wrapper

A simple api wrapper around the Mercari jp site.

**This package does not use scraping of the underlying HTML**, it simulates API requests by generating tokens according to how Mercari.JP expects it. This should result in quicker response times, less breaking changes (due to layout swaps), and overall better experience.

## Searching

Simple usage can be something like

```python
import mercari

for item in mercari.search("東方 ふもふも"):
    print("{}, {}".format(item.productName, item.productURL))
```

**The search call will take a long time because it goes through all the pages to find every item.** It does not return parts where you paginate yourself.

the item object contains the following properties:

- id
- productURL
- imageURL
- productName
- price
- status
- soldOut
- created
- updated
- auction (can be None) with following properties
    - bid_deadline (can be different types depending on search vs item info)
    - total_bid
    - highest_bid

If you want to do more specific searching, you can use something like the following
```python
from mercari import search, MercariSearchStatus, MercariSort, MercariOrder

for item in search(
        "",
        sort=MercariSort.SORT_PRICE,
        order=MercariOrder.ORDER_DESC,
        status=MercariSearchStatus.SOLD_OUT
    ):
    print("{}, {}".format(item.productName, item.productURL))

```

The defaults are currently:

- `sort=MercariSort.SORT_CREATED_TIME`
- `order=MercariOrder.ORDER_DESC` 
- `status=MercariSearchStatus.ON_SALE`

Which will sort by most recent to oldest, and only show on sale item.

### MercariSort
- STATUS_DEFAULT
- STATUS_ON_SALE
- STATUS_SOLD_OUT
### MercariOrder
- SORT_DEFAULT
- SORT_CREATED_TIME
- SORT_NUM_LIKES
- SORT_SCORE
- SORT_PRICE
### MercariSearchStatus
- ORDER_DESC
- ORDER_ASC

You can also pass `excluded_keywords="something to exclude"` if you want to remove certain pieces from your search

## Item Info

```python
from mercari import getItemInfo

itemId = 'm48957867611' # get it using a search or some other way
# default country code is US, so don't need to pass if you're fine with US
item = getItemInfo(itemId, country_code="US")
print(item.id, item.price, item.name)
```

The item returned is properly typed so you can explore it using intellisense in your IDE. I don't do any safe checks or conversions on parameters but some gotchas:
- status is just a string which can be `on_sale`
- price is the JPY price, but `converted_price` contains the currency according to the `country_code` you pass in (USD by default)
- any timestamp field (`created`, `updated`) come back as int with the unix timestamp in seconds
- pretty much 90% of fields, I'm unsure if they're useful (wtf is a pager id? additional_service??)
- some properties I didn't get samples that contained property so they're blank
    - `comments` - empty array always
    - `application_attributes` - empty dict always
    - `hash_tags` - empty array always
    - `additional_services` - empty array always

Another big gotcha is that I didn't bother adding great error handling, so if an item is expired, it'll throw a request error with like 403 if it used to be an item, or 404 is the itemId doesn't exist. If people are still using this, I'll add that in but I'm not consuming this lib myself any more.


## Development

Clone this repo, install the dependencies in `requirement.txt` and off you go.

## Deploying / Publishing

- `python setup.py sdist`

- `twine upload dist/mercari-<version>.tar.gz`
