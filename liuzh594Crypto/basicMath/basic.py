# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 16:37
Author:   刘征昊(£·)
Version:  V 1.1
File:     basic.py
Describe: 基础运算
"""
from functools import reduce
from random import randint

from basicMath.type import type_check, TYPEMATRIX


def Egcd(a: int, b: int) -> list:
    """
    扩展欧拉算法:au+bv=g
    :param a:
    :param b:
    :return: x = [g, u, v]
    """
    if type_check(a, int) and type_check(b, int):
        pass
    x = [a, 1, 0]
    y = [b, 0, 1]
    while y[0] != 0:
        q = x[0] // y[0]
        for i in range(0, 3):
            x[i] = x[i] - q * y[i]
        tmp = x[:]
        x = y[:]
        y = tmp[:]
    return x


def invmod(a: int, n: int) -> int:
    """
    求a mod n 的逆元
    :param a:
    :param n:
    :return:
    """
    if type_check(a, int) and type_check(n, int):
        pass
    if n < 2:
        raise ValueError("basic:n must be bigger than 1")
    g, x, y = Egcd(a, n)
    if g != 1:
        raise ValueError("basic:no invmod")
    else:
        return x % n


def crt(r_lst: list, mod_lst: list) -> int:
    """
    中国剩余定理求解: x = c (mod n)
    :param r_lst: 余数c列表
    :param mod_lst: 模数n列表
    :return:
    """
    if type_check(r_lst, list) and type_check(mod_lst, list):
        pass
    # 累积 m = n1*n2*...*nk
    m = reduce(lambda x, y: x * y, (ni for ni in mod_lst))
    result = 0
    data = zip(r_lst, mod_lst)
    for ci, ni in data:
        mi = m // ni
        di = invmod(mi, ni)
        result += (ci * mi * di) % m
    return result % m


def matrix_multiply_mod(matrix1, matrix2, mod=0):
    """
    实现矩阵乘法，参数矩阵应满足乘法条件
    :param matrix1:
    :param matrix2:
    :param mod: 默认值为0则不是模意义下的矩阵运算
    :return:
    """
    col1, col2 = len(matrix1[0]), len(matrix2[0])
    raw1, raw2 = len(matrix1), len(matrix2)
    if col1 != raw2:
        raise ValueError("basic:Please confirm the matrix multiplication condition")
    else:
        result = [[0 for a in range(col2)] for b in range(raw1)]
        for i in range(raw1):
            for j in range(col2):
                for x in range(col1):
                    result[i][j] += matrix1[i][x] * matrix2[x][j]
                if mod != 0:
                    result[i][j] %= mod
        return result


def fast_power_matrix_mod(base: TYPEMATRIX, power: int, mod=0) -> TYPEMATRIX:
    """
    矩阵乘法的快速幂算法实现
    :param mod:
    :param base:
    :param power:
    :return:
    """
    if type_check(base, list) and type_check(power, int):
        pass
    if power <= 0:
        raise ValueError("basic:power must be postive")
    result = [[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]]
    while power > 0:
        if power & 1:
            result = matrix_multiply_mod(result, base, mod)
        power >>= 1
        base = matrix_multiply_mod(base, base, mod)
    return result


def fast_power(base: int, power: int, n: int = 0) -> int:
    """
    快速(模)幂运算
    :param base:
    :param power:
    :param n: n的默认值为0：快速幂运算;n>0:快速模幂运算
    :return:
    """
    if type_check(base, int) and type_check(power, int) and type_check(n, int):
        pass
    if power <= 0:
        raise ValueError("basic:power must be postive")
    result = 1
    if n == 0:
        while power > 0:
            if power & 1:
                result *= base
            power >>= 1
            base *= base
    else:
        while power > 0:
            if power & 1:
                result = result * base % n
            power >>= 1
            base = base ** 2 % n
    return result


def trans(m: TYPEMATRIX) -> TYPEMATRIX:
    """
    矩阵转置
    :param m:
    :return:
    """
    if type_check(m, list):
        pass
    return list(map(list, zip(*m)))


def isPrime(n: int) -> bool:
    """
    miller-rabin检验，返回是否是质数
    :param n:
    :return:
    """
    if type_check(n, int):
        pass
    if n == 2 or n == 3:
        return True
    if not n & 1:
        return False
    m, q, ans = n - 1, 0, 0
    while not m & 1:
        m >>= 1
        q += 1
    rd, seed1, seed2 = 20011224, 998244353, 20217371
    for i in range(0, 15):
        rd = rd * seed1 + seed2
        if rd < 0:
            rd = -rd
        a = rd % (n - 1) + 1
        tmp = fast_power(a, m, n)
        for j in range(0, q):
            ans = tmp ** 2 % n
            if ans == 1:
                if tmp != 1 and tmp != n - 1:
                    return False
                break
            tmp = ans
        if ans != 1:
            return False
    return True


def get_prime(len_bit: int) -> int:
    """
    随机获取一个二进制位长len_bit的整数
    :param len_bit:
    :return:
    """
    if type_check(len_bit, int):
        pass
    prm = (randint(2 ** (len_bit - 1), 2 ** len_bit) + 1) | 1
    # 利用或运算保证prm是一个奇数
    while not isPrime(prm):
        prm += 2
    return prm


def nextprime(n: int) -> int:
    """
    获取n的下一个质数
    :param n:
    :return:
    """
    if type_check(n, int):
        pass
    n = (n + 1) | 1
    while not isPrime(n):
        n += 2
    return n


def rot_shift(ans: int, n: int, l_bit: int) -> int:
    """
    循环左移
    :param l_bit: 循环字的比特大小
    :param ans:待移位整数
    :param n:左移位数
    :return :循环左移结果
    """
    if type_check(ans, int) and type_check(n, int):
        pass
    return ((ans << n) | (ans >> (l_bit - n))) & ((1 << l_bit) - 1)


if __name__ == "__main__":
    pass
