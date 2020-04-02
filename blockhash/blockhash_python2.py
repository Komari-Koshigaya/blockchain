#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author :        NIEJUN 
# Datetime：      2020.4.2 17:06
# IDE:            PyCharm
# File Name：     blockhash.py
# DESCRIP：       python2版本bitcoin计算block hash， 参考连接 https://www.jianshu.com/p/4187a7352769 只有python2版本
#                先把 version prev_block mrkl_root time bits nonce当做字符串合并到一起, 得到结果 result. 得到 result 后,
#                做2次 sha256运算, 得到 hash, 再然后hash 做大小端转换, 最后的结果就是这个block的hash.
#                不过 version time bits nonce 要转换为 unsigned long型小字端, prev_block mrkl_root 要转换为16进制并大小端转换,

import hashlib  # 用于计算hash
import struct  # 本项目用于将int 转成 unsigned long,并小端对齐

# 以下信息来源 https://blockchain.info/rawblock/000000000000000000003306eff4d5ac9f94a69507c4fd3348107af23de3dfcc
# 网页打开第一行即可获得确切的ver 和 time bitx 和nonce(这四个皆是10进制，默认大端对齐)
# 打开 https://btc.com/000000000000000000003306eff4d5ac9f94a69507c4fd3348107af23de3dfcc 即可看到前个区块的hash和本区块的梅克尔树根
ver = 1073733632      # version 即网络节点的版本号
prev_block = "0000000000000000000eb14190ce1867332bac3520af691e76547386269929fa"   #  前一个块的hash,创世块没有,以后的块都有
mrkl_root = "e67eae842181145ac8ac48ab1057b5d497886bbe606ce8924f61faac98e025ab"
time = 1585832466         # utc时间戳
bits = 387201857          # 网络的难度
nonce = 2518273408        # 随机数，也就是 Pow 要计算的随机量

hex_str = struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +\
  mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time, bits, nonce)

hash_str = hashlib.sha256(hashlib.sha256(hex_str).digest()).digest()
# 这就是bitcoin矿机的工作 , 找到一个合适的nonce
# 使得做2次sha256运算的结果符合某个条件

block_hash = hash_str[::-1].encode('hex_codec')
print(mrkl_root.decode('hex')[::-1], "\n")
print(hex_str, hash_str)
print(block_hash + "\n" + prev_block + "\n")

