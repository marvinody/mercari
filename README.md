# Mercari Wrapper

A simple api wrapper around the Mercari jp site.

Simple usage can be something like

```python
import mercari

for item in mercari.search("東方 ふもふも"):
    print("{}, {}".format(item.name, item.productURL))
```

the item object contains the following properties:

- id
- productURL
- imageURL
- productName
- price
- status
- soldOut

## Google Proxy

~~By default, the wrapper will try to use a google proxy to hide traffic. This is a bit finicky and I think google has wised up recently. To disable it and have your requests by direct to mercari, use it in the following way~~

This is false now, and the google proxyy is removed. Because of how the api endpoint works, this had to be removed.

I've left this part in here to not gaslight any one that it never existed.

```python
import mercari

for item in mercari.search("東方 ふもふも", use_google_proxy=False):
    print("{}, {}".format(item.productName, item.productURL))
```

The wrapper will throw on any 4xx or 5xx http status code.

Main reason I've seen errors is because mercari decides to throw 403 if they blacklist your IP. I've tried to get around this with the google proxy, but it seems like google themselves are blocking either the IP or the mercari domain.


## Development

Clone this repo, install the dependencies in `requirement.txt` and off you go.

## Deploying / Publishing

- `python setup.py sdist`

- `twine upload dist/mercari-<version>.tar.gz`
