# _*_ coding: utf-8 _*_
"""
Time:     2023/5/20 13:14
Author:   刘征昊(£·)
Version:  V 1.1
File:     tests.py
Describe: This is the test samples of liuzh594Crypto!
"""
from liuzh594Crypto.basicMath.ECC import *
from liuzh594Crypto.basicMath.GF import *
from liuzh594Crypto.basicMath.basic import *
from liuzh594Crypto.basicMath.type import *
from liuzh594Crypto.blockCipher.SM4 import *
from liuzh594Crypto.digitalSignature.SM2_SV import *
from liuzh594Crypto.hash.SM3 import *
from liuzh594Crypto.pubkeyCipher.RSA import *
from liuzh594Crypto.pubkeyCipher.SM2 import *


def basic_test():
    """
    basic.py测试样例
    :return:
    """
    # 生成素数
    prime1 = get_prime(512)
    print(prime1)
    # 素性检验
    prime2 = nextprime(prime1)
    print(isPrime(prime2))
    # 求逆元
    inv = invmod(prime2, prime1)
    print(inv)
    # 快速模幂运算
    fast = fast_power(prime1, 5 << 20, prime2)
    print(fast)
    # 矩阵快速(模)幂运算
    mtx: TYPEMATRIX = [[5, 2, 0],
                       [5, 9, 4],
                       [119, 121, 122]]
    mtx_fast = fast_power_matrix_mod(mtx, 13 << 14, 26)
    print(mtx_fast)
    # 循环左移
    print(prime2 == rot_shift(prime2, 512, 512))
    # 中国剩余定理
    r, mod = [2, 3, 2], [3, 5, 7]
    print(crt(r, mod))


def type_test():
    """
    type.py测试样例
    :return:
    """
    x_str = "594"
    print(x_str)
    # 字符串转字节串
    x_bytes = str2byte(x_str)
    print(x_bytes)
    # 字节串转HEXSTR
    x_hex = byte2hex(x_bytes, len(x_bytes) * 2)
    print(x_hex)
    # 字节串转整数
    x_int = byte2int(x_bytes)
    print(x_int)
    # HEXSTR转字节串
    x_bytes = hex2byte(x_hex, (len(x_hex) - 2) // 2)
    print(x_bytes)
    # 整数转字节串
    x_bytes = int2byte(x_int, len_bytes(x_int))
    print(x_bytes)
    # 字节串转字符串
    x_str = byte2str(x_bytes)
    print(x_str)
    # 椭圆曲线点的转换
    # 略，详见SM2


def ECC_test():
    """
    ECC.py测试样例
    :return:
    """
    # 建立椭圆曲线
    p = 115792089210356248756420345214020892766250353991924191454421193933289684991999
    a = 115792089210356248756420345214020892766250353991924191454421193933289684991996
    b = 18505919022281880113072981827955639221458448578012075254857346196103069175443
    curve = Curve(a, b, p)
    A = (64901889550129866513443884082574452575157116031103742365434905633820925813192,
         84553412528427919723206133858954594911213526647800598970633596412071681640913)
    B = (64901889550129866513443884082574452575157116031103742365434905633820925813192,
         84553412528427919723206133858954594911213526647800598970633596412071681640913)
    k = 1090995336408336436299323842074559377173634035498855897587250085319472956
    # 点加
    print(*curve.add(A, B))
    # 91829719240076595600910287219737299259627413891073174690491219092963035830325
    # 31474822276849859104123114646070976974921401394140157637420547181522913249875
    # 点减
    print(*curve.minus(A, B))
    # 0
    # 0
    # 倍点:double-and-add
    print(*curve.power(k, A))
    # 57373321148051506091723093715148369162664271829435462559258806045759894672711
    # 47810523934102992307219225430955925621395444436399395870291687870429993066087

    # 倍点:NAF
    print(*curve.power_NAF(k, A))
    # 57373321148051506091723093715148369162664271829435462559258806045759894672711
    # 47810523934102992307219225430955925621395444436399395870291687870429993066087

    # 倍点:w-NAF
    print(*curve.power_w_NAF(k, 4, A))
    # 57373321148051506091723093715148369162664271829435462559258806045759894672711
    # 47810523934102992307219225430955925621395444436399395870291687870429993066087


def GF_test():
    """
    GF.py测试样例
    :return:
    """
    # 加法
    print(f'{add_minus_GF(int("af", 16), int("3b", 16)):02x}')
    # 减法
    print(f'{add_minus_GF(int("89", 16), int("4d", 16)):02x}')
    # 乘法
    print(f'{multiply_GF(int("0e", 16), int("74", 16)):02x}')
    # 除法
    d, m = div_mod_GF(int("b9", 16), int("74", 16))
    print(f'{d:02x} {m:02x}')
    # 快速模幂
    print(f'{fast_power_GF(int("4d", 16), 63108):02x}')
    # 逆元
    print(f'{invmod_GF(int("3c", 16), 283):02x}')


def SM4_test():
    """
    SM4.py测试样例
    :return:
    """
    # 创建实例 载入密钥
    sm4 = SM4("0x4046fb1985d94a7f1ff55ec7ec5f6054")
    # 加密
    print(byte2hex(sm4.encrypt(hex2byte("0x6b956ddb0faff373bc338cb600739f23", 16)), 32))
    # 解密
    print(byte2hex(sm4.decrypt(hex2byte("0xc04a9b311a2fc245f742c5719fcf249d", 16)), 32))
    # ECB加密
    print(byte2hex(sm4.ECB(hex2byte("0xc04a9b311a2fc245f742c5719fcf249d", 16), ENCRYPT), 64))
    # ECB解密
    c = "0x20712aff4346e76138a94e586ad59171bbdaa4aae5de571e757af456e80dbed0"
    print(byte2hex(sm4.ECB(hex2byte(c, 32), DECRYPT), 32))
    # CBC加密
    iv = "0xa8638d2fb23cc49206edd7c84532eaab"
    print(byte2hex(sm4.CBC(hex2byte("0xc04a9b311a2fc245f742c5719fcf249d", 16), iv, ENCRYPT), 64))
    # CBC解密
    c = "0xec0a6bda48356253a34e7600d63f4a35229d10ae51e59da0c42cbe739153952c"
    print(byte2hex(sm4.CBC(hex2byte(c, 32), iv, DECRYPT), 32))
    # 文件ECB加密
    sm4.file_process_bmp("pic_original.bmp", MODEECB, ENCRYPT)
    # pic_original_ECB.bmp
    # 文件CBC加密
    sm4.file_process_bmp("pic_original.bmp", MODECBC, ENCRYPT, iv)
    # pic_original_CBC.bmp


def RSA_test():
    """
    RSA.py测试样例
    :return:
    """
    # 构建1024bit素数参数的RSA实例
    rsa = RSA(1024)
    # 读取模数n,但无法访问p/q
    print(rsa.param.n)
    # 生成公钥
    print(rsa.param.get_pubkey())
    # 生成公钥
    print(rsa.param.get_pvtkey())
    # RSA加密
    en = rsa.encrypt(str2byte("haha,I'm lzh.I'm falling love with wyz!"))
    print(byte2hex(en, len(en) * 2))
    # RSA解密
    de = rsa.decrypt(en)
    print(byte2str(de))


def SM2_test():
    """
    SM2.py测试样例
    :return:
    """
    # 建立椭圆曲线
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    curve = Curve(a, b, p)
    G = (0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
         0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2)
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    sm2 = SM2(G, curve, n)
    # SM2加密
    M = str2byte("hello,wyz.I'm Lzh")
    k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    PB = (0x435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A,
          0x75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42)
    C = sm2.encrypt(M, k, PB)
    print(byte2hex(C, len(M) * 2))
    # SM2解密
    dB = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
    M1 = sm2.decrypt(C, dB)
    print(byte2str(M1))


def SM3_test():
    """
    SM3.py测试样例
    :return:
    """
    # 创建SM3实例
    M = str2byte("the missed love... ---Lzh&wyz")
    sm3 = SM3(M)
    # 输出字节串消息摘要
    print(sm3.digest())
    # 输出十六进制消息摘要
    print(sm3.hexdigest())
    # 对文件签名
    hex_digest = file_process("pic_original.bmp", HEXSTRDIGEST)
    print(hex_digest)
    byte_digest = file_process("pic_original.bmp", BYTESDIGEST)
    print(byte_digest)


def SM2_SV_text():
    """
    SM2_SV.py测试样例
    :return:
    """
    # 建立椭圆曲线
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    curve = Curve(a, b, p)
    G = (0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
         0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2)
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    # 签名者A的信息
    IDA = "2529346431@qq.com"
    PA = (0x0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A,
          0x7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857)
    M = "today is 520, but I' postive..."
    # 创建SM2_SV实例
    sm2_sv = SM2_SV(curve, G, n, IDA, PA, M)
    # A用私钥签名
    dA = 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
    k = 0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
    r, s = sm2_sv.sign(dA, k)
    print(byte2hex(r, len(r) * 2))
    print(byte2hex(s, len(s) * 2))
    # B用公钥验签
    print(sm2_sv.verify(r, s))


if __name__ == "__main__":
    """
    可以根据测试需求进行代码注释部分的添加与解除
    """
    """
    basicMath测试样例
    """
    # basic_test()
    # type_test()
    # ECC_test()
    # GF_test()

    """
    blockCipher测试样例
    """
    # SM4_test()

    """
    pubkeyCipher测试样例
    """
    # RSA_test()
    # SM2_test()

    """
    hash测试样例
    """
    # SM3_test()

    """
    digitalSignature测试样例
    """
    SM2_SV_text()