from random import randint


def miller_rabin(p):
    if p == 1: return False
    if p == 2: return True
    if p % 2 == 0: return False
    m, k, = p - 1, 0
    while m % 2 == 0:
        m, k = m // 2, k + 1
    a = randint(2, p - 1)
    x = pow(a, m, p)
    if x == 1 or x == p - 1: return True
    while k > 1:
        x = pow(x, 2, p)
        if x == 1: return False
        if x == p - 1: return True
        k = k - 1
    return False


def is_prime(p, r=40):
    for i in range(r):
        if miller_rabin(p) == False:
            return False
    return True


def gcd(a, b):
    a, b = adjust(a, b)
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def adjust(a, b):
    if a >= b:
        return a, b
    else:
        return b, a


def generate_PQ(size):
    '''
    size：产生的素数位数
    '''
    res = [0, 0]
    for j in range(2):
        index = size
        num = 0
        for i in range(index):
            num = num * 2 + randint(0, 1)
        while is_prime(num) == False:
            num = num + 1
        res[j] = num
    if res[0] == res[1]:
        raise ValueError('大素数产生失败，请调整素数位数重新生成')
    return res[0], res[1]


def caculate_n(P, Q):
    return P * Q


def Euler(P, Q):
    return (P - 1) * (Q - 1)


def find_e(Euler_n):
    for e in range(2, Euler_n):
        if gcd(e, Euler_n) == 1:
            return e
    raise ValueError("不能找到合适条件的e，请调整素数位数")


def get_d(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def fast_modular_exponentiation(base, exponent, modulus):
    result = 1

    base = base % modulus  # 将底数取模以避免溢出

    while exponent > 0:
        # 如果指数为奇数，则乘以当前底数
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # 将指数除以2，底数平方
        exponent //= 2
        base = (base * base) % modulus

    return result


def RSA_encode(message, e, n):
    encode_list = []
    for i in range(len(message)):
        encode_list.append(fast_modular_exponentiation(ord(message[i]), e, n))
    return encode_list


def RSA_decode(encode_list, d, n):
    message = ''
    for v in encode_list:
        message += chr(fast_modular_exponentiation(v, d, n))
    return message


def ELGamal_encode(message, p, alpha, y):
    encode_list = []
    k = randint(2, p - 2)
    U = fast_modular_exponentiation(y, k, p)
    C1 = fast_modular_exponentiation(alpha, k, p)
    for i in range(len(message)):
        M = ord(message[i])
        C2 = U * M % p
        encode_list.append((C1, C2))
    return encode_list


def ELGamal_decode(encode_list, d, p):
    res = ''
    for (c1, c2) in (encode_list):
        V = fast_modular_exponentiation(c1, d, p)
        V2 = get_d(V, p)  # 求V在模p下的逆
        M = c2 * V2 % p
        res += chr(M)
    return res


def add(p1, p2, a, p):
    # 其中一个点为0元素的情况
    if p1 == 0:
        return p2
    if p2 == 0:
        return p1

    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    # 两个点互逆
    if (x1 == x2) & (y1 + y2 == 0):
        return 0
    # 两个点相同
    elif (x1 == x2) & (y1 == y2):
        l = ((3 * x1 * x1 + a) * get_d(2 * y1, p)) % p
        x3 = (l * l - 2 * x1) % p
        y3 = (l * (x1 - x3) - y1) % p
        return (x3, y3)
    # 其他情况
    else:
        l = (((y2 - y1) % p) * get_d((x2 - x1) % p, p)) % p
        x3 = (l * l - x1 - x2) % p
        y3 = (l * (x1 - x3) - y1) % p
        return (x3, y3)


def mul(point, x, a, p):
    if x == 1:
        return point
    mod_point = point
    r = 0

    bit_length = x.bit_length()
    for _ in range(bit_length):
        if x & 1:
            r = add(r, mod_point, a, p)

        mod_point = add(mod_point, mod_point, a, p)
        x >>= 1

    return r


def Gkey(d, G, a, p):
    return mul(G, d, a, p)


# M是一个数值
def ECC_encode(M, n, G, Q, a, p):
    k = randint(1, n - 1)
    X2 = (0, 0)
    while (X2[0] == 0):
        X1 = mul(G, k, a, p)
        X2 = mul(Q, k, a, p)
    C = M * X2[0] % n
    return (X1, C)


def ECC_decode(X1, C, n, a, p, d):
    X2 = mul(X1, d, a, p)
    M = C * get_d(X2[0], n) % n
    return M


def ECC_en_message(message, n, G, Q, a, p):
    encode_list = []
    for i in range(len(message)):
        t = ord(message[i])
        encode_list.append(ECC_encode(t, n, G, Q, a, p))
    return encode_list


def ECC_de_message(encode_list, n, a, p, d):
    r = ''
    for (X1, C) in encode_list:
        M = ECC_decode(X1, C, n, a, p, d)
        r += chr(M)
    return r
