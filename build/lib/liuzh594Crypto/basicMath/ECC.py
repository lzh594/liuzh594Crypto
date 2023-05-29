# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 23:52
Author:   刘征昊(£·)
Version:  V 1.1
File:     ECC.py
Describe: 
"""
from basic import invmod
from type import TYPEPOINT, type_check

# 无穷远点
NULL_POINT: TYPEPOINT = (0, 0)


class Curve:
    """
    Zp上的椭圆曲线类
    """

    def __init__(self, a: int, b: int, p: int) -> None:
        """
        椭圆曲线参数
        :param a: 参数a
        :param b: 参数b
        :param p: 模数
        """
        if type_check(a, int) and type_check(b, int) and type_check(p, int):
            pass
        self.a = a
        self.b = b
        self.mod = p

    @staticmethod
    def is_null(pt: TYPEPOINT) -> bool:
        """
        判断是否为无穷远点
        :param pt: 待判断点
        :return: bool
        """
        if type_check(pt, tuple):
            pass
        if pt == NULL_POINT:
            return True

    def is_opposite(self, pt1: TYPEPOINT, pt2: TYPEPOINT) -> bool:
        """
        判断是否互为负元
        :param pt1: 点
        :param pt2: 点
        :return: BOOL
        """
        if type_check(pt1, tuple) and type_check(pt2, tuple):
            pass
        x1, y1 = pt1
        x2, y2 = pt2
        return x1 == x2 and y1 == -y2 % self.mod

    def check(self, pt: TYPEPOINT) -> bool:
        """
        判断点是否在椭圆曲线上
        :param pt: 点
        :return: bool
        """
        if type_check(pt, tuple):
            pass
        x, y = pt
        if self.is_null(pt):
            return True
        left = (y ** 2) % self.mod
        right = self.right(x)
        return left == right

    def right(self, x: int) -> int:
        """
        Right part of the curve equation: x^3 + a*x + b (mod p)
        """
        if type_check(x, int):
            pass
        return (x ** 3 + self.a * x + self.b) % self.mod

    def add(self, pt1: TYPEPOINT, pt2: TYPEPOINT) -> TYPEPOINT:
        """
        点的加法
        :param pt1: 点
        :param pt2: 点
        :return: 点之和
        """
        if type_check(pt1, tuple) and type_check(pt2, tuple):
            pass
        if self.is_null(pt1):
            return pt2
        if self.is_null(pt2):
            return pt1
        if self.is_opposite(pt1, pt2):
            return NULL_POINT
        x1, y1 = pt1
        x2, y2 = pt2
        if x1 != x2:
            slope = (y2 - y1) * invmod((x2 - x1), self.mod) % self.mod
        else:
            slope = (3 * x1 ** 2 + self.a) * invmod(2 * y1, self.mod) % self.mod
        x = (slope ** 2 - x1 - x2) % self.mod
        y = (-y1 + slope * (x1 - x)) % self.mod
        return x, y

    def minus(self, pt1: TYPEPOINT, pt2: TYPEPOINT) -> TYPEPOINT:
        """
        点的减法
        :param pt1: 点
        :param pt2: 点
        :return: 差
        """
        if type_check(pt1, tuple) and type_check(pt2, tuple):
            pass
        pt2_m = (pt2[0], -pt2[1])
        return self.add(pt1, pt2_m)

    def power(self, n: int, pt: TYPEPOINT) -> TYPEPOINT:
        """
        点乘运算
        :param n: 系数
        :param pt: 点
        :return: 积
        """
        if type_check(pt, tuple):
            pass
        if n == 0 or pt == NULL_POINT:
            return NULL_POINT
        res = NULL_POINT
        while n:
            if n & 1:
                res = self.add(res, pt)
            pt = self.add(pt, pt)
            n >>= 1
        return res

    @staticmethod
    def NAF(e: int) -> list[int]:
        """
        NAF表示转换
        :param e:待转化整数
        :return Z:e的NAF表示
        """
        if type_check(e, int):
            pass
        Z = []
        while e > 0:
            if e & 1:
                z = 2 - (e % 4)
                e -= z
            else:
                z = 0
            e >>= 1
            Z.append(z)
        return Z[::-1]

    @staticmethod
    def w_NAF(e: int, w: int) -> list[int, ...]:
        """
        w-NAF表示转换
        :param e: 待转换整数
        :param w: 窗口大小
        :return Z: e的w-NAF表示
        """
        if type_check(e, int) and type_check(w, int):
            pass
        Z = []
        while e > 0:
            if e & 1:
                tmp = e % (1 << w)
                z = tmp if tmp < (1 << (w - 1)) else tmp - (1 << w)
                e -= z
            else:
                z = 0
            e >>= 1
            Z.append(z)
        return Z[::-1]

    def power_NAF(self, n: int, pt: TYPEPOINT) -> TYPEPOINT:
        """
        NAF算法的点乘运算
        :param n: 系数
        :param pt: 点
        :return: 积
        """
        if type_check(n, int) and type_check(pt, tuple):
            pass
        if n == 0 or pt == NULL_POINT:
            return NULL_POINT
        res = NULL_POINT
        n = self.NAF(n)
        for ni in n:
            res = self.add(res, res)
            if ni == 1:
                res = self.add(res, pt)
            if ni == -1:
                res = self.minus(res, pt)
        return res

    def power_w_NAF(self, n: int, w: int, pt: TYPEPOINT) -> TYPEPOINT:
        """
        w-NAF算法的点乘运算
        :param n: 系数
        :param w: 窗口大小
        :param pt: 点
        :return: 积
        """
        if type_check(n, int) and type_check(w, int) and type_check(pt, tuple):
            pass
        if n == 0 or pt == NULL_POINT:
            return NULL_POINT
        res = NULL_POINT
        n = self.w_NAF(n, w)
        nip = [pt] + [self.power_NAF(i, pt) for i in range(3, (1 << (w - 1)), 2)]
        for ni in n:
            res = self.add(res, res)
            if ni > 0:
                res = self.add(res, nip[(ni - 1) // 2])
            if ni < 0:
                res = self.minus(res, nip[(-ni - 1) // 2])
        return res

    def get_order(self, p, limit=None):
        """
        获取点p的阶
        :param p:
        :param limit:
        :return:
        """
        order = 1
        res = p
        while not self.is_null(res):
            res = self.add(res, p)
            order += 1
            if limit is not None and order >= limit:
                return None
        return order


if __name__ == "__main__":
    pass
