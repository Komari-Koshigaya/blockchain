#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author :        NIEJUN 
# Datetime：      2020.1.11 16:16
# IDE:            PyCharm
# File Name：     BlockChain.py
# DESCRIP：       BlockChain 类负责管理链式数据，他会存储交易并添加新的区块到链式数据的method
import hashlib
import json
from time import time
import logging
from urllib.parse import urlparse, quote
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)  # 创建创世区块
        self.nodes = set()  # use set to store node in order to avoiding duplicate

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        logging.debug('register_node -- parsed_url: ' + str(parsed_url) + ' , parsed_url.netloc: ' + parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid by checking all block's proof and previous_hash
        :param chain: <list> A blockchain
        :return: <bool> True if valid or False
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            logging.debug('last_block : ' + f'{last_block}' + ' ,block : ' + f'{block}' + '\n-----------\n')
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            logging.debug('向临近节点查询，若比自己的链长则更新，查询的url： ' + response.url)

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def new_block(self, proof, previous_hash=None):
        """
        add a new block into the BlockChain
        :param proof: <int> work proof that generated by proof-of-work
        :param previous_hash: (optional) <str> hash of previous block
        :return: <dict> new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(round(time() * 1000)),   # unix时间戳
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []  # reset current transaction record

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount
        :return <int> the index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        simple proof of work algorithm:
        -find a number p' usch that hsh(pp') contains leading 4zeroes, where p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        start = time()
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        logging.debug('工作量证明用时 ' + str(time() - start) + ' , 工作量是 -- ' + str(proof))
        return proof

    @property  # @property装饰器，将一个方法变成属性调用 外部可以直接 BlockChain.last_block访问
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]

    @staticmethod  # 静态方法，可以不用实例化，通过 class.function()，但是在该函数内调用类的其他方法无法直接调用,只能直接类名.属性名或类名.方法名
    def hash(block):
        """
        hash a block
        :param block: <dict> block
        :return: <str> hash160 of block
        """
        # 我们必须确保这个字典（区块）是经过排序的，否则我们将会得到不一致的散列
        block_string = json.dumps(block, sort_keys=True).encode()
        logging.debug('执行hash函数， block_string = json.dumps(block, sort_keys=True).encode() --' + str(block_string)
                      + '\n返回值是 -- ' + hashlib.sha256(block_string).hexdigest())
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> true if correct, or false
        """
        guess = f'{last_proof}{proof}'.encode()  # f'0{name}' 作用是格式化字符串，若name=ni，则结果是 0ni
        guess_hash = hashlib.sha256(guess).hexdigest()  # 进行hash计算时 必须现将字符编码成 二进制
        return guess_hash[:4] == '0000'
