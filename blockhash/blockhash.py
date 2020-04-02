#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author :        NIEJUN 
# Datetime：      2020.4.2 17:06
# IDE:            PyCharm
# File Name：     blockhash.py
# DESCRIP：       python3版本bitcoin计算block hash， 参考连接 https://www.jianshu.com/p/4187a7352769 只有python2版本
#                先把 version prev_block mrkl_root time bits nonce当做字符串合并到一起, 得到结果 result. 得到 result 后,
#                做2次 sha256运算, 得到 hash, 再然后hash 做大小端转换, 最后的结果就是这个block的hash.
#                不过 version time bits nonce 要转换为 unsigned long型小字端, prev_block mrkl_root 要转换为16进制并大小端转换,

import hashlib  # 用于计算hash
import struct  # 本项目用于将int 转成 unsigned long,并小端对齐
import codecs  # 由于 'hello'.encode("hex") 只适用python2，故python3使用该库

# 以下信息来源 https://blockchain.info/rawblock/000000000000000000003306eff4d5ac9f94a69507c4fd3348107af23de3dfcc
# 网页打开第一行即可获得确切的ver 和 time bitx 和nonce(这四个皆是10进制，默认大端对齐)
# 打开 https://btc.com/000000000000000000003306eff4d5ac9f94a69507c4fd3348107af23de3dfcc 即可看到前个区块的hash和本区块的梅克尔树根
ver = 1073733632      # version 即网络节点的版本号
prev_block = "0000000000000000000eb14190ce1867332bac3520af691e76547386269929fa"   #  前一个块的hash,创世块没有,以后的块都有
mrkl_root = "e67eae842181145ac8ac48ab1057b5d497886bbe606ce8924f61faac98e025ab"
time = 1585832466         # utc时间戳
bits = 387201857          # 网络的难度
nonce = 2518273408        # 随机数，也就是 Pow 要计算的随机量

# "abced"[::-1] 代表原字符串倒序输出；[:-1]代表去字符串 0-倒数第一个数 左闭右开；[-1]代表取字符串最后一个数
# prev_block.encode() 将字符串转成字节， codecs.getdecoder('hex')(prev_block.encode())[0]将字节编码成16进制字符串
after_prev_block = codecs.getdecoder('hex')(prev_block.encode())[0][::-1]
#  after_prev_block: '\xfa)\x99&\x86sTv\x1ei\xaf 5\xac+3g\x18\xce\x90A\xb1\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00'
after_mrkl_root = codecs.getdecoder('hex')(mrkl_root.encode())[0][::-1]
# after_mrkl_root：  ‘\xab%\xe0\x98\xac\xfaaO\x92\xe8l`\xbek\x88\x97\xd4\xb5W\x10\xabH\xac\xc8Z\x14\x81!\x84\xae~\xe6'
#  struct.pack("<L", ver) 中<代表小端对齐，L代表unsigned long  将版本ver转成小端对齐无符号长整型，再转成 16进制字符串
# 最后结果为 '\x00\xe0\xff?'

hex_str = struct.pack("<L", ver) + after_prev_block +\
          after_mrkl_root + struct.pack("<LLL", time, bits, nonce)

hash_str = hashlib.sha256(hashlib.sha256(hex_str).digest()).digest()  # 对16进制字符串进行2次 sha256，返回的是小段对其的 16进制字节
block_hash = codecs.getencoder('hex_codec')(hash_str[::-1])[0]  # 将 hash 结果转成 大端对齐，并按 字符串编码成 0000000330
# block_hash: '000000000000000000003306eff4d5ac9f94a69507c4fd3348107af23de3dfcc'  本区块的hash
print(hex_str, "\n", hash_str, " \n", "\n", block_hash, "\n",)

