import common

block_length = 32  # 16 bytes
c = ['20814804c1767293b99f1d9cab3bc3e7', 'ac1e37bfb15599e5f40eef805488281d']
pt = 'Pay Bob 100$'
m = common.str_to_hex(pt)


def execute():
    # show where '100' is at
    print(pt[8:11])
    print(m[16:22])

    print(c[0][16:18])

    # xor with intended change
    tampered_iv_partial = \
        common.xor_hexstr(
            common.str_to_hex('100'),
            c[0][16:22],
            common.str_to_hex('500'))
    print(tampered_iv_partial)

    # integrated into original iv
    tampered_iv = c[0][:16] + tampered_iv_partial + c[0][22:]
    tampered_c = [tampered_iv, c[1]]

    # compare
    print('original: ' + ' '.join(c))
    print('tampered: ' + ' '.join(tampered_c))

    return tampered_c

if __name__ == '__main__':
    execute()
