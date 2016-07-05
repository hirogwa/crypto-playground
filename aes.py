from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter


def encrypt_cbc(key, plaintext, iv=None):
    '''
    inputs are all hex string
    '''
    iv = Random.new().read(AES.block_size) if iv is None else bytes.fromhex(iv)
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv)
    return cipher.encrypt(bytes.fromhex(plaintext))


def decrypt_cbc(key, ciphertext):
    '''
    inputs are all hex string
    '''
    ciphertext_bytes = bytes.fromhex(ciphertext)
    iv, c = ciphertext_bytes[:16], ciphertext_bytes[16:]
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv)
    d = cipher.decrypt(c)
    return d[:-d[-1]].decode()


def encrypt_ctr(key, plaintext, iv=None):
    '''
    inputs are all hex string
    '''
    iv = Random.new().read(AES.block_size) if iv is None else bytes.fromhex(iv)
    ctr = Counter.new(128)
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CTR, iv, ctr)
    return cipher.encrypt(bytes.fromhex(plaintext))


def decrypt_ctr(key, ciphertext):
    '''
    inputs are all hex string
    '''
    ciphertext_bytes = bytes.fromhex(ciphertext)
    iv, c = ciphertext_bytes[:16], ciphertext_bytes[16:]
    ctr = Counter.new(128)
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CTR, iv, ctr)
    d = cipher.decrypt(c)
    return d


def str_to_hex(s):
    return ''.join([format(ord(c), '02x') for c in s])


def hex_to_str(s, prefix=''):
    if len(s) == 0:
        return prefix + s
    return prefix + hex_to_str(s[2:], chr(int(s[:2], base=16)))


def example_cbc():
    key = 'This is a key123'.encode()
    iv = 'This is an IV456'.encode()
    obj = AES.new(key, AES.MODE_CBC, iv)
    message = "The answer is no".encode()
    ciphertext = obj.encrypt(message)
    print(ciphertext)

    obj = AES.new(key, AES.MODE_CBC, iv)
    print(obj.decrypt(ciphertext))


def example_ctr():
    key = 'This is a key123'.encode()
    iv = 'This is an IV456'.encode()
    ctr = Counter.new(128)
    obj = AES.new(key, AES.MODE_CTR, iv, ctr)
    message = "The answer is no".encode()
    ciphertext = obj.encrypt(message)
    print(ciphertext)

    ctr = Counter.new(128)
    obj = AES.new(key, AES.MODE_CTR, iv, ctr)
    print(obj.decrypt(ciphertext))


if __name__ == '__main__':
    key = '36f18357be4dbd77f050515c73fcf9f2'
    c = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
    d = decrypt_ctr(key, c)
    print(d)
