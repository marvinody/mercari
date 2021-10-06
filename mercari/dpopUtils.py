from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
import base64
import json


private_key = ec.generate_private_key(
    ec.SECP256R1()
)

data = b"this is some data I'd like to sign"

signature = private_key.sign(
    data,
    ec.ECDSA(hashes.SHA256())
)

def intToBase64URL(n):
    nBytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
    return bytesToBase64URL(nBytes)

def strToBase64URL(s):
    sBytes = bytes(s, 'utf-8')
    return bytesToBase64URL(sBytes)

def bytesToBase64URL(b):
    return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')


def public_key_to_JWK(public_key):
    public_numbers = public_key.public_numbers()
    x,y = (public_numbers.x, public_numbers.y)

    return {
      "crv": "P-256",
      "kty": "EC",
      "x": intToBase64URL(x),
      "y": intToBase64URL(y),
    }
def public_key_to_Header(public_key):
    return {
      "typ": "dpop+jwt",
      "alg": "ES256",
      "jwk": public_key_to_JWK(public_key)
    }

public_key = private_key.public_key()

header = public_key_to_Header(public_key)

payload = {
  "iat": 1633388418,
  "jti": "eca01827-1724-4eea-8eb6-4532616aed9f",
  "htu": "https://api.mercari.jp/search_index/search",
  "htm": "GET"
}

print(header)
print(payload)
headerString = json.dumps(header)
payloadString = json.dumps(payload)

dataToSign = f"{strToBase64URL(headerString)}.{strToBase64URL(payloadString)}"

signature = private_key.sign(
    bytes(dataToSign, 'utf-8'),
    ec.ECDSA(hashes.SHA256())
)

# print(signature.hex())
# print(len(signature))
print(len(signature))
r, s = utils.decode_dss_signature(signature)
print(r.bit_length(), r)
print(s.bit_length(), s)
signatureString = intToBase64URL(s)

print(f"{dataToSign}.{signatureString}")


