# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 23:50
Author:   刘征昊(£·)
Version:  V 1.1
File:     SM2_SV.py
Describe: 
"""
from math import ceil, log
from basicMath.ECC import Curve, TYPEPOINT
from basicMath.basic import invmod
from basicMath.type import int2byte, type_check, byte2int
from hash.SM3 import SM3


class SM2_SV:
    """
    SM2数字签名类
    """

    def __init__(self, crv: Curve, g: TYPEPOINT, N: int, ida: str, pa: TYPEPOINT, msg: str) -> None:
        """
        :param crv: 椭圆曲线
        :param g: 基点
        :param N: g的阶
        :param ida: A的ID
        :param pa: A公钥
        :param msg: 消息
        """
        if type_check(crv, Curve) and type_check(g, tuple) and type_check(N, int) \
                and type_check(ida, str) and type_check(pa, tuple) and type_check(msg, str):
            pass
        self.crv = crv
        self.g = g
        self.n = N
        self.ida = ida.encode("utf-8")
        self.pa = pa
        self.msg = msg.encode("utf-8")
        self.__l = ceil(log(self.crv.mod, 2) / 8)

    def __get_Z(self) -> bytes:
        """
        用户杂凑值生成
        :return: 杂凑值
        """
        entlen = len(self.ida) * 8
        ENTL = int2byte(entlen, 2)
        xg, yg = int2byte(self.g[0], self.__l), int2byte(self.g[1], self.__l)
        x, y = int2byte(self.pa[0], self.__l), int2byte(self.pa[1], self.__l)
        tmp = b"".join(
            [ENTL, self.ida, int2byte(self.crv.a, self.__l), int2byte(self.crv.b, self.__l), xg, yg, x,
             y])
        hexdigest = SM3(tmp).hexdigest()
        bytedigest = int2byte(int(hexdigest, 16), 32)
        return bytedigest

    def sign(self, da: int, k: int) -> tuple[bytes, bytes]:
        """
        签名算法
        :param da: A私钥
        :param k: 随机数
        :return: 签名(R,S)
        """
        if type_check(da, int) and type_check(k, int):
            pass
        M1 = self.__get_Z() + self.msg
        e = int(SM3(M1).hexdigest(), 16)
        x1, y1 = self.crv.power(k, self.g)
        R = (e + x1) % self.n
        if R == 0 or R == self.n - k:
            raise ValueError("SM2_SV:please reselect the param k!")
        S = invmod(1 + da, self.n) * (k - R * da) % self.n
        if S == 0:
            raise ValueError("SM2_SV:please reselect the param k!")
        return int2byte(R, self.__l), int2byte(S, self.__l)

    def verify(self, R: bytes, S: bytes) -> bool:
        """
        验签算法
        :param R: 签名1
        :param S: 签名2
        :return: bool
        """
        if type_check(R, bytes) and type_check(S, bytes):
            pass
        r_int, s_int = byte2int(R), byte2int(S)
        if not 0 < r_int < self.n:
            return False
        if not 0 < s_int < self.n:
            return False
        M1 = self.__get_Z() + self.msg
        e1 = int(SM3(M1).hexdigest(), 16)
        T = (r_int + s_int)%self.n
        if T == 0:
            return False
        x1, y1 = self.crv.add(self.crv.power(s_int, self.g), self.crv.power(T, self.pa))
        R1 = (e1 + x1) % self.n
        return R1 == r_int


if __name__ == "__main__":
    pass
