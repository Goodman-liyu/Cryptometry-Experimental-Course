from tool import *
import time

def aes_encrypt(plaintext, key):
    Nb = int(len(plaintext) / 4)
    Nk = int(len(key) / 4)
    Nr = get_Nr(Nb, Nk)

    state=init_state(plaintext,Nb)
    round_keys = key_expansion(key, Nk, Nb, Nr)

    add_round_key(state, round_keys[0:4][:])

    for round_num in range(1, Nr):
        sub_bytes(state,'state')
        shift_rows(state, Nb)
        mix_columns(state)
        add_round_key(state, round_keys[4 * round_num:4 * round_num + 4][:])

    # 最后一轮
    round_num += 1
    sub_bytes(state,'state')
    shift_rows(state, Nb)
    add_round_key(state, round_keys[4 * round_num:4 * round_num + 4][:])

    ciphertext = [hex(state[j][i])[2:].zfill(2).zfill(2)for i in range(4) for j in range(Nb)]

    return ciphertext


def aes_decrypt(ciphertext, key):
    Nb = int(len(ciphertext) / 4)
    Nk = int(len(key) / 4)
    Nr = get_Nr(Nb, Nk)

    state = init_state(ciphertext, Nb)

    round_keys = Inv_key_expansion(key, Nk, Nb, Nr)

    add_round_key(state, round_keys[Nr*4:Nr*4+4][:])

    for round_num in range(Nr-1, 0,-1):
        Inv_sub_bytes(state, 'state')
        Inv_shift_rows(state, Nb)
        Inv_mix_columns(state)
        add_round_key(state, round_keys[4 * round_num:4 * round_num + 4][:])

    # 最后一轮
    round_num -=1
    Inv_sub_bytes(state, 'state')
    Inv_shift_rows(state, Nb)
    add_round_key(state, round_keys[4 * round_num:4 * round_num + 4][:])
    plaintext = [hex(state[j][i])[2:].zfill(2) for i in range(4) for j in range(Nb)]
    return plaintext

if __name__ == "__main__":
    # 128位密钥（16字节）

    key = [
        0x00, 0x01, 0x20, 0x01,
        0x71, 0x01, 0x98, 0xae,
        0xda, 0x79, 0x17, 0x14,
        0x60, 0x15, 0x35, 0x94
    ]

    # 明文（16字节）
    plaintext = [
        0x00, 0x01, 0x00, 0x01,
        0x01, 0xa1, 0x98, 0xaf,
        0xda, 0x78, 0x17, 0x34,
        0x86, 0x15, 0x35, 0x66
    ]
    #print("原始明文:")
    #print(plaintext)
    # 加密
    # print("加密后的结果:")
    # ciphertext = aes_encrypt(plaintext, key)
    # print(ciphertext)
    # 解密
    # ciphertext=[int(x, 16) for x in ciphertext]
    # print("解密后的结果:")
    # decrypttext = aes_decrypt(ciphertext, key)
    # print(decrypttext)

    t1=0
    t2=0

    for i in range(1000):
        start = time.perf_counter()
        ciphertext = aes_encrypt(plaintext, key)
        end = time.perf_counter()
        t1=t1+end-start

        ciphertext = [int(x, 16) for x in ciphertext]
        start = time.perf_counter()
        decrypttext = aes_decrypt(ciphertext, key)
        end = time.perf_counter()
        t2 = t2 + end - start
    t1/=1000
    t2/=1000
    print(' encryption speed: %s mb/s' % (128 / (t1) / 1024))
    print(' decryption speed: %s mb/s' % (128 / (t2) / 1024))