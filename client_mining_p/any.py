import requests
import hashlib
import json
import time

def valid_proof(block_string, proof, diff):
    #block_string should = last proof after it's been run through the hash function
    #:return: True if the resulting hash is a valid proof, False otherwise
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:diff] == "0" * diff #6 is the difficulty se

def proof_of_work(last_proof, diff):
    #block_string = json.dumps(last_proof, sort_keys=True)
    print(f"finding that next proof for you, sire... ")
    proof = 100000000000000

    while valid_proof(last_proof, proof, diff) is False:
        proof -= 1
    return proof

coins = 1
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c'
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}
while True: 
    r = requests.get(url="https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers=headers)
    last_proof = r.json()
    
    cooldown = last_proof['cooldown']
    diff = last_proof["difficulty"]
    proof = last_proof["proof"]

    print(f"response: {last_proof}")
    print(f"last proof: {proof}")
    print(f"current difficulty: {diff}")
    print(f"cooldown: {cooldown}")

    #pause for cooldown
    time.sleep(cooldown)

    new_proof = proof_of_work(proof, diff)
    to_post = {"proof": new_proof}

    r = requests.post(url="https://lambda-treasure-hunt.herokuapp.com/api/bc/mine", json=to_post, headers=headers)
    response = r.json()

    print(f"post response: {response}")
    
    if r.status_code != 200:
        print(f"{r.status_code}")
        print(f"{response}")
    else:
        if response["messages"] == "New Block Forged":
            coins += 1
            print("Total Coins: {coins}")
    time.sleep(response["cooldown"])
