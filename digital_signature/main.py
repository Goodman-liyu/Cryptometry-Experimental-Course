from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from tool import *

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    message = "Hello, this is a message to hash."
    message_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    message_bytes = message.encode('utf-8')
    message_hash.update(message_bytes)
    digest = message_hash.finalize()
    # 将摘要输出为十六进制字符串
    hex_digest = digest.hex()

    print("原始摘要的十六进制表示:", hex_digest)
    # RSA签名与验签
    # P, Q = generate_PQ(128)
    # n = caculate_n(P, Q)
    # Euler_n = Euler(P, Q)
    # e = find_e(Euler_n)
    # d = get_d(e, Euler_n)
    # cipher_text = RSA_encode(hex_digest, e, n)
    # print("RSA签名信息",cipher_text)
    # plain_text = RSA_decode(cipher_text, d, n)
    # print("RSA验签结果",plain_text)

    # # ELGamal签名与验签
    # p, alpha, d = 10243, 2, 666
    # y = fast_modular_exponentiation(alpha, d, p)
    # print("私钥d：{} ； 公钥y：{} ".format(d, y))
    # # 公钥加密
    # cipher_text = ELGamal_encode(hex_digest, p, alpha, y)
    # print("ELGamal加密所得结果", cipher_text)
    # # 私钥解密
    # plain_text = ELGamal_decode(cipher_text, d, p)
    # print("ELGamal解密结果", plain_text)

    # ECC签名与验签
    # p = int("8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3", 16)
    # a = int("787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498", 16)
    # b = int("63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A", 16)
    # n = int("8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7", 16)
    # G = (int("421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D", 16), \
    #      int("0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2", 16))
    # d = 100
    # M = 5
    # Q = Gkey(d, G, a, p)
    #
    # encode_list = ECC_en_message(hex_digest, n, G, Q, a, p)
    # print("ECC加密所得结果,格式为(X1,C)")
    # print(encode_list)
    # plain_text = ECC_de_message(encode_list, n, a, p, d)
    # print("ECC解密所得结果")
    # print(plain_text)
