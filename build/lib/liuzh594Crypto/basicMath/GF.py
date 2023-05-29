# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 16:26
Author:   刘征昊(£·)
Version:  V 1.1
File:     GF.py
Describe: GF(2^8)有限域上的基础运算
"""
from basicMath.type import type_check, TYPEMATRIX


def add_minus_GF(a: int, b: int) -> int:
    """
    GF(2^8)上的加减法
    :param a:
    :param b:
    :return:
    """
    if type_check(a, int) and type_check(b, int):
        pass
    return a ^ b


def multiply_GF(a: int, b: int, poly: int = 283) -> int:
    """
    GF(2^8)上的乘法
    :param a:
    :param b:
    :param poly: 默认为283(int)/1 0001 1011(bin)
    :return:
    """
    if type_check(a, int) and type_check(b, int) and type_check(poly, int):
        pass
    res = 0
    l = poly.bit_length() - 1
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        b >>= 1
        if a >> l:
            a ^= poly
    return res


def div_mod_GF(a: int, b: int) -> tuple[int, int]:
    """
    GF(2^8)上的除法和取模
    :param a:
    :param b:
    :return:
    """
    if type_check(a, int) and type_check(b, int):
        pass
    if b == 0:
        raise ZeroDivisionError
    d = 0
    la, lb = a.bit_length(), b.bit_length()
    while la >= lb:
        l = la - lb
        a = a ^ (b << l)
        d = d | (1 << l)
        la = a.bit_length()
    return d, a


def Egcd_GF(a: int, b: int, poly: int = 283) -> list:
    """
    扩展欧拉算法:au+bv=g
    params: a, b®
    return: x = [g, u, v]
    """
    if type_check(a, int) and type_check(b, int) and type_check(poly, int):
        pass
    x = [a, 1, 0]
    y = [b, 0, 1]
    while y[0] != 0:
        q, r = div_mod_GF(x[0], y[0])
        x[0], y[0] = y[0], r
        x[1], y[1] = y[1], add_minus_GF(x[1], multiply_GF(q, y[1], poly))
        x[2], y[2] = y[2], add_minus_GF(x[2], multiply_GF(q, y[2], poly))
    return x


def invmod_GF(a: int, n: int, poly: int = 283) -> int:
    """
    求a mod n 的逆元(GF(2^8)上)
    :param a:
    :param n:
    :param poly:
    :return:
    """
    if type_check(a, int) and type_check(n, int) and type_check(poly, int):
        pass
    g, x, y = Egcd_GF(a, n, poly)
    return x


def matrix_multiply_GF(matrix1: TYPEMATRIX, matrix2: TYPEMATRIX, poly: int = 283) -> TYPEMATRIX:
    """
    实现GF(2^8)上矩阵乘法，参数矩阵应满足乘法条件
    :param matrix1:
    :param matrix2:
    :param poly:
    :return:
    """
    if type_check(matrix1, list[list]) and type_check(matrix2, list[list]) and type_check(poly, int):
        pass
    col1, col2 = len(matrix1[0]), len(matrix2[0])
    raw1, raw2 = len(matrix1), len(matrix2)
    if col1 != raw2:
        raise ValueError("GF:Please confirm the matrix multiplication condition")
    else:
        result = [[0 for _ in range(col2)] for _ in range(raw1)]
        for i in range(raw1):
            for j in range(col2):
                for x in range(col1):
                    result[i][j] = add_minus_GF(result[i][j], multiply_GF(matrix1[i][x], matrix2[x][j], poly))
        return result


def fast_power_GF(base: int, power: int, poly: int = 283) -> int:
    """
    GF上快速幂运算
    :param base:
    :param power:
    :param poly:
    :return:
    """
    if type_check(base, int) and type_check(poly, int) and type_check(power, int):
        pass
    if power <= 0:
        raise ValueError("GF:power must be postive")
    result = 1
    while power > 0:
        if power & 1:
            result = multiply_GF(result, base, poly)
        power >>= 1
        base = multiply_GF(base, base, poly)
    return result
