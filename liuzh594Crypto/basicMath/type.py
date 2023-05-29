# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 17:21
Author:   刘征昊(£·)
Version:  V 1.1
File:     type.py
Describe: 
"""
from math import ceil

# 十六进制字符串类型：0xabcd...
HEXSTR = str
# SM4类型
TYPESM4 = int
# 哈希摘要类型
BYTESDIGEST = bytes
HEXSTRDIGEST = HEXSTR
# 坐标点类型
TYPEPOINT = tuple[int, int]
# 矩阵类型
TYPEMATRIX = list[list[int]]


def byte2hex(b: bytes, l_hex: int) -> HEXSTR:
    """
    bytes to hex
    :param b:
    :param l_hex: 16进制长度(不含0x)
    :return:
    """
    if type_check(b, bytes) and type_check(l_hex, int):
        pass
    i = byte2int(b)
    h = "0x" + f"{i:x}".rjust(l_hex, "0")
    return h


def hex2byte(h: HEXSTR, l_byte: int) -> bytes:
    """
    hex to bytes
    :param h:
    :param l_byte: 字节长度
    :return:
    """
    if type_check(h, HEXSTR) and type_check(l_byte, int):
        pass
    i = int(h[2:], 16)
    b = int2byte(i, l_byte)
    return b


def byte2int(b: bytes) -> int:
    """
    bytes to int
    :param b: 待转换的字节
    :return:
    """
    if type_check(b, bytes):
        pass
    return int.from_bytes(b, byteorder="big")


def len_bytes(i: int) -> int:
    """
    获取整数的最小字节宽度
    :param i:
    :return:
    """
    if type_check(i, int):
        pass
    return ceil(i.bit_length() / 8)


def int2byte(i: int, l_byte: int) -> bytes:
    """
    int to bytes
    :param i: 待转换的整数
    :param l_byte: byte宽度
    :return:
    """
    if type_check(i, int) and type_check(l_byte, int):
        pass
    if i == 0:
        return bytes([0]) * l_byte
    return i.to_bytes(l_byte, byteorder="big")


def str2byte(s: str) -> bytes:
    """
    str tp bytes
    :param s: 待转换字符串
    :return: 字节串
    """
    if type_check(s, str):
        pass
    b = s.encode("utf-8")
    return b


def byte2str(b: bytes) -> str:
    """
    bytes to str
    :param b: 待转换字节串
    :return: 字符串
    """
    if type_check(b, bytes):
        pass
    s = b.decode("utf-8")
    return s


def point2byte(pt: TYPEPOINT, l_byte: int) -> bytes:
    """
    点转换为字节串
    :param l_byte: 坐标的字节串长度
    :param pt: 点
    :return: 点字节串
    """
    if type_check(pt, tuple) and type_check(l_byte, int):
        pass
    xp, yp = pt
    X1 = int2byte(xp, l_byte)
    Y1 = int2byte(yp, l_byte)
    PC = int2byte(4, 1)
    S = b"".join([PC, X1, Y1])
    return S


def byte2point(bt: bytes, l_byte: int) -> TYPEPOINT:
    """
    字节串转为点
    :param l_byte: 坐标的字节串长度
    :param bt: 点的字节串
    :return: 点
    """
    if type_check(bt, bytes) and type_check(l_byte, int):
        pass
    _, X1, Y1 = bt[:1], bt[1:l_byte + 1], bt[l_byte + 1:]
    xp, yp = byte2int(X1), byte2int(Y1)
    return xp, yp


def type_check(c: object, t: object) -> object:
    if type(c) == t:
        return True
    else:
        raise TypeError(f"type:param {c} is {type(c)} but it must be {t}!")


if __name__ == "__main__":
    x = b"\x11"
    print(byte2hex(x, 10))
    type_check(100, HEXSTR)
