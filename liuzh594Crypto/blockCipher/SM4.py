# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 16:59
Author:   刘征昊(£·)
Version:  V 1.1
File:     SM4.py
Describe: 
"""
import os.path

from liuzh594Crypto.basicMath.type import HEXSTR, byte2hex, hex2byte, byte2int, TYPESM4, type_check
from liuzh594Crypto.basicMath.basic import rot_shift

# 工作模式加解密选择
ENCRYPT: TYPESM4 = 1
DECRYPT: TYPESM4 = 0

# 文件加密工作模式选择
MODEECB: TYPESM4 = ord("e")
MODECBC: TYPESM4 = ord("c")

# 合成置换T的模式选择
T_flag: int = 1

# S盒
S: list[list[str]] = [
    ["d6", "90", "e9", "fe", "cc", "e1", "3d", "b7", "16", "b6", "14", "c2", "28", "fb", "2c", "05"],
    ["2b", "67", "9a", "76", "2a", "be", "04", "c3", "aa", "44", "13", "26", "49", "86", "06", "99"],
    ["9c", "42", "50", "f4", "91", "ef", "98", "7a", "33", "54", "0b", "43", "ed", "cf", "ac", "62"],
    ["e4", "b3", "1c", "a9", "c9", "08", "e8", "95", "80", "df", "94", "fa", "75", "8f", "3f", "a6"],
    ["47", "07", "a7", "fc", "f3", "73", "17", "ba", "83", "59", "3c", "19", "e6", "85", "4f", "a8"],
    ["68", "6b", "81", "b2", "71", "64", "da", "8b", "f8", "eb", "0f", "4b", "70", "56", "9d", "35"],
    ["1e", "24", "0e", "5e", "63", "58", "d1", "a2", "25", "22", "7c", "3b", "01", "21", "78", "87"],
    ["d4", "00", "46", "57", "9f", "d3", "27", "52", "4c", "36", "02", "e7", "a0", "c4", "c8", "9e"],
    ["ea", "bf", "8a", "d2", "40", "c7", "38", "b5", "a3", "f7", "f2", "ce", "f9", "61", "15", "a1"],
    ["e0", "ae", "5d", "a4", "9b", "34", "1a", "55", "ad", "93", "32", "30", "f5", "8c", "b1", "e3"],
    ["1d", "f6", "e2", "2e", "82", "66", "ca", "60", "c0", "29", "23", "ab", "0d", "53", "4e", "6f"],
    ["d5", "db", "37", "45", "de", "fd", "8e", "2f", "03", "ff", "6a", "72", "6d", "6c", "5b", "51"],
    ["8d", "1b", "af", "92", "bb", "dd", "bc", "7f", "11", "d9", "5c", "41", "1f", "10", "5a", "d8"],
    ["0a", "c1", "31", "88", "a5", "cd", "7b", "bd", "2d", "74", "d0", "12", "b8", "e5", "b4", "b0"],
    ["89", "69", "97", "4a", "0c", "96", "77", "7e", "65", "b9", "f1", "09", "c5", "6e", "c6", "84"],
    ["18", "f0", "7d", "ec", "3a", "dc", "4d", "20", "79", "ee", "5f", "3e", "d7", "cb", "39", "48"]]
# FK常数
FK: list[int] = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
# CK常数
CK: list[int] = [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
                 0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
                 0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
                 0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]


class SM4:
    """
    SM4类
    """

    def __init__(self, key: HEXSTR) -> None:
        """
        SM4初始化
        :param key: 原始密钥（32hex）
        """
        if type_check(key, HEXSTR):
            pass
        if len(key) != 34:
            raise ValueError("SM4:length of key must be 32 hex(128 bit)!")
        self.ori_key = key[2:]
        self.r_key = []

    def gen_round_key(self) -> list[str]:
        """
        轮密钥生成
        :return rk:轮密钥
        """
        MK = self.ori_key
        MK = [MK[8 * i:8 * (i + 1)] for i in range(4)]
        w = [f"{int(MK[i], 16) ^ FK[i]:08x}" for i in range(4)]
        for i in range(32):
            ck_res = f"{int(w[i + 1], 16) ^ int(w[i + 2], 16) ^ int(w[i + 3], 16) ^ CK[i]:08x}"
            t_k_res = self.__T_func(ck_res, T_flag)
            w.append(f"{int(w[i], 16) ^ int(t_k_res, 16):08x}")
        rk = w[4:]
        return rk

    @staticmethod
    def __T_func(xor_result: str, T_state: int = 0) -> str:
        """
        合成置换T
        :param xor_result: 异或结果
        :param T_state: 区分密钥/普通模式
        :return l_res: 合成置换T的结果
        """
        if type_check(xor_result, str) and type_check(T_state, int):
            pass
        s_res, l_res = [], ""
        for i in range(4):
            x, y = int(xor_result[2 * i:2 * (i + 1)][0], 16), int(xor_result[2 * i:2 * (i + 1)][1], 16)
            s_res.append(S[x][y])
        s_res = int("".join(s_res), 16)
        if T_state == 1:
            l_res = f"{s_res ^ rot_shift(s_res, 13, 32) ^ rot_shift(s_res, 23, 32):08x}"
        else:
            l_res = f"{s_res ^ rot_shift(s_res, 2, 32) ^ rot_shift(s_res, 10, 32) ^ rot_shift(s_res, 18, 32) ^ rot_shift(s_res, 24, 32):08x}"
        return l_res

    def __feistel(self, pre: str) -> str:
        """
        SM4非平衡feistel结果
        :param pre:待加/解密字符串
        :return ans: 明密文字符串
        """
        if type_check(pre, str):
            pass
        pre = pre[2:]
        last = [pre[8 * i:8 * (i + 1)] for i in range(4)]
        for i in range(32):
            xor_res = f"{int(last[i + 1], 16) ^ int(last[i + 2], 16) ^ int(last[i + 3], 16) ^ int(self.r_key[i], 16):08x}"
            T_res = self.__T_func(xor_res)
            last.append(f"{int(last[i], 16) ^ int(T_res, 16):08x}")
        ans = "".join(["0x", last[35], last[34], last[33], last[32]])
        return ans

    def encrypt(self, message: bytes) -> bytes:
        """
        加密函数
        :param message: 明文字符串
        :return :密文字符串
        """
        if type_check(message, bytes):
            pass
        self.r_key = self.gen_round_key()
        return hex2byte(self.__feistel(byte2hex(message, 32)), 16)

    def decrypt(self, cipher: bytes) -> bytes:
        """
        解密函数
        :param cipher: 密文字符串
        :return: 明文字符串
        """
        if type_check(cipher, bytes):
            pass
        self.r_key = self.gen_round_key()[::-1]
        return hex2byte(self.__feistel(byte2hex(cipher, 32)), 16)

    def ECB(self, byte_stm: bytes, mode: TYPESM4) -> bytes:
        """
        SM4-ECB模式
        :param byte_stm: 字节流
        :param mode: 加解密模式
        :return out: 处理后字符串
        """
        if type_check(byte_stm, bytes) and type_check(mode, TYPESM4):
            pass
        stm = byte2hex(byte_stm, len(byte_stm) * 2)[2:]
        out = []
        if mode == ENCRYPT:  # 加密
            num_pad = 16 - len(stm) % 32 // 2
            stm += num_pad * f"{num_pad:02x}"
            t = len(stm) // 32
            stm_lst = ["0x" + stm[32 * i:32 * (i + 1)] for i in range(t)]
            for i in range(t):
                out.append(self.encrypt(hex2byte(stm_lst[i], 16)))
        if mode == DECRYPT:  # 解密
            t = len(stm) // 32
            stm_lst = ["0x" + stm[32 * i:32 * (i + 1)] for i in range(t)]
            for i in range(t):
                out.append(byte2hex(self.decrypt(hex2byte(stm_lst[i], 16)), 32))
            last = int(out[t - 1][32:], 16)
            out[t - 1] = out[t - 1][:34 - last * 2]
            out = [hex2byte(x, (len(x) - 2)//2) for x in out if x != '']
        return b"".join(out)

    def CBC(self, byte_stm: bytes, iv: HEXSTR, mode: TYPESM4) -> bytes:
        """
        SM4-CBC模式
        :param byte_stm: 字节流
        :param iv: 初始变量
        :param mode: 加解密模式选择
        :return: 处理后字符串
        """
        if type_check(byte_stm, bytes) and type_check(iv, HEXSTR) and type_check(mode, TYPESM4):
            pass
        stm = byte2hex(byte_stm, len(byte_stm) * 2)[2:]
        out = []
        if mode == 1:  # 加密
            out.append(iv[2:])
            num_pad = 16 - len(stm) % 32 // 2
            stm += num_pad * f"{num_pad:02x}"
            t = len(stm) // 32
            stm_lst = [stm[32 * i:32 * (i + 1)] for i in range(t)]
            for i in range(t):
                xor = f"0x{int(out[i], 16) ^ int(stm_lst[i], 16):032x}"
                out.append(byte2hex(self.encrypt(hex2byte(xor, 16)), 32)[2:])
            out = out[1:]
        else:  # 解密
            t = len(stm) // 32
            stm_lst = ["0x" + stm[32 * i:32 * (i + 1)] for i in range(t)]
            stm_lst.insert(0, iv)
            for i in range(t):
                d = self.decrypt(hex2byte(stm_lst[i + 1], 16))
                xor = f"{byte2int(d) ^ int(stm_lst[i], 16):032x}"
                out.append(xor)
            last = int(out[t - 1][30:], 16)
            out[t - 1] = out[t - 1][:32 - last * 2]
        h = "0x" + "".join(out)
        return hex2byte(h, (len(h) - 2) // 2)

    def file_process_bmp(self, filename: str, workMode: TYPESM4, cryptMode: TYPESM4, *args: HEXSTR) -> None:
        """
        bmp文件加解密
        :param filename: 文件名
        :param workMode: 工作模式选择
        :param cryptMode: 加解密选择
        :return:
        """
        name, ext = os.path.splitext(filename)
        with open(filename, "rb") as file, open(name + f"_{'ECB' if workMode == MODEECB else 'CBC'}" + ext, "wb") as outfile:
            outfile.write(file.read(54))
            data = file.read()
            if workMode == MODEECB:
                ecb_data = self.ECB(data, cryptMode)
                outfile.write(ecb_data)
            if workMode == MODECBC:
                iv = args[0]
                cbc_data = self.CBC(data, iv, cryptMode)
                outfile.write(cbc_data)
        print(f'SM4:the file {filename} is {"encrypted" if ENCRYPT else "decrypted"} by {"ECB" if workMode == MODEECB else "CBC"}!')


if __name__ == "__main__":
    pass
