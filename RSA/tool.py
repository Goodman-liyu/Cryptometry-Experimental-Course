from random import randint
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk


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


def split_string(input_str, n):
    string_groups = [input_str[i:i + n] for i in range(0, len(input_str), n)]
    num_groups = len(string_groups)

    return string_groups, num_groups


def readfile(Mpath):
    with open(Mpath, 'r', encoding='utf-8') as file:
        content_str = file.read()
    unicode_unfill = [hex(ord(char)) for char in content_str]  # 原始的uncode编码
    unicode_filled = [format(int(hex_num[2:], 16), '06x') for hex_num in unicode_unfill]  # 补为6位且去掉了0x的uncode编码
    # unicode_filled_remove_0x = ["0x{:x}".format(int(hex_str.lstrip('0'), 16)) for hex_str in unicode_filled]  #还原补位与去0x操作，得原始的unicode编码
    # decimal_values = [int(hex_str, 16) for hex_str in original_a]  #原始unicode编码转为对应的10进制
    result_string = ''.join(unicode_filled)
    return result_string


def get_content(M_list):
    M_list = [str(hex(x)) for x in M_list]
    M_list = [hex_str[2:].rjust(6, '0') for hex_str in M_list]
    unicode_characters = [chr(int(x, 16)) for x in M_list]
    decode_str = ''
    for item in unicode_characters:
        decode_str += str(item)
    return decode_str

    # with open(origin_file_path, 'w', encoding='utf-8') as file:
    #     # 将列表中的每个元素写入文件
    #     for item in unicode_characters:
    #         file.write(item)
