#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from Crypto.Cipher import ARC4
import base64

def rc4_encrypt(data, key1):        # 加密
    key = bytes(key1, encoding='utf-8')
    enc = ARC4.new(key)
    res = enc.encrypt(data.encode('utf-8'))
    res=base64.b64encode(res)
    res = str(res,'utf-8')
    return res

def rc4_decrypt(data, key1):        # 解密
    data = base64.b64decode(data)
    key = bytes(key1, encoding='utf-8')
    enc = ARC4.new(key)
    res = enc.decrypt(data)
    res = str(res,'gbk')
    return res


if __name__ == "__main__":
    data = 'nihao'  # 需要加密的内容
    key = '123456'  # 加密key
    start_time = time.perf_counter()
    encrypt_data = rc4_encrypt(data,key)     # 加密方法
    print("S--- %s seconds ---" % (time.perf_counter() - start_time))
    print('加密后:',encrypt_data)
    print('解密后:',rc4_decrypt(encrypt_data, key))         # 解密方法

