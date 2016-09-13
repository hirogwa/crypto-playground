def str_to_hex(s):
    return ''.join([format(ord(c), '02x') for c in s])


def hex_to_str(s, prefix=''):
    result = ''
    for i in range(0, len(s), 2):
        result = result + chr(int(s[i:i + 2], base=16))
    return result


def xor_hexstr(*args):
    if len(args) < 1:
        return None

    l = len(args[0])
    assert l > 0
    assert l % 2 == 0
    for x in args:
        assert l == len(x)

    result = ''
    for i in range(0, l, 2):
        xored_int = 0
        for byte_num in [int(x[i: i+2], base=16) for x in args]:
            xored_int = xored_int ^ byte_num
        result = result + format(xored_int, '02x')

    return result


def hex_str_to_list(hex_str):
    return [''.join(pair) for pair in zip(hex_str[::2], hex_str[1::2])]
