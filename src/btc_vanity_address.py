
import hashlib
from ecdsa import SigningKey,SECP256k1
from binascii import unhexlify,hexlify # from bytes to hex, and viceversa
import time 
from base58 import b58encode

# questa funzione ci restituirà l'address per una transazione p2pkh
def p2pkh_address(public_key: str) -> bytes:

    public_key_bytes = unhexlify(public_key)

    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)

    hash = sha256.digest()

    # funzione hash da openssl
    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash)

    hash2 = ripemd160.hexdigest()
    # print('L\'address che compare nel locking script è ', hash2)

    hash3 = '00' + hash2
    hash3_bytes = unhexlify(hash3)

    sha256.update(hash3_bytes)
    hash4 = sha256.digest()
    
    sha256.update(hash4)
    hash5 = sha256.hexdigest()

    checksum = hash5[:8]

    hash_final = hash3 + checksum
    hash_final_bytes = unhexlify(hash_final)

    return b58encode(hash_final_bytes)

def bytes_from_int(a: int) -> bytes:
    return a.to_bytes(32, "big")


def vanity_address_generator(vanity_string_expected: str) :

    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    # n = 10 # test n, 
    p2pkh_pre = '1' # '3' per p2sh
    vanity_string_expected = p2pkh_pre + vanity_string_expected
    vanity_string_expected_len = len(vanity_string_expected)
    private_key_counter = 2

    while private_key_counter <= n:
     
        start = time.time()
         # argument of this function should be bytes, buffer or ASCII string, not 'int'
        private_key = SigningKey.from_string(bytes_from_int(private_key_counter), curve=SECP256k1)
        public_key_str = hexlify(private_key.get_verifying_key().to_string("compressed")).decode()    
        end = time.time()
        print('Tempo richiesto per calcolare la chiave publica è di', end-start, 'secondi')
        
        address = p2pkh_address(public_key_str)
        vanity_string = address[:vanity_string_expected_len]
        vanity_string = vanity_string.decode('utf-8')
        
        if vanity_string_expected == vanity_string:
            return address
        
        private_key_counter += 1


vanity_string = 'kids'
start = time.time()
vanity_address = vanity_address_generator(vanity_string)
end = time.time()

print('Il vanity address che è stato trovato è', vanity_address, "in", end-start, "secondi")

'''
key = 2
key = bytes_from_int(key)
print(key)
# argument should be bytes, buffer or ASCII string, not 'int'
private_key = SigningKey.from_string(key, curve=SECP256k1)
print(hexlify(private_key.to_string()))

public = hexlify(private_key.get_verifying_key().to_string("compressed")).decode()
print(p2pkh_address(public))
'''

# lettera k, pc A.G., algoritmo 1, circa 96 secondi
# lettera k, pc mio, algoritmo 1, circa 32 secondi
# lettera k, ecdsa library, algoritmo 2, 0.53 secondi

# antonopulus vanity address 'love' 1 minuto, funzione python per generare curve ellittiche 
# secondi per generare un chiave pubblica,
# 0.17  algoritmo 1, A.G.
# 0.05  algoritmo 1, mio pc
# 0.0010104179382324219  algoritmo 2
# 58**4*0.0012 = 13579.8 secondi, meno di 4 ore
# 0.0002 algortimo 2, macbook pro 2019 i5, 2264 secondi => 37 minuti