import math
import base58
import hashlib
from . import keys
import json
import datetime

class Uint64:
    def __init__(self, exp=0):
        self.value = int(exp) % (2 ** 64)

    def __int__(self):
        return self.value

    def __str__(self):
        return hex(self.value)

    def __bytes__(self):
        return self.value.to_bytes(8, 'little')


class Name:
    def __init__(self, exp=0):
        try:
            self.value = int(exp)
            return None
        except:
            pass

        s = str(exp)

        # str -> name value
        self.value = 0

        if len(s) > 13:
            raise Exception("given string length is more than 13")

        if len(s) == 0:
            return None

        n = min(len(s), 12)

        for i in range(n):
            self.value <<= 5;
            self.value |= self.char_to_value(s[i])

        self.value <<= ( 4 + 5*(12 - n) )

        if len(s) == 13:
            v = self.char_to_value(s[12])
            if v > 15:
                raise Exception("thirteenth character in name cannot be a letter that comes after j")

            self.value |= v

        return None

    def __int__(self):
        return self.value

    def __str__(self):
        charmap = ".12345abcdefghijklmnopqrstuvwxyz"
        mask = int("f800000000000000", 16)
        s = ""
        v = self.value
        for i in range(13):
            if int(Uint64(v)) == 0:
                return s

            indx = (v & mask) >> (60 if i == 12 else 59)
            s += charmap[indx]
            v <<= 5

        return s;

    def __bytes__(self):
        return bytes(Uint64(self.value))

    def char_to_value(self, c):
        if c == '.':
            return 0
        elif '1' <= c <= '5':
            return ord(c) - ord('1') + 1
        elif 'a' <= c <= 'z':
            return ord(c) - ord('a') + 6
        else:
            raise Exception("character is not in allowed character set for names")


class SymbolCode:
    def __init__(self, exp=0):
        try:
            self.raw = int(exp)
            return None
        except:
            pass

        s = str(exp)

        # str -> symbol_code row
        self.raw = 0

        if len(s) > 7:
            raise Exception("string is too long to be a valid symbol_code")

        n = len(s)

        for i in range(n):
            c = s[n - i - 1]
            if c < 'A' or 'Z' < c:
                raise Exception("only uppercase letters allowed in symbol_code string")

            self.raw <<= 8
            self.raw |= ord(c)

    def __int__(self):
        return self.raw

    def __str__(self):
        mask = int("ff", 16)
        s = ""
        v = self.raw
        for i in range(7):
            if int(Uint64(v)) == 0:
                return s

            c = (v & mask) % 256;
            s += chr(c)
            v >>= 8

        return s

    def __bytes__(self):
        return bytes(Uint64(self.raw))


def public_key_to_bytes34(public_key):
    return b'\x00' + base58.b58decode(str(public_key).lstrip("EOS"))[0: -4]

