import math
import time


# 蒙哥马利
class MontMul:
    def __init__(self, R, N):
        self.N = N
        self.R = R
        self.logR = int(math.log(R, 2))
        N_inv = MontMul.modinv(N, R)
        self.N_inv_neg = R - N_inv
        self.R2 = (R * R) % N

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = MontMul.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(a, m):
        g, x, y = MontMul.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def REDC(self, T):
        N, R, logR, N_inv_neg = self.N, self.R, self.logR, self.N_inv_neg

        m = ((T & int('1' * logR, 2)) * N_inv_neg) & int('1' * logR, 2)  # m = (T%R * N_inv_neg)%R
        t = (T + m * N) >> logR  # t = int((T+m*N)/R)
        if t >= N:
            return t - N
        else:
            return t

    def ModMul(self, a, b):
        if a >= self.N or b >= self.N:
            raise Exception('input integer must be smaller than the modulus N')

        R2 = self.R2
        aR = self.REDC(a * R2)  # convert a to Montgomery form
        bR = self.REDC(b * R2)  # convert b to Montgomery form
        T = aR * bR  # standard multiplication
        abR = self.REDC(T)  # Montgomery reduction
        return self.REDC(abR)  # covnert abR to normal ab


# 分治法
def fast_power(a, b, m):
    if b == 0:
        return 1 % m
    elif b % 2 == 0:
        half_pow = fast_power(a, b // 2, m)
        return (half_pow * half_pow) % m
    else:
        half_pow = fast_power(a, (b - 1) // 2, m)
        return (a * half_pow * half_pow) % m


# 模反复平方法
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


if __name__ == '__main__':
    N = 10086
    R = 2 ** 64  # assume here we are working on 64-bit integer multiplication
    g, x, y = MontMul.egcd(N, R)
    if R <= N or g != 1:
        raise Exception('N must be larger than R and gcd(N,R) == 1')
    T = time.perf_counter()
    inst = MontMul(R, N)

    input1, input2 = 12345, 678
    mul = inst.ModMul(input1, input2)
    print('({input1}*{input2})%{N} is {mul}'.format(input1=input1, input2=input2, N=N, mul=mul))
    print("用时：", time.perf_counter() - T, "秒")

    # ##分治法统计
    # T = time.perf_counter()
    # result = fast_power(8899, 13579, 10086)
    # print(result)
    # print("用时：", time.perf_counter() - T, "秒")

    #
    # T = time.perf_counter()
    # result = fast_modular_exponentiation(8899, 13579, 10086)
    # print(result)
    # print("用时：", time.perf_counter() - T, "秒")
