# _*_ coding: utf-8 _*_
"""
Time:     2023/5/19 00:01
Author:   刘征昊(£·)
Version:  V 1.1
File:     SM3.py
Describe: 
"""

from basicMath.basic import rot_shift
from basicMath.type import byte2int, int2byte, HEXSTR, BYTESDIGEST, HEXSTRDIGEST, type_check

# 初始寄存器向量
IV: list[int] = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
# T参数
T = [0x79cc4519, 0x7a879d8a]


def file_process(filename: str, type_digest: BYTESDIGEST | HEXSTRDIGEST) -> BYTESDIGEST | HEXSTRDIGEST:
    """
    哈希函数文件处理
    :param filename: 待处理文件
    :param type_digest: 摘要输出类型
    :return: 摘要
    """
    if type_check(filename, str) and type_check(type_digest, type):
        with open(filename, "rb") as file:
            data = file.read()
            if type_digest == BYTESDIGEST:
                return SM3(data).digest()
            if type_digest == HEXSTRDIGEST:
                return SM3(data).hexdigest()


class SM3:
    """
    SM3杂凑算法
    """

    def __init__(self, msg: bytes = b"") -> None:
        """
        初始化
        :param msg: 消息
        """
        if type_check(msg, bytes):
            pass
        self.m = self.__pad_split(msg)

    @staticmethod
    def __pad_split(msg: bytes) -> list[list[bytes]]:
        """
        填充分割消息
        :param msg:
        :return:
        :return:
        """
        if type_check(msg, bytes):
            pass
        Msg = msg + int2byte(128, 1)
        l_msg = len(Msg) * 8
        l_pad = (448 - (l_msg % 512)) % 512
        Msg = Msg + int2byte(0, l_pad // 8)
        Msg = Msg + int2byte(l_msg - 8, 8)
        block_num = len(Msg) // 64
        Msg = [Msg[64 * i:64 * (i + 1)] for i in range(block_num)]
        Msg = [[x[4 * i:4 * (i + 1)] for i in range(16)] for x in Msg]
        return Msg

    @staticmethod
    def __FF(j: int, x: int, y: int, z: int) -> int:
        """
        逻辑函数FF
        :param j: 轮数
        :param x: 参数1
        :param y: 参数2
        :param z: 参数3
        :return: FF()
        """
        if type_check(j, int) and type_check(x, int) and type_check(y, int) and type_check(z, int):
            pass
        return (x ^ y ^ z) if 0 <= j <= 15 else (x & y) | (x & z) | (y & z)

    @staticmethod
    def __GG(j: int, x: int, y: int, z: int) -> int:
        """
        逻辑函数GG
        :param j: 轮数
        :param x: 参数1
        :param y: 参数2
        :param z: 参数3
        :return: G()
        """
        if type_check(j, int) and type_check(x, int) and type_check(y, int) and type_check(z, int):
            pass
        return (x ^ y ^ z) if 0 <= j <= 15 else (x & y) | ((~x) & z)

    @staticmethod
    def __P(x: int, flag: int) -> int:
        """
        逻辑函数P
        :param x:
        :param flag:
        :return:
        """
        if type_check(x, int) and type_check(flag, int):
            pass
        return x ^ rot_shift(x, 9, 32) ^ rot_shift(x, 17, 32) if flag == 0 else x ^ rot_shift(x, 15, 32) ^ rot_shift(x,
                                                                                                                     23,
                                                                                                                     32)

    def __get_W(self, block: list[bytes]) -> tuple[list, list]:
        """
        生成扩展字
        :param block: 字节块
        :return: 扩展字数组
        """
        if type_check(block, list):
            pass
        W = [byte2int(x) for x in block]
        W1 = []
        for j in range(16, 68):
            W.append(
                self.__P(W[j - 16] ^ W[j - 9] ^ rot_shift(W[j - 3], 15, 32), 1) ^ rot_shift(W[j - 13], 7, 32) ^ W[j - 6])
        for j in range(64):
            W1.append(W[j] ^ W[j + 4])
        return W, W1

    def __CF(self, v: list[int], block: list[bytes]) -> list[int]:
        """
        压缩函数
        :param v: 链接向量
        :param block: 字节块
        :return: 链接向量
        """
        if type_check(v, list) and type_check(block, list):
            pass
        W, W1 = self.__get_W(block)
        A, B, C, D, E, F, G, H = v
        for j in range(64):
            t = 0 if 0 <= j <= 15 else 1
            SS1 = rot_shift((rot_shift(A, 12, 32) + E + rot_shift(T[t], j % 32, 32)) % (1 << 32), 7, 32)
            SS2 = SS1 ^ rot_shift(A, 12, 32)
            TT1 = (self.__FF(j, A, B, C) + D + SS2 + W1[j]) % (1 << 32)
            TT2 = (self.__GG(j, E, F, G) + H + SS1 + W[j]) % (1 << 32)
            D = C
            C = rot_shift(B, 9, 32)
            B = A
            A = TT1
            H = G
            G = rot_shift(F, 19, 32)
            F = E
            E = self.__P(TT2, 0)
        V = [x ^ y for x, y in zip([A, B, C, D, E, F, G, H], v)]
        return V

    def hexdigest(self) -> HEXSTR:
        """
        生成消息摘要(16进制)
        :return: 16进制digest
        """
        V = IV
        for block in self.m:
            V = self.__CF(V, block)
        hex_ans = [f"{x:08x}" for x in V]
        hex_ans = "0x" + "".join(hex_ans)
        return hex_ans

    def digest(self) -> bytes:
        """
        生成消息摘要(bytes)
        :return: 字节串摘要
        """
        V = IV
        for block in self.m:
            V = self.__CF(V, block)
        byte_ans = [int2byte(x, 4) for x in V]
        byte_ans = b"".join(byte_ans)
        return byte_ans


if __name__ == "__main__":
    pass
