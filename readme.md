# Mercari Wrapper

A simple api wrapper around the Mercari jp site.

Simple usage can be something like

```python
import mercari

for item in mercari.search("東方 ふもふも"):
    print("{}, {}".format(item.productName, item.productURL))
```

the item object contains the following properties
- productURL
- imageURL
- productName
- price
- productCode
