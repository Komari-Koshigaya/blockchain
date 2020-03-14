#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author :        NIEJUN 
# Datetime：      2020.1.9 21:01
# IDE:            PyCharm
# File Name：     read_test.py
# DESCRIP：       
from blockchain.blockexplorer import *
import time
import requests
import json

#   查看区块
# 1.查看最新区块
# latest_block = get_latest_block()
# print('最近区块高度： ' + str(latest_block.height) + ' ,产生时间： ' + time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(latest_block.time))
#       + ' ,hash： ' + str(latest_block.hash))

# # 2.根据区块的hash查看区块
# block = get_block('000000000000000000124068439cb30bfc401d12f37d29b4f7eacd8115365655')  # 根据区块 hash 查询区块
# print('该区块的高度是： ' + str(block.height) + " ,是否是主链 " + str(block.main_chain) + " ,merkle root: " + block.merkle_root
#       + ' ,交易数量：' + str(block.n_tx) + ' ,交易费是(BTC)：' + str(block.fee/100000000.0) + ' ,大小(bytes)：' + str(block.size))
#       

# # 3. 查看交易
tx = get_tx('6d0419dc865d3f986130051208804c24ab45de4790eceb4d405087f14ad34c72')  # 根据交易的 hash 查询交易
# tx.time得到的是时间戳，即格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数
print(tx.hash + '该交易发生的时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(tx.time)) + ' ,所在区块高度是：' + str(
    tx.block_height) + ' ,交易的确认数：' + str(tx.tx_index) + ' ,交易的输入个数：' + str(tx.inputs.__len__())
    + ' ,交易的输出个数：' + str(tx.outputs.__len__()))  # 高度为-1代表未确认


# 4. 查询账户地址的历史记录，如 可用余额、相关的交易数
block_addr = get_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd')
print('账户地址:' + block_addr.address + ',余额： ' + str(block_addr.final_balance / 100000000.0)
      + ' BTC,相关的交易数：' + str(block_addr.n_tx))

# 5. 查看当前区块链上未确认的交易
txs_unconfirmed = get_unconfirmed_tx()
print('当前未确认交易数： ' + str(len(txs_unconfirmed)))

