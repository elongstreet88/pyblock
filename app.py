from Crypto.PublicKey import RSA
from hashlib import sha256
import json

def get_key_pair():
    key_pair = RSA.generate(bits=2048)
    print(f"Public key:  (n={hex(key_pair.n)}, e={hex(key_pair.e)})")
    print(f"Private key: (n={hex(key_pair.n)}, d={hex(key_pair.d)})")
    return key_pair

def sign_message(message, key_pair):
    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    signature = pow(hash, key_pair.d, key_pair.n)
    return signature

def verify_signature(message, key_pair, signature):
    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, key_pair.e, key_pair.n) 
    print("Signature valid:", hash == hashFromSignature)

def add_data(message, source_key_pair, destination_key_pair):
    return
    
def new_chain(chain_file_path,target_key_pair, origin_message):
    origin_key_pair = get_key_pair()

    signed_message = sign_message(f"{origin_message}{target_key_pair.n}".encode('utf-8'), origin_key_pair)

    block = {
        "s" : signed_message,
        "f" : origin_key_pair.n,
        "t" : target_key_pair.n,
        "m" : origin_message
    }

    with open(chain_file_path, 'w') as chain_file:
        json.dump(block, chain_file)

def add_block(self,source_key_pair, target_key_pair, message):
    return

chain_file_path = "./chain.json"
origin_message = "Hi"
first_key_pair = get_key_pair()
new_chain(chain_file_path, first_key_pair, origin_message)