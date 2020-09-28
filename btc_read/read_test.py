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


latest_block = get_latest_block()
print('最近区块高度： ' + str(latest_block.height) + ' ,产生时间： ' + time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(latest_block.time))
      + ' ,hash： ' + str(latest_block.hash))
#
# # 2.根据区块的hash查看区块
block = get_block('000000000000000000124068439cb30bfc401d12f37d29b4f7eacd8115365655')  # 根据区块 hash 查询区块
print('该区块的高度是： ' + str(block.height) + " ,是否是主链 " + str(block.main_chain) + " ,merkle root: " + block.merkle_root
      + ' ,交易数量：' + str(block.n_tx) + ' ,交易费是(BTC)：' + str(block.fee/100000000.0) + ' ,大小(bytes)：' + str(block.size))

# 3.根据区块的产生时间 、所在矿池 查看区块 ，返回的是区块列表
pool_blocks = get_blocks(time=1554888299 * 1000)
# pool_blocks = get_blocks(time=1554888299*1000, pool_name='UKRPool')
print('2019-04-10 17:24:59 挖出的区块个数是：' + str(len(pool_blocks)))

# 4.根据区块高度获取区块列表，此处返回列表是因为 区块链可能在此处产生分叉  如：525000、503888(BTC block、ETH block、BCH block)
# (请求过长 可能超时)
# blocks = get_block_height(503888)   #  等价于请求  https://blockchain.info/block-height/2570?format=json
# print(len(blocks))

# 查询账户地址的历史记录，如 可用余额、相关的交易数
block_addr = get_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd')
print('账户地址:' + block_addr.address + ',余额： ' + str(block_addr.final_balance / 100000000.0)
      + ' BTC,相关的交易数：' + str(block_addr.n_tx))

# 查看交易
tx = get_tx('6d0419dc865d3f986130051208804c24ab45de4790eceb4d405087f14ad34c72')  # 根据交易的 hash 查询交易
# 实际请求如下， BlockChain.blockexplorer 将请求和结果包装了  故访问更方便
# re_tx = requests.get('https://blockchain.info/rawtx/d851e7d1631a39055f14cc0707c22cdc9c7fd4f7cc84c8b4431b4bde70527fb7')
# tx.time得到的是时间戳，即格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数
print(tx.hash + '该交易发生的时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(tx.time)) + ' ,所在区块高度是：' + str(
    tx.block_height) + ' ,交易的确认数：' + str(tx.tx_index) + ' ,交易的输入个数：' + str(tx.inputs.__len__())
    + ' ,交易的输出个数：' + str(tx.outputs.__len__()))  # 高度为-1代表未确认

# 查看当前区块链上未确认的交易
txs_unconfirmed = get_unconfirmed_tx()
print('当前未确认交易数： ' + str(len(txs_unconfirmed)))

# BlockChain.info提供的接口请求太慢 以下是 btc.com 提供的接口，由于没有库，故需自己是使用requests库去请求
# re_block = requests.get('https://chain.api.btc.com/v3/block/3')
# block_json = json.loads(re_block.text)
# print(block_json["data"]["timestamp"])
# print('该交易发生的时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime(block_json["data"]["timestamp"])))
