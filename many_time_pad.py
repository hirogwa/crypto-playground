import re

c_target = \
    '32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904'

c_list = [
    '315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e',
    '234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f',
    '32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb',
    '32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa',
    '3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070',
    '32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4',
    '32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce',
    '315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3',
    '271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027',
    '466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83',
    c_target
]


def xor_hexstr(a, b, prefix=''):
    if len(a) < len(b):
        return xor_hexstr(b, a, prefix)
    return ''.join(
        [format(int(x, base=16) ^ int(y, base=16), '02x') for (x, y) in zip(
            hex_str_to_list(a[:len(b)]), hex_str_to_list(b))])


def hex_to_str(s, prefix=''):
    if len(s) == 0:
        return prefix + s
    return prefix + hex_to_str(s[2:], chr(int(s[:2], base=16)))


def str_to_hex(s):
    return ''.join([format(ord(c), '02x') for c in s])


def crib_drag(hex_str, phrase, starting_position=0, highlight_regex=None):
    target_hex = str_to_hex(phrase)
    position = starting_position
    print('"{}"({}) on {}{}'.format(
        phrase, target_hex, hex_str,
        ', highlighting ' + highlight_regex if highlight_regex else ''))
    while position + len(target_hex) <= len(hex_str):
        hex_str_sub = hex_str[position: position + len(target_hex)]
        xored_str = hex_to_str(xor_hexstr(hex_str_sub, target_hex))
        hl_result = highlight_regex and re.match(
            highlight_regex, xored_str)
        print('{}, {}, {} {}'.format(
            format(position, '03d'), hex_str_sub, xored_str,
            '<= !!' if hl_result else ''))
        position += 2


def partial_key(ct_hex, position, partial_message):
    """ returns key (hex string) that decrypts the portion of the cipher text
    starting at the specified position
    """
    assert position % 2 == 0
    partial_message_hex = str_to_hex(partial_message)
    ct_hex_partial = ct_hex[position:position + len(partial_message_hex)]
    return PartialKey(position,
                      xor_hexstr(ct_hex_partial, partial_message_hex))


def hex_str_to_list(hex_str):
    return [''.join(pair) for pair in zip(hex_str[::2], hex_str[1::2])]


def merge_partial_keys(partial_keys, key_length):
    result = []
    for i, p in enumerate(zip(*[hex_str_to_list(k.fullkey(key_length))
                                for k in partial_keys])):
        candidates = {x for x in p if x != '00'}
        if len(candidates) == 0:
            result.append('00')
        elif len(candidates) == 1:
            result.append(candidates.pop())
        else:
            raise ValueError('multiple key candidates {} at position {}'
                             .format(candidates, i * 2))
    return ''.join(result)


def test_partial_key(key):
    print('Testing partial key {} at position {}'.format(
        key.hex_string, key.position))
    for i, c in enumerate(c_list):
        message = key.decrypt(c)
        if len(message) > 0:
            print('{}: {}(index {} to {})'.format(
                i, message, key.position,
                key.position + len(key.hex_string) - 1))
        else:
            print('{}:'.format(i))


class PartialKey:
    '''Key for only one chunk'''
    def __init__(self, position, hex_string):
        assert position % 2 == 0
        self.position = position
        self.hex_string = hex_string

    def __repr__(self):
        return self.fullkey()

    def __str__(self):
        return self.fullkey()

    def fullkey(self, length=None):
        length = length or self.position + len(self.hex_string)
        pre = '0' * self.position
        post = '0' * (length - self.position - len(self.hex_string))
        return pre + self.hex_string + post

    def decrypt(self, hex_string, output='str'):
        result = xor_hexstr(
            hex_string[self.position:self.position + len(self.hex_string)],
            self.hex_string)
        if output == 'str':
            return hex_to_str(result)
        else:
            return result


if __name__ == '__main__':
    print('Cipher texts:')
    key_length = 0
    for i, c in enumerate(c_list):
        key_length = max(key_length, len(c))
        print('{}: {}, {}'.format(i, len(c), len(c) // 2))
    print('Key length:{}'.format(key_length))

    crib_drag(xor_hexstr(c_list[6], c_list[8]), ' the ',
              starting_position=290,
              highlight_regex='^[a-zA-Z\s]+$')

    # key = partial_key(c_list[5], 280, 'your ')
    # test_partial_key(key)

    promising_partial_keys = [
        partial_key(c_list[1], 22, ' probably '),
        partial_key(c_list[7], 20, ' the point '),
        partial_key(c_list[4], 18, ' want to buy '),
        partial_key(c_list[5], 18, ' two types of '),
        partial_key(c_list[0], 18, 'ctor the number '),
        partial_key(c_list[5], 18, ' two types of crypt'),
        partial_key(c_list[4], 18, ' want to buy a set of '),
        partial_key(c_list[8], 2, ' (private-key)  encryption scheme'),
        partial_key(c_list[5], 0, 'There are two types of cryptography '),

        partial_key(c_list[3], 68, 'encryption '),
        partial_key(c_list[7], 68, 'p is unhappy '),
        partial_key(c_list[3], 90, 'algorithm '),
        partial_key(c_list[7], 104, 'wrong '),
        partial_key(c_list[9], 104, ' as the '),
        partial_key(c_list[3], 104, 'hm looks '),
        partial_key(c_list[8], 104, 'ms, namely'),
        partial_key(c_list[0], 104, 'We can also '),

        # crib_drag(xor_hexstr(c_list[0], c_list[3]), ' the ', '^[a-zA-Z\s]+$')
        partial_key(c_list[3], 144, 'ciphertext '),
        partial_key(c_list[0], 140, ' the number 1'),
        partial_key(c_list[6], 138, ' use brute force '),
        partial_key(c_list[8], 128, ' procedure for generating '),
        partial_key(c_list[1], 114, ' corner stone of crypto - Annonymous '),

        # crib_drag(xor_hexstr(c_list[0], c_list[6]), ' the ', starting_position=188,
        #          highlight_regex='^[a-zA-Z\s]+$')
        partial_key(c_list[0], 252, 'Robert'),
        partial_key(c_list[3], 254, 'Philip '),
        partial_key(c_list[6], 254, 'the Government '),
        partial_key(c_list[8], 280, 'for ')
    ]

    key_incomplete = merge_partial_keys(promising_partial_keys, key_length)
    print(key_incomplete)
    print('First position unresolved:', key_incomplete.find('00'))
    print(hex_to_str(xor_hexstr(c_target, key_incomplete)))
