from Crypto.PublicKey import RSA
from hashlib import sha256
import json

def get_key_pair():
    key_pair = RSA.generate(bits=2048)
    #print(f"Public key:  (n={hex(key_pair.n)}, e={hex(key_pair.e)})")
    #print(f"Private key: (n={hex(key_pair.n)}, d={hex(key_pair.d)})")
    return key_pair

def sign_message(message, key_pair):
    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    #signature = pow(hash, key_pair.d, key_pair.n)
    return hash

def verify_signature(message, key_pair, signature):
    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, key_pair.e, key_pair.n) 
    #print("Signature valid:", hash == hashFromSignature)

def create_block(source_key_pair, target_key_pair, message, chain_file_path = "./chain.json"):
    last_block = get_last_block(chain_file_path)
    signed_message = sign_message(f"{message}{last_block['s']}{target_key_pair.n}".encode('utf-8'), source_key_pair)

    block = {
        "s" : signed_message,
        "f" : source_key_pair.n,
        "t" : target_key_pair.n,
        "m" : message,
        "p" : last_block["s"]
    }

    with open(chain_file_path, 'a') as chain_file:
        chain_file.write( 
            f"{json.dumps(block)}\n"
        )
    
def new_chain(chain_file_path,target_key_pair, origin_message):
    origin_key_pair = get_key_pair()

    genesis_prev_key = int('0'*617)

    signed_message = sign_message(f"{origin_message}{genesis_prev_key}{target_key_pair.n}".encode('utf-8'), origin_key_pair)

    block = {
        "s" : signed_message,
        "f" : origin_key_pair.n,
        "t" : target_key_pair.n,
        "m" : origin_message,
        "p" : genesis_prev_key
    }

    with open(chain_file_path, 'w') as chain_file:
        chain_file.write( 
            f"{json.dumps(block)}\n"
        )

def get_last_block(chain_file_path = "./chain.json"):
    with open(chain_file_path, 'r') as chain_file:
        for line in chain_file:
            pass
        last_line = line
        block = json.loads(last_line)
        return block

key1 = get_key_pair()
key2 = get_key_pair()

chain_file_path = "./chain.json"
origin_message = "Hi"

new_chain(chain_file_path, key1, origin_message)

i=0
while i<1000:
    create_block(key1, key2, f"block much? {i}")
    i+=1