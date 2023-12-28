def initial_permutation(data):
    permutation_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    return permute(data, permutation_table)

def permute(data, table):
    return ''.join(data[i - 1] for i in table)

def generate_subkeys(key):
    # 生成16个子密钥
    key_permutation_table = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    key_shift_table = [
        1, 1, 2, 2, 2, 2, 2, 2,
        1, 2, 2, 2, 2, 2, 2, 1
    ]

    key = permute(key, key_permutation_table)
    left, right = key[:28], key[28:]  #初始的C0，D0

    subkeys = []
    for shift in key_shift_table:
        left = left[shift:] + left[:shift]
        right = right[shift:] + right[:shift]
        subkey = permute(left + right, [
            14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32
        ])
        subkeys.append(subkey)

    return subkeys

def feistel_network(data, subkey,k):
    # Feistel网络
    left, right = data[:32], data[32:]
    expanded_right = permute(right, [   #选择运算E
        32, 1, 2, 3, 4, 5, 4, 5,
        6, 7, 8, 9, 8, 9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27,
        28, 29, 28, 29, 30, 31, 32, 1
    ])
    xor_result = bin(int(expanded_right, 2) ^ int(subkey, 2))[2:].zfill(48)  #模2相加（等同于异或）
    substitution_result = substitution(xor_result)   #S盒置换，输入一个48位，返回32位
    permuted_result = permute(substitution_result, [   #置换运算P
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ])
    new_right = bin(int(left, 2) ^ int(permuted_result, 2))[2:].zfill(32)
    new_lift=right
    if k==16:
        return new_right + new_lift
    return new_lift + new_right

def substitution(data):
    # S盒替换
    s_boxes = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    result = ''
    for i in range(0, len(data), 6):
        block = data[i:i + 6]
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        result += bin(s_boxes[i // 6][row][col])[2:].zfill(4)

    return result


def substitution2(data):
    # S盒替换
    s_boxes = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
    ]
    result = ''
    block = data
    row = int(block[0] + block[5], 2)
    col = int(block[1:5], 2)
    result += bin(s_boxes[0][row][col])[2:].zfill(4)

    return result

def final_permutation(data):
    # 最终置换
    permutation_table = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]
    return permute(data, permutation_table)


def hex_to_binary(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(4)

def des_encrypt(data, key):
    # DES加密
    binary_data = ''.join(hex_to_binary(hex_digit) for hex_digit in data)
    binary_key = ''.join(hex_to_binary(hex_digit) for hex_digit in key)
    data = initial_permutation(binary_data)  #初始变换IP
    subkeys = generate_subkeys(binary_key)  #生成子密钥
    k=0
    for subkey in subkeys:
        k+=1
        data = feistel_network(data, subkey,k)
    encrypted_data = final_permutation(data)  #逆初始变换IP-
    encrypted_data= hex(int(encrypted_data, 2))[2:].zfill(16)
    return encrypted_data

def des_decrypt(data, key):
    # DES加密
    binary_data = ''.join(hex_to_binary(hex_digit) for hex_digit in data)
    binary_key = ''.join(hex_to_binary(hex_digit) for hex_digit in key)
    data = initial_permutation(binary_data)  #初始变换IP
    subkeys =  generate_subkeys(binary_key)  #生成子密钥
    subkeys.reverse()  #颠倒子密钥的顺序
    k = 0
    for subkey in subkeys:
        k += 1
        data = feistel_network(data, subkey,k)
    decrypted_data = final_permutation(data)  #逆初始变换IP-
    decrypted_data= hex(int(decrypted_data, 2))[2:].zfill(16)
    return decrypted_data

plaintext = ["3031323334353637","1234567890abcdef","a1a2a3a4b1b2b3b4","fdf1f2fafef5f900"]  # 64位十六进制明文
key = ["3132333435363738","31abc134aaa63738","ffffffffffffffff","fdf1f2fafef5f900"]  # 64位十六进制密钥

for i in range(len(plaintext)):
    p=plaintext[i]
    k=key[i]
    print("原始数据",p,end='  ')
    print("密钥", k, end='  ')
    encrypted_text = des_encrypt(p, k)
    print("加密后的数据:", encrypted_text,end='  ')

    plaintext2= des_decrypt(encrypted_text,k)
    print("解密后的数据:", plaintext2)


# S_input="111111"
# print("S盒输入",S_input,end='  ')
# print("S盒输出",substitution2(S_input))
#
# S_input="010000"
# print("S盒输入",S_input,end='  ')
# print("S盒输出",substitution2(S_input))