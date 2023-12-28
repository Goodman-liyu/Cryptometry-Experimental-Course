from function import *

if __name__=='__main__':
    #采用《密码学引论》172页的示例
    key = [CustomString("3d"), CustomString("4c"), CustomString("4b"), CustomString("e9")
        , CustomString("6a"), CustomString("82"), CustomString("fd"), CustomString("ae")
        , CustomString("b5"), CustomString("8f"), CustomString("64"), CustomString("1d")
        , CustomString("b1"), CustomString("7b"), CustomString("45"), CustomString("5b")]

    IV = [CustomString("84"), CustomString("31"), CustomString("9a"), CustomString("a8")
        , CustomString("de"), CustomString("69"), CustomString("15"), CustomString("ca")
        , CustomString("1f"), CustomString("6b"), CustomString("da"), CustomString("6b")
        , CustomString("fb"), CustomString("d8"), CustomString("c7"), CustomString("66")]

    R1 = CustomString("0")
    R2 = CustomString("0")

    S = init_S(key, IV)
    disp(S)
    for i in range(32):
        x0, x1, x2, x3 = BitReconstruction(S)
        W, R1, R2 = F(x0, x1, x2, R1, R2)
        S = LFSRWithInitialisationMode(W, S)

    for i in range(3):
        x0, x1, x2, x3 = BitReconstruction(S)
        W, R1, R2 = F(x0, x1, x2, R1, R2)
        S = LFSRWithWorkMode(S)
        z = W ^ x3
        print("密钥流：Z_{}：".format(i), z)
