# _*_ coding: utf-8 _*_
"""
Time:     2023/5/19 20:44
Author:   刘征昊(£·)
Version:  V 1.1
File:     SM2.py
Describe: 
"""
from math import ceil, floor, log
from liuzh594Crypto.basicMath.ECC import Curve
from liuzh594Crypto.basicMath.type import int2byte, byte2int, point2byte, byte2point, TYPEPOINT, type_check
from liuzh594Crypto.hash.SM3 import SM3

class SM2:
    """
    SM2类
    """
    crv: Curve

    def __init__(self, g: TYPEPOINT, crv: Curve, n: int) -> None:
        """

        :param g: 生成元
        :param n: g的阶
        :param crv: 椭圆曲线
        """
        if type_check(g, tuple) and type_check(crv, Curve):
            pass
        self.g = g
        self.n = n
        self.crv = crv
        self.l = ceil(log(self.crv.mod, 2) / 8)

    @staticmethod
    def __KDF(Z: bytes, klen: int) -> bytes:
        """
        密钥派生函数
        :param Z: 字节串
        :param klen: 所需密钥比特长度
        :return: 派生密钥
        """
        if type_check(Z, bytes) and type_check(klen, int):
            pass
        ct = 0x00000001
        upper = ceil(klen / 256) + 1
        H = []
        for i in range(1, upper):
            Hi = SM3(Z + int2byte(ct, 4)).digest()
            H.append(Hi)
            ct += 1
        tmp = b"".join(H)
        tmp = byte2int(tmp)
        if klen % 256 != 0:
            tmp >>= (256 - (klen - (256 * floor(klen / 256))))
        K = int2byte(tmp, ceil(klen / 8))
        return K

    def encrypt(self, msg: bytes, key: int, pb: TYPEPOINT) -> bytes:
        """
        SM2加密
        :param msg: 明文
        :param key: 私钥
        :param pb: 公钥
        :return: 密文
        """
        if type_check(msg, bytes) and type_check(key, int) and type_check(pb, tuple):
            pass
        if not 0 < key < self.n:
            raise ValueError("SM2:please reselect the param key")
        c1 = self.crv.power(key, self.g)
        c1 = point2byte(c1, self.l)
        x2, y2 = self.crv.power(key, pb)
        x2, y2 = int2byte(x2, self.l), int2byte(y2, self.l)
        t = self.__KDF(x2 + y2, len(msg) * 8)
        if byte2int(t) == 0:
            raise ValueError("SM2:please reselect the param key")
        msg_int = byte2int(msg)
        c2 = int2byte(msg_int ^ byte2int(t), ceil(msg_int.bit_length() / 8))
        c3 = SM3(x2 + msg + y2).digest()
        cpr = b"".join([c1, c2, c3])
        # cpr = "0x" + f"{byte2int(cpr):x}".rjust(len(cpr) * 2, "0")
        return cpr

    def decrypt(self, cpr: bytes, db: int) -> bytes:
        """
        SM2解密
        :param cpr: 密文
        :param db: 私钥
        :return: 明文
        """
        if type_check(cpr, bytes) and type_check(db, int):
            pass
        c1 = cpr[:2 * self.l + 1]
        c1 = byte2point(c1, self.l)
        if not self.crv.check(c1):
            raise ValueError("SM2:point C1 is not on the curve!")
        x2, y2 = self.crv.power(db, c1)
        x2, y2 = int2byte(x2, self.l), int2byte(y2, self.l)
        klen = 8 * len(cpr) - (8 * (2 * self.l + 1)) - 256
        t = self.__KDF(x2 + y2, klen)
        if byte2int(t) == 0:
            raise ValueError("SM2:please reselect the param key!")
        c2 = cpr[2 * self.l + 1:2 * self.l + 1 + klen // 8]
        msg = int2byte(byte2int(c2) ^ byte2int(t), klen // 8)
        c3 = cpr[2 * self.l + 1 + klen // 8:]
        u = SM3(x2 + msg + y2).digest()
        if u != c3:
            raise ValueError("SM2:cipher is incorrect!")
        # msg = "0x" + f"{msg:x}".rjust(klen // 4, "0")
        return msg


if __name__ == "__main__":
    pass