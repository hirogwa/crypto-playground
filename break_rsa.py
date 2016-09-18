import gmpy2
import common
from gmpy2 import mpz


def factor_1(N):
    '''
    premise: A - sqrt(N) < 1
    '''
    A, remainder = gmpy2.isqrt_rem(N)
    if remainder != mpz(0):
        A += 1

    factors = verify_A(A, N)
    if factors:
        return factors
    else:
        print('Failed')
        return False


def factor_2(N):
    '''
    premise: A - sqrt(N) < 2**20
    '''
    root, remainder = gmpy2.isqrt_rem(N)
    if remainder != mpz(0):
        root += 1

    for i in range(2**20):
        if i % 5000 == 0:
            # print('Attempts made to find A: {}'.format(i))
            pass
        A = root + i
        factors = verify_A(A, N)
        if factors:
            return factors

    assert False, 'Failed'


def verify_A(A, N):
    '''
    serves factor_1 and factor_2
    '''
    x = gmpy2.isqrt(A**2 - N)
    p, q = A - x, A + x

    if p*q == N:
        return p, q
    else:
        return False


def factor_3(N):
    '''
    premise: sqrt(6N) is close to (3p + 2q)/2

    M = (3p + 2q)/2 is a midpoint of (3p, 2q).
    Note that since both p and q are odd, A = M + 0.5 is an integer.

    There exits an integer x such that
    min(3p, 2q) = A - x - 1
    max(3p, 2q) = A + x

    It follows;
    N = pq = (A-x-1)(A+x)/6 = (A^2 - x^2 - A - x)/6
    => 6N = A^2 - x^2 - A - x
    => x^2 + x + (-A^2 + A + 6N) = 0

    We can obtain once from A and N via quadratic formula.
    '''
    A, remainder = gmpy2.isqrt_rem(6*N)
    if remainder != mpz(0):
        A += 1

    factors = verify_A3(A, N)
    if factors:
        return factors
    else:
        assert False, 'Failed'


def verify_A3(A, N):
    '''
    serves factor_3
    '''
    c = -A**2 + A + 6*N
    b = mpz(1)
    a = mpz(1)

    if (b**2 - 4*a*c) < 0:
        return False

    x_candidates = (
        gmpy2.div((-b + gmpy2.isqrt(b**2 - 4*a*c)), 2*a),
        gmpy2.div((-b - gmpy2.isqrt(b**2 - 4*a*c)), 2*a))

    for x in x_candidates:
        if x < 0:
            continue

        # 2q < 3p
        p = gmpy2.div((A + x), 3)
        q = gmpy2.div((A - x - 1), 2)
        if p*q == N:
            return p, q

        # 3p < 2q
        p = gmpy2.div((A - x - 1), 3)
        q = gmpy2.div((A + x), 2)
        if p*q == N:
            return p, q
    return False


def decrypt_challenge(N, e, c):
    '''
    premise: N is factored by factor_1
    '''
    p, q = factor_1(N)
    phi_n = (p - 1) * (q - 1)
    d = gmpy2.invert(e, phi_n)
    print('Secret key d found:\n{}'.format(d))

    plaintext_int = gmpy2.powmod(c, d, N)
    plaintext_hex = format(plaintext_int, '02x')

    delim_index = plaintext_hex.find('00') + 2
    return common.hex_to_str(plaintext_hex[delim_index:])


if __name__ == '__main__':
    print('=== Factor N1 ===')
    N1 = int(
        '17976931348623159077293051907890247336179769789423065727343008115 \
        77326758055056206869853794492129829595855013875371640157101398586 \
        47833778606925583497541085196591615128057575940752635007475935288 \
        71082364994994077189561705436114947486504671101510156394068052754 \
        0071584560878577663743040086340742855278549092581'.replace(' ', ''))

    p, q = factor_1(N1)
    print('p:\n{}'.format(p))

    print('=== Factor N2 ===')
    N2 = int(
        '6484558428080716696628242653467722787263437207069762630604390703787 \
        9730861808111646271401527606141756919558732184025452065542490671989 \
        2428844841839353281972988531310511738648965962582821502504990264452 \
        1008852816733037111422964210278402893076574586452336833570778346897 \
        15838646088239640236866252211790085787877'.replace(' ', ''))
    p, q = factor_2(N2)
    print('p:\n{}'.format(p))

    print('=== Factor N3 ===')
    N3 = int(
        '72006226374735042527956443552558373833808445147399984182665305798191 \
        63556901883377904234086641876639384851752649940178970835240791356868 \
        77441155132015188279331812309091996246361896836573643119174094961348 \
        52463970788523879939683923036467667022162701835329944324119217381272 \
        9276147530748597302192751375739387929'.replace(' ', ''))
    p, q = factor_3(N3)
    print('smaller of the two:\n{}'.format(min(p, q)))

    print('=== Decrypt RSA with N1 ===')
    e = 65537
    c = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540
    m = decrypt_challenge(N1, e, c)
    print('message:\n{}'.format(m))
