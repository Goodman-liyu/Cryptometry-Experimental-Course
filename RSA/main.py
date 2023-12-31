from tool import *
from prime import *
import time

split = "---------------------------------------------------------------------------"


def generate_PQ(size, way='mr'):
    '''
    size：产生的素数位数 , way: 大素数生成的指定算法，默认为Miller-Rabin
    '''
    if way == 'origin':
        res = origin_traversal_generation_algorithm(size)
    elif way == 'mj':
        res = generate_prime_mj(size)
    elif way == 'mr':
        res = generate_two_primes_using_miller_rabin(size)
    elif way == 'er':
        res = generate_prime_eratosthenes(size)
    elif way == 'zl':
        res = generate_prime_zl(size)
    elif way == 'zl-improve':
        res = generate_prime_zl_improve(size)
    else:
        raise ValueError('请重新选择的生成算法素数生成')
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


def encode(Mpath, e, n):
    unicode_str = readfile(Mpath)
    print("文件内容编码后的结果：", unicode_str)

    num_str = str(n)
    num_digits = len(num_str)  # n的位数

    M_str, M_num = split_string(unicode_str, 6)
    M_list = [int(strM, 16) for strM in M_str]
    print("明文:", M_list)

    encode_list = []

    for k in range(M_num):  # 对于后面的先加密，再将密文异或到下一个明文上
        C = fast_modular_exponentiation(M_list[k], e, n)
        encode_list.append(C)
        if k < M_num - 1:
            M_list[k + 1] ^= encode_list[k]
    print("密文:", encode_list)

    # with open(Cpath, 'w') as file:
    #     for item in encode_list:
    #         file.write(str(item)+'\n')

    encode_str = ''
    for item in encode_list:
        encode_str += str(item) + '\n'
    return encode_str


def decode(Cpath, d, n):
    with open(Cpath, 'r') as file:
        encode_list = file.read().splitlines()

    encode_list = [int(encode) for encode in encode_list]
    num = len(encode_list)
    M_list = [0] * num

    for i in range(num - 1, -1, -1):  # 从后到前，先解密，再异或前一个密文
        M_list[i] = fast_modular_exponentiation(encode_list[i], d, n)
        if i != 0:
            M_list[i] = M_list[i] ^ encode_list[i - 1]
    return get_content(M_list)


if __name__ == '__main__':
    # print(1)
    T = time.perf_counter()

    P, Q = generate_PQ(512, 'origin')
    print("用时：", time.perf_counter() - T, "秒")

    # n=caculate_n(P,Q)
    # Euler_n=Euler(P,Q)
    # e=find_e(Euler_n)
    # d=get_d(e,Euler_n)
    # t=encode('example.txt',e,n)
    # decode('C.txt',d,n)
