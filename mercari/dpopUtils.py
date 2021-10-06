from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from time import time
import base64
import json

def intToBytes(n):
  return n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')

def intToBase64URL(n):
    return bytesToBase64URL(intToBytes(n))

def strToBase64URL(s):
    sBytes = bytes(s, 'utf-8')
    return bytesToBase64URL(sBytes)

def bytesToBase64URL(b):
    return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')


def public_key_to_JWK(public_key):
    public_numbers = public_key.public_numbers()
    x,y = (public_numbers.x, public_numbers.y)

    return {
      "crv": "P-256", # we're hardcoding this because SECP256R1 === P-256
      "kty": "EC", # and we're always using EC, so hardcoded
      "x": intToBase64URL(x),
      "y": intToBase64URL(y),
    }
def public_key_to_Header(public_key):
    return {
      "typ": "dpop+jwt",
      "alg": "ES256", # we're hardcoding because we're not changing algo ever
      "jwk": public_key_to_JWK(public_key)
    }

# this is an util that will generate a pseudo-DPOP
# Mercari fucked up how they generate these tokens and it's not compliant with the actual spec
# But the way they screwed up makes it much easier for us.
# We can just generate random ECC keys and sign any data and as long as the keys match and signature
# is valid, then mercari doesn't care if it's a new key.
# So let's make a new key everytime so they dont blacklist any JWK public keys or something dumb
# Just make sure the method & url match the endpoint you're trying to call
# uuid SHOULD probably be a real uuid, but it doesn't seem like they're even checking this for much.
# maybe some tracking for later, so making it purely random just like the key will make it really hard
# for mercari to detect this as inorganic traffic if spread across IPs
# The biggest giveaway MAY be multiple keys/uuid being used for 1 IP.
# But then you just swap it every week or so instead and problem solved (hopefully)
def generate_DPOP(*, uuid, method, url):

    private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    # DPOP lets you specify
    payload = {
      "iat": int(time()), # 1633388418,
      "jti": uuid, # "eca01827-1724-4eea-8eb6-4532616aed9f",
      "htu": url, # "https://api.mercari.jp/search_index/search",
      "htm": method.upper(), # "GET"
    }

    # we need to give our public key to mercari, so export
    public_key = private_key.public_key()

    # create header including the JWK encoding of the key & metadata about algo we'll sign with
    header = public_key_to_Header(public_key)

    # JWT expects everything to be JSON string -> base 64 encoded
    headerString = json.dumps(header)
    payloadString = json.dumps(payload)

    # So let's encode them and add a delimiter of .
    dataToSign = f"{strToBase64URL(headerString)}.{strToBase64URL(payloadString)}"

    # Sign our resulting big string with the sk and a hardcoded algorithm
    signature = private_key.sign(
        bytes(dataToSign, 'utf-8'),
        ec.ECDSA(hashes.SHA256())
    )

    # Cryptolibrary returns an encoded structure that the webapi decryption doesn't like
    # So we need a special format. We pull out the r, s values from our DSS signature (which are ints)
    r, s = utils.decode_dss_signature(signature)
    rB, sB = intToBytes(r), intToBytes(s)

    # and then we just concat the byte representations of the r,s values & base64 the whole monster
    signatureString = bytesToBase64URL(rB + sB)

    # and concat the signature at the end
    return f"{dataToSign}.{signatureString}"

if __name__ == '__main__':
    print(generate_DPOP(uuid='DUMMY_UUID', method="GET", url="https://api.mercari.jp/search_index/search"))
