import random
import copy
sbox = [
            0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
            0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
            0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
            0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
            0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
            0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
            0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
            0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
            0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
            0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
            0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
            0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
            0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
            0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
            0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
            0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
        ]

def transform(byte_Str):
        return int(byte_Str, 16)

def S_box(byte_Str):
    byte=transform(byte_Str)
    row = (byte >> 4) & 0x0F
    col = byte & 0x0F
    return sbox[row * 16 + col]

def tt(Word):
    a=[ hex((Word>>(8*i))&0xff)[2:]  for i in range(4)]
    a.reverse()
    b=[ hex(S_box(x))[2:].zfill(2) for x in a]
    res=transform(b[0]+b[1]+b[2]+b[3])
    return res

def left_rotate(number, shift):
    return ((number << shift) | (number >> (32 - shift))) & 0xFFFFFFFF

def L1(number):
    return number^(left_rotate(number,2))^(left_rotate(number,10))^(left_rotate(number,18))^(left_rotate(number,24))

def L2(number):
    return number^(left_rotate(number,13))^(left_rotate(number,23))

def T1(word):
    t1=tt(word)
    return L1(t1)

def T2(word):
    t1=tt(word)
    return L2(t1)

def generate_key(Key):
    FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
    CK = [
        0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
        0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
        0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
        0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
        0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
        0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
        0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
        0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279
    ]

    MK=[ int(Key[i]+Key[i+1]+Key[i+2]+Key[i+3],16) for i in range(0,16,4)]
    K=[ MK[i]^FK[i] for i in range(4)]
    for i in range(32):
        t=hex(K[i] ^ T2(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ CK[i]))
        K.append(K[i]^T2(K[i+1]^K[i+2]^K[i+3]^CK[i]))
    rk=K[4:36]
    return rk


def deal(rs,Plain_text,way):

    M_word = [
        int(Plain_text[i] + Plain_text[i + 1] + Plain_text[i + 2] + Plain_text[i + 3], 16) for i in range(0, 16, 4)]
    X = M_word

    if way=='encrypt':
        for i in range(32):
            X.append(X[i] ^ T1(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rs[i]))
    elif way=='decrypt':
        for i in range(32):
            X.append(X[i] ^ T1(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rs[31 - i]))

    Y = X[-4:]
    Y.reverse()
    return Y



def ECB(rs,M,way):
    M2=[M[i:i + 16] for i in range(0, len(M), 16)]
    res=[]
    for m in M2:
        t=deal(rs, m, way)
        for i in range(4):
            t2=hex(t[i])[2:].zfill(8)
            for j in range(0,len(t2),2):
                res.append(t2[j:j+2])

    return res

def CBC(rs,M,way,Z):
    M2=[M[i:i + 16] for i in range(0, len(M), 16)]
    res=[]
    q=0
    tlist=[]
    for m in M2:
        if way=='encrypt':
            if q==0:
                m=XOR(m,Z)
            else:
                m=XOR(m,tlist[q-1])
            q+=1

        t = deal(rs, m, way)
        tlist.append(t)

        if way == 'decrypt':
            if q == 0:
                t = [x^y for x,y in zip(t,Z) ]
            else:
                t = XOR(M2[q-1],t)
                t2=[]
                for i in range(0, len(t), 4):
                    sub_list = t[i:i + 4]
                    combined_String = ''.join(sub_list)
                    number = int(combined_String, 16)
                    t2.append(number)
                t=t2
            q += 1

        for i in range(4):
            t2=hex(t[i])[2:].zfill(8)
            for j in range(0,len(t2),2):
                res.append(t2[j:j+2])

    return res

def XOR(A,B):   #A 是一个['01','23','45','67','89','ab','cd',..]  ,B类似=[1,2,3,4]，返回的类似A
    numbers = []
    res=[]
    for i in range(0, len(A), 4):
        # 取每4个元素组成子列表
        sub_list = A[i:i + 4]
        combined_String = ''.join(sub_list)
        number = int(combined_String, 16)
        numbers.append(number)
    for i in range(4):
        numbers[i]^=B[i]


    for i in range(4):
        t2 = hex(numbers[i])[2:].zfill(8)
        for j in range(0, len(t2), 2):
            res.append(t2[j:j + 2])

    return res


def OFB(state,rs,way,M):
    M2 = [M[i:i + 16] for i in range(0, len(M), 16)]
    res = []
    for m in M2:
        state = deal(rs, state, way)  #结果为十进制
        res += XOR(m, state)

        #把state转化为下次方便加密的形式
        new_state=[]
        for i in range(4):
            t = hex(state[i])[2:].zfill(8)
            for j in range(0, len(t), 2):
                new_state.append(t[j:j + 2])
        state=new_state

    return res

def CFB(state,rs,way,M):
    M2 = [M[i:i + 16] for i in range(0, len(M), 16)]
    res = []
    for m in M2:
        state = deal(rs, state, way)  #结果为十进制
        state=XOR(m, state)
        res += state

    return res

def CFB_D(state,rs,way,M):
    M2 = [M[i:i + 16] for i in range(0, len(M), 16)]
    res = []
    q=0
    for m in M2:
        if q==0:
            state = deal(rs, state, way)  #结果为十进制
            state=XOR(m, state)
            res += state
        else:
            state = deal(rs, M2[q-1], way)  # 结果为十进制
            state = XOR(m, state)
            res += state
        q+=1

    return res

def pad(m):
    if len(m)==16:
        return m
    elif  len(m)>16:
        raise ValueError("明文切割出错")
    else:
        for i in range(16-len(m)):
            if i==0:
                m.append('10')
            else :
                m.append('00')
        return m

def CTR(M,rs,counter,way):
    CP=copy.deepcopy(counter)
    # last_value=counter[-1]
    M2 = [M[i:i + 16] for i in range(0, len(M), 16)]
    res = []

    for m in M2:
        res += XOR(m, deal(rs, CP, way))
        CP[-1]=hex(int(CP[-1],16)+1)[2:].zfill(2)
    #counter[-1]=last_value
    return res

def display(R):
    r_hex = ''
    for r in R:
        r_hex+=r
    return r_hex
if __name__=='__main__':
    M=['01','23','45','67','89','ab','cd','ef','fe','dc','ba','98','76','54','32','10','ab','cd','12','34','ef','34','ab','fa','fe','dc','ba','98','76','54','32','10']
    K=['01','23','45','67','89','ab','cd','ef','fe','dc','ba','98','76','54','32','10']
    state=['ee','aa','47','a7','bf','ff','fd','1f','9e','dc','b6','78','66','e4','d2','1b']
    rs=generate_key(K)

    ecb=ECB(rs,M,'encrypt')
    ecb2=ECB(rs,ecb,'decrypt')

    print("ECB工作模型加解密结果")
    print("加密",end='')
    print(display(ecb))
    print("解密",end='')
    print(display(ecb2))
    print("----------------------------------------------------------------------------------------------------------")

    Z=[]
    for i in range(4):
        Z.append(random.randint(0, 2**32- 1))
    cbc=CBC(rs,M,'encrypt',Z)
    cbc2=CBC(rs,cbc,'decrypt',Z)
    print("CBC工作模型加解密结果")
    print("加密",end='')
    print(display(cbc))
    print("解密",end='')
    print(display(cbc2))
    print("----------------------------------------------------------------------------------------------------------")
    #
    ofb=OFB(state,rs,'encrypt',M)
    ofb2=OFB(state,rs,'encrypt',ofb)
    print("OFB工作模型加解密结果")
    print("加密",end='')
    print(display(ofb))
    print("解密",end='')
    print(display(ofb2))
    print("----------------------------------------------------------------------------------------------------------")
    #
    #
    cfb=CFB(state,rs,'encrypt',M)
    cfb2=CFB_D(state,rs,'encrypt',cfb)
    print("CFB工作模型加解密结果")
    print("加密",end='')
    print(display(cfb))
    print("解密",end='')
    print(display(cfb2))
    print("----------------------------------------------------------------------------------------------------------")
    #
    counter=[]
    for i in range(16):
        counter.append(hex(random.randint(0, 2**8- 1))[2:].zfill(2))
    ctr=CTR(M,rs,counter,'encrypt')
    ctr2=CTR(ctr,rs,counter,'encrypt')
    print("CTR工作模型加解密结果")
    print("加密",end='')
    print(display(ctr))
    print("解密",end='')
    print(display(ctr2))
    print("----------------------------------------------------------------------------------------------------------")

    #
    M=['01','23','45','67','89','ab','cd','ef','fe','dc','ba','98']
    print(pad(M))

