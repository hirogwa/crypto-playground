import numbthy

B = 2 ** 20


def get_discrete_log(p, g, h):
    lhs_values = {}
    for x1 in range(0, B + 1):
        if x1 % 20000 == 0:
            print('(LHS) storing x1={}'.format(x1))
        lhs = (numbthy.invmod(numbthy.powmod(g, x1, p), p) * h) % p
        if lhs not in lhs_values:
            lhs_values[lhs] = x1

    x0_found, x1_found, x_found = None, None, None
    for x0 in range(0, B + 1):
        if x0 % 10000 == 0:
            print('(RHS) checking x0={}'.format(x0))
        rhs = numbthy.powmod(g, B * x0, p)
        if rhs in lhs_values:
            x0_found, x1_found = x0, lhs_values[rhs]
            x_found = (x0_found * B + x1_found) % p
            print('Found. x0={}, x1={}, x={}'.format(
                x0_found, x1_found, x_found))
            break

    assert x_found, 'Failed to find discrete log. May not exist?'
    return x_found


def execute():
    p = int(
        '134078079299425970995740249982058461274793658205923933\
        77723561443721764030073546976801874298166903427690031\
        858186486050853753882811946569946433649006084171'
        .replace(' ', ''))
    g = int(
        '11717829880366207009516117596335367088558084999998952205\
        59997945906392949973658374667057217647146031292859482967\
        5428279466566527115212748467589894601965568'
        .replace(' ', ''))
    h = int(
        '323947510405045044356526437872806578864909752095244\
        952783479245297198197614329255807385693795855318053\
        2878928001494706097394108577585732452307673444020333'
        .replace(' ', ''))

    print(get_discrete_log(p, g, h))

if __name__ == '__main__':
    execute()
