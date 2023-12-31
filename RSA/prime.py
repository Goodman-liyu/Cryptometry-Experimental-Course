import random
from tool import *


def generate_prime_using_miller_rabin(size):
    while True:
        num_bits = random.getrandbits(size)
        if num_bits.bit_length() == size:
            if is_prime(num_bits):
                return num_bits


def generate_two_primes_using_miller_rabin(size):
    prime_list = []
    while len(prime_list) < 2:
        prime_candidate = generate_prime_using_miller_rabin(size)
        if prime_candidate not in prime_list:
            prime_list.append(prime_candidate)
    return prime_list


'''
-----------------------------------------------------------------------上面是miller_rabin素数生成
'''


def origin_traversal_generation_algorithm(size):
    res = [0, 0]
    for j in range(2):
        index = size
        num = 0
        for i in range(index):
            num = num * 2 + randint(0, 1)
        while is_prime(num) == False:
            num = num + 1
        res[j] = num
    return res


'''
-----------------------------------------------------------------------上面是原始遍历算法的素数生成
'''


def generate_prime_zl(size):
    p_size = size // 2 + 1  # 两个素数总位数的一半
    p = random.getrandbits(p_size) | (1 << (p_size - 1)) | 1  # 生成奇数p

    while True:
        p += 2
        if is_prime(p):
            q = p + 2
            if is_prime(q):
                return [p, q]


'''
-----------------------------------------------------------------------上面是增量素数生成算法的素数生成
'''


def generate_prime_zl_improve(size):
    p_size = size // 2 + 1  # 两个素数总位数的一半
    t = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29

    p = random.getrandbits(p_size) | (1 << (p_size - 1)) | 1  # 生成奇数p

    while True:
        p += t
        if is_prime(p):
            q = p + t
            if is_prime(q):
                return [p, q]


'''
-----------------------------------------------------------------------上面是增量素数生成算法的素数生成
'''


def generate_prime_eratosthenes(n):
    # 初始所有的都为True
    IsPrime = [True] * (n + 1)
    # 100**0.5 = 10
    for i in range(2, int(n ** 0.5) + 1):
        # i在2-10范围内如果是素数
        if IsPrime[i]:
            # 从i平方开始往后去掉，即置标志位为false
            for j in range(i * i, n + 1, i):
                IsPrime[j] = False
    # 输出所有标志位为True的就是素数
    return [x for x in range(2, n + 1) if IsPrime[x]]


'''
-----------------------------------------------------------------------上面是埃拉托斯特尼筛法 (Sieve of Eratosthenes) 算法的素数生成
'''


def generate_prime_mj(bits):
    n = bits // 10
    N = random.randint(10 ** (n - 1), 10 ** n - 1)
    f = N ** (10 ** n - 1) - N
    if is_prime(f):
        return N
    else:
        return generate_prime_mj(bits)


'''
-----------------------------------------------------------------------上面是埃拉托斯特尼筛法 (Sieve of Eratosthenes) 算法的素数生成
'''

if __name__ == '__main__':
    size = 128  # 256-bit primes, adjust as needed
    [p, q] = generate_prime_mj(12)
    print(p)
    print(q)
