# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 19:40
Author:   刘征昊(£·)
Version:  V 1.1
File:     RSA.py
Describe: 
"""
from math import gcd

from liuzh594Crypto.basicMath.basic import get_prime, invmod, fast_power, crt
from liuzh594Crypto.basicMath.type import byte2int, int2byte, len_bytes, type_check


class RSAkeyParam:
    """
    RSA密钥参数类
    """

    def __init__(self, p: int, q: int) -> None:
        if type_check(p, int) and type_check(q, int):
            pass
        self.__p = p
        self.__q = q

    @property
    def n(self):
        """
        读取n
        :return: n
        """
        return self.__p * self.__q

    @property
    def __phi(self):
        """
        读取phi
        :return: phi
        """
        return (self.__p - 1) * (self.__q - 1)

    def get_pubkey(self, e: int = 65537) -> tuple[int, int]:
        """
        获取公钥
        :param e:
        :return: (n,e)
        """
        if type_check(e, int):
            pass
        if gcd(e, self.__phi) > 1:
            raise ValueError("RSA:please reselect the param e!")
        return self.n, e

    def get_pvtkey(self, e: int = 65537) -> tuple[int, int]:
        """
        获取私钥
        :param e:
        :return: (n,d)
        """
        if type_check(e, int):
            pass
        if gcd(e, self.__phi) > 1:
            raise ValueError("RSA:please reselect the param e!")
        d = invmod(e, self.__phi)
        return self.n, d


class RSA:
    """
    RSA类
    """

    def __init__(self, len_bits: int) -> None:
        """
        初始化参数
        :param len_bits: 素数参数比特长度
        """
        if type_check(len_bits, int):
            pass
        if len_bits < 1024:
            raise ValueError("RSA:We advise you to use more than 1024 bit, maybe 2048 bit!")
        self.param = RSAkeyParam(get_prime(len_bits + 1), get_prime(len_bits + 3))

    def encrypt(self, message: bytes) -> bytes:
        """
        RSA加密
        :param message: 明文
        :return: 密文
        """
        if type_check(message, bytes):
            pass
        if not 0 < byte2int(message) < self.param.n:
            raise ValueError("RSA:the message is too long!")
        n, e = self.param.get_pubkey()
        encrypted = fast_power(byte2int(message), e, n)
        return int2byte(encrypted, len_bytes(encrypted))

    def decrypt(self, cipher: bytes) -> bytes:
        """
        RSA解密——CRT加速
        :param cipher: 密文
        :return: 明文
        """
        if type_check(cipher, bytes):
            pass
        if not 0 < byte2int(cipher) < self.param.n:
            raise ValueError("RSA:the cipher is too long!")
        n, d = self.param.get_pvtkey()
        c_lst = [fast_power(byte2int(cipher), d % (self.param._RSAkeyParam__p - 1), self.param._RSAkeyParam__p),
                 fast_power(byte2int(cipher), d % (self.param._RSAkeyParam__q - 1), self.param._RSAkeyParam__q)]
        n_lst = [self.param._RSAkeyParam__p, self.param._RSAkeyParam__q]
        decrypted = crt(c_lst, n_lst)
        return int2byte(decrypted, len_bytes(decrypted))


if __name__ == "__main__":
    pass
