# Mercari Wrapper

A simple api wrapper around the Mercari jp site.

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


## Development

Clone this repo, install the dependencies in `requirement.txt` and off you go.

## Deploying / Publishing

- `python setup.py sdist`

- `twine upload dist/mercari-<version>.tar.gz`
