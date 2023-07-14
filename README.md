# Mercari Wrapper

A simple api wrapper around the Mercari jp site.

## Installation

`pip install mercari`

## Usage

Simple usage can be something like

```python
import mercari

for item in mercari.search_all("東方 ふもふも"):
    print("{}, {}".format(item.productName, item.productURL))
```

**The search call will take a long time because it goes through all the pages to find every item.** It does not return parts where you paginate yourself. If you want pagination or limited searches, look at `search_page` below

the item object contains the following properties:

- id
- productURL
- imageURL
- productName
- price
- status
- soldOut


## Advanced Usage

If you want to do more specific searching, you can use something like the following
```python
from mercari import search_all, MercariSearchStatus, MercariSort, MercariOrder

for item in search_all(
        keywords="",
        sort=MercariSort.SORT_PRICE,
        order=MercariOrder.ORDER_DESC,
        status=MercariSearchStatus.SOLD_OUT
    ):
    print("{}, {}".format(item.productName, item.productURL))

```

### Enums
The defaults are currently:

- `sort=MercariSort.SORT_CREATED_TIME`
- `order=MercariOrder.ORDER_DESC` 
- `status=MercariSearchStatus.ON_SALE`

Which will sort by most recent to oldest, and only show on sale item.

#### MercariSort
- `STATUS_DEFAULT`
- `STATUS_ON_SALE`
- `STATUS_SOLD_OUT`
#### MercariOrder
- `SORT_DEFAULT`
- `SORT_CREATED_TIME`
- `SORT_NUM_LIKES`
- `SORT_SCORE`
- `SORT_PRICE`
#### MercariSearchStatus
- `ORDER_DESC`
- `ORDER_ASC`

You can pass `excluded_keywords="something to exclude"` if you want to remove certain pieces from your search

If you know brand or category IDs of a specific search query (use the website to narrow these down for your use-case), you can pass them in a list format to allow querying by name (keywords not needed, just be aware of large amount of results)

### Examples

The following examples are contrived and may not result in items when using it. Change the query parameters to fit your use-case, this is just to learn how to format the functions & use them.


#### All Parameters
```python
from mercari import search_all, MercariSearchStatus, MercariSort, MercariOrder

# Using all parameters
for item in search_all(
        keywords="I want to search for this",
        exclude_keywords="but exclude these",
        brandIds=[13], # Note that it must be a list. You can pass multiple IDs if you want
        categoryIds=[25], # Same Array
        sort=MercariSort.SORT_PRICE, # these are all enums to make sure they're correctly typed
        order=MercariOrder.ORDER_DESC,
        status=MercariSearchStatus.SOLD_OUT,
    ):
    print("{}, {}".format(item.productName, item.productURL))
```

#### One Page Search
```python
from mercari import search_page, MercariSort

# Searching using a page (uses all the same params as above if you want)
(results, nextPageToken) = search_page(
    brandIds=[17716], # Note that it must be a list. You can pass multiple IDs if you want
    categoryIds=[2], # Same Array
    sort=MercariSort.SORT_PRICE, # these are all enums to make sure they're correctly typed
    limit=10, # this is only available on search_page(), not search or search_all. Range is from 1 to 120
)
for item in results:
    print("{}, {}".format(item.productName, item.productURL))
```

#### Brand + Category lists
```python
from mercari import brands_all, categories_all

# this will print like 50,000 lines - don't run it in console, save to a file if you need to go through them by hand...
# it's just here in case you wanted to pull them dynamically
for brand in brands_all():
    print(brand)

for category in categories_all():
    print(category)
```


## Development

Clone this repo, install the dependencies in `requirement.txt` and off you go.

## Deploying / Publishing

- `python setup.py sdist`

- `twine upload dist/mercari-<version>.tar.gz`
