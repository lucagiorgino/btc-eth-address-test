import random, time
from Crypto.Hash import keccak
from ecdsa import SigningKey,SECP256k1
from binascii import hexlify,unhexlify
import rlp

def private_key_gen():
    return hexlify(SigningKey.generate(curve=SECP256k1).to_string())

def public_key_gen(k: str):
    k = SigningKey.from_string(unhexlify(k),curve=SECP256k1)
    K = k.get_verifying_key().to_string()
    return hexlify(K)

def account_address_gen(K: str):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(unhexlify(K))
    computed_hash = keccak_hash.hexdigest()
    #get the last 20bytes (40hex)
    return '0x' + computed_hash[24:]  

def contract_account_address_gen(address: str, tx_count: int):
    address = address.replace('0x','')
    # NOTICE that unhexlify return the same result with uppercase or lowercase
    input_for_CA = rlp.encode([unhexlify(address),tx_count])
    print("input_for_CA",input_for_CA)
    print("input_for_CA_hex",hexlify(input_for_CA))
    keccak_hash = keccak.new(digest_bits=256)
    #get the last 20bytes (40hex)
    contract_address = keccak_hash.update(input_for_CA).hexdigest()
    print("hash",contract_address)
    # it is not EIPencoded, all hex digit are lowercase
    return '0x' + contract_address[24:]

def EIP55_encode(address: str):
    checksum = ""
    address = address.replace('0x','').lower()

    keccak_Hash = keccak.new(digest_bits=256)
    #get the first 40 hex digit that correspond to 20 bytes
    mask = keccak_Hash.update(address.encode()).hexdigest()[:40]

    for i, digit in enumerate(address):
        if digit in '0123456789':
            # We can't upper-case the decimal digits
            checksum += digit
        elif digit in 'abcdef':
            # Check if the corresponding hex digit in the hash is 8 or higher
            if int(mask[i],16) > 7:
                checksum += digit.upper()
            else: 
                checksum += digit

    return '0x' + checksum

def detect_EIP55_errors(address_to_check: str):
    address_lower_case = address_to_check.lower()

    checksum = EIP55_encode(address_lower_case)

    if checksum != address_to_check:
        return True # Errors found
    else:
        return False # No errors found

def stub_get_transaction_count(address: str):
    # get number of not pending transaction for that address
    return random.randrange(100)

def address_compare(addr_1: str, addr_2: str):
    addr_1 = addr_1.replace('0x','').lower()
    addr_2 = addr_2.replace('0x','').lower()
    return addr_1 == addr_2

if __name__ == "__main__":
    # example of usage
    book_key = b'f8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315'
    k = private_key_gen()
    K = public_key_gen(k)

    address = account_address_gen(K)
    eip55_address = EIP55_encode(address)
    print(eip55_address)

    if detect_EIP55_errors(eip55_address):
        print("Error found")
    else: 
        print("EIP55 compliant")

    wrong_address = '0x001d3F1ef827552Ae1114027BD3ECF1f086bA0E9'
    if detect_EIP55_errors(wrong_address):
        print("Error found")
    else: 
        print("EIP55 compliant")
    

    print("Test example")
    print(detect_EIP55_errors("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"))
    print(detect_EIP55_errors("0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359"))
    print(detect_EIP55_errors("0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB"))
    print(detect_EIP55_errors("0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb"))

    print("All Caps")
    print(detect_EIP55_errors("0x52908400098527886E0F7030069857D2E4169EE7"))
    print(detect_EIP55_errors("0x8617E340B3D01FA5F11F306F4090FD50E238070D"))
    print("All Lower")
    print(detect_EIP55_errors("0xde709f2102306220921060314715629080e2fb77"))
    print(detect_EIP55_errors("0x27b1fdb04752bbc536007a920d24acb045561c26"))
    print("Normal")
    print(detect_EIP55_errors("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"))
    print(detect_EIP55_errors("0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359"))
    print(detect_EIP55_errors("0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB"))
    print(detect_EIP55_errors("0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb"))

    print(detect_EIP55_errors("0x001d3F1ef827552Ae1114027BD3ECF1f086bA0E9"))

    random.seed()
    nonce = stub_get_transaction_count(address)
    contract_address = contract_account_address_gen(address,nonce)  

    forum_addr = '0x6ac7ea33f8831ea9dcc53393aaa88b25a785dbf0'
    expected_contract_address = "0x343c43a37d37dff08ae8c4a11544c718abb4fcf8"
    computed_contract_address = contract_account_address_gen(forum_addr,1)
    
    if expected_contract_address != computed_contract_address:
        print("Error in contract address generation")
    
    metamask_account_address = '0x220a530fBBfE397C9F95279117fEf25e4490dA90'
    private_key = b'dc9bcd6bc45712da0dc33b33292cd4a60e5deac1de1fc69fdc98ca3c68640450'
    metamask_computed = EIP55_encode(account_address_gen(public_key_gen(private_key))) 

    print(metamask_computed)

    # https://ropsten.etherscan.io/address/0xd196e1105e638d71ea0a03f902ccd3342e7bc0c2
    # https://ropsten.etherscan.io/address/0x220a530fbbfe397c9f95279117fef25e4490da90
                      
    faucet_contract = '0xd196e1105e638D71Ea0a03f902cCd3342E7bc0c2'
    nonce = 2 # this is the tx_count
    contract_computed = contract_account_address_gen(metamask_account_address,nonce)
    
    if(address_compare(contract_computed,faucet_contract)):
        print(nonce,contract_computed)