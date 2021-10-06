# Mercari Wrapper (Archived)

This project has been archived from python because of Mercari changes to their site.

I have some starter code to help anyone who's trying to generate an API access token in `mercari/dpopUtils.py` but the cryptography library is above my head. The missing part that's failing is that the signature returned is DER encoded around ASN.1 encoding of a `Dss-Sig-Value` sequence. I think it needs to be decoded for a valid JWT to be made...

But I'm bored of this honestly, and I'm moving my code to the JavaScript versions

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

## Google Proxy

By default, the wrapper will try to use a google proxy to hide traffic. This is a bit finicky and I think google has wised up recently. To disable it and have your requests by direct to mercari, use it in the following way

```python
import mercari

for item in mercari.search("東方 ふもふも", use_google_proxy=False):
    print("{}, {}".format(item.productName, item.productURL))
```

The wrapper will throw on any 4xx or 5xx http status code.

Main reason I've seen errors is because mercari decides to throw 403 if they blacklist your IP. I've tried to get around this with the google proxy, but it seems like google themselves are blocking either the IP or the mercari domain.
