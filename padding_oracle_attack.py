import urllib.parse
import urllib.request
import urllib.error
import common

PO_URL = 'http://crypto-class.appspot.com/po?er='
C_KNOWN = 'f20bdba6ff29eed7b046d1df9fb70000' + \
          '58b1ffb4210a580f748b4ac714c001bd' + \
          '4a61044426fb515dad3f21f18aa577c0' + \
          'bdf302936266926ff37dbf7035d5eeb4'

BLOCK_LENGTH_BYTES = 16
BLOCK_LENGTH = BLOCK_LENGTH_BYTES * 2


class PaddingOracle(object):
    def query(self, q):
        target = PO_URL + urllib.parse.quote(q)
        req = urllib.request.Request(target)
        try:
            resp = urllib.request.urlopen(req)
            return resp.status
        except urllib.error.HTTPError as e:
            return e.code


def good_pad(c):
    po = PaddingOracle()
    status = po.query(c)
    return status if status in (404, 200) else False


def solve_byte(pre_blocks, block, post_block, solved=''):
    if len(solved) == BLOCK_LENGTH:
        return ''
    assert len(solved) % 2 == 0

    pad_bytes = len(solved) // 2 + 1
    for g in range(0, 256):
        guess = format(g, '02x')
        border_index = -len(solved) - 2
        test_block = block[:border_index] + \
            common.xor_hexstr(block[border_index:],
                              guess + solved,
                              format(pad_bytes, '02x') * pad_bytes)
        if test_block == block:
            continue
        test_cipher = ''.join(pre_blocks) + test_block + post_block
        status = good_pad(test_cipher)
        if status:
            print('{} was a good guess! ({})'.format(guess, status))
            return guess


def solve_block(c_blocks, i, solved=''):
    print('Solving plain text block {} with cipher block {}: {}'
          .format(i + 1, i, c_blocks[i]))
    print('Solved: {}'.format('-' * (BLOCK_LENGTH - len(solved)) + solved))
    while len(solved) < BLOCK_LENGTH:
        solved = solve_byte(
            c_blocks[:i], c_blocks[i], c_blocks[i + 1], solved) + solved
        print('Solved: {}'.format('-' * (BLOCK_LENGTH - len(solved)) + solved))
    return solved


def solve(c):
    c_blocks = list(cipher_to_blocks(c))

    print('Solving last byte for padding.')
    last_byte = solve_byte(c_blocks[:2], c_blocks[2], c_blocks[3])
    solved = last_byte * int(last_byte, base=16)  # padding bytes

    result = solve_block(c_blocks, 2, solved)
    result = solve_block(c_blocks, 1) + result
    result = solve_block(c_blocks, 0) + result
    print(result)
    print(common.hex_to_str(result))


def cipher_to_blocks(c):
    for i in range(0, len(c), BLOCK_LENGTH):
        yield c[i:i + BLOCK_LENGTH]


if __name__ == "__main__":
    solve(C_KNOWN)
