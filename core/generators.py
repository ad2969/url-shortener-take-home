import random
import hashlib
import secrets


# generate a 4-digit pin and it's associated hash
def generate_pin_and_hash() -> (str,str):
    pincode = random.randint(0,9999)
    pincode_hash = convert_pin_to_hash(pincode)
    return (str(pincode).zfill(4), pincode_hash)

def convert_pin_to_hash(pincode) -> str:
    pincode_encoded = pincode.to_bytes(2, 'big')
    return hashlib.md5(pincode_encoded).hexdigest() # 32-char strings


# generate a url 10-character hash
def generate_hash_url() -> str:
    token = secrets.token_urlsafe(16)[:10]
    return token