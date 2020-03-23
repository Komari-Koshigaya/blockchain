#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author :        NIEJUN 
# Datetime：      2020.1.11 17:16
# IDE:            PyCharm
# File Name：     app.py
# DESCRIP：       Flask 服务器 将扮演区块链网络中的一个节点
# Instantiate our Node（实例化我们的节点）
import json
from flask import Flask, jsonify, request
from blockchain import BlockChain
from uuid import uuid4  # 通用唯一标识库，用来生成空间和时间上的唯一标识
import logging
import hashlib

app = Flask(__name__)

# Generate a globally unique address for this node（为这个节点生成一个全球唯一的地址）
node_identifier = str(uuid4()).replace('-', '')  # 为节点创建一个随机的名称。

# Instantiate the Blockchain（实例化 Blockchain类）
BlockChain = BlockChain()
logging.basicConfig(level=logging.DEBUG)


@app.route('/mine', methods=['GET'])
def mine():
    logging.info("We'll mine a new Block")
    # We run the proof of work algorithm to get the next proof...
    last_block = BlockChain.last_block
    last_proof = last_block['proof']
    proof = BlockChain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    BlockChain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = BlockChain.hash(last_block)
    block = BlockChain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 202  # 使用 flask 库中的 jsonify() 将字符串序列化成json格式


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    用 postman 构造该请求的方法
    选 post 请求方式，在 body选择raw 右侧格式选择 json 在文本框中填入
    {
        "sender":"1Po1oWkD2LmodfkBYiAktwh76vkF93LKnh",
        "recipient": "someone-other-address",
        "amount": 100
    }
    headers选中content-type，将其值改为 application/json，而后点击 send 即可
    :return:
    """
    logging.debug("We'll add a new transaction")
    #  get_json 这个函数默认情况下只对 mime 为 application/json 的请求可以正确解析。否则获取到的将是 none
    # 所以解决办法是 http 请求增加 Content - Type: application / json header
    # 或者 使用 request.get_json(force=True) 忽略 mimetype
    values = request.get_json(force=True)
    logging.debug('获取的请求参数是' + str(request.json))
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = BlockChain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': BlockChain.chain,
        'length': len(BlockChain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/neighbour', methods=['get', 'post'])
def show_neighbor_nodes():
    response = {
        'message': 'ok',
        'neighbour_num': list(BlockChain.nodes).__len__(),
        'neighbour_nodes': list(BlockChain.nodes),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        BlockChain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_neighbour_nodes': list(BlockChain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = BlockChain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': BlockChain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': BlockChain.chain
        }
    return jsonify(response), 200


@app.route('/', methods=['get', 'post'])
def welcome():
    logging.debug(str(uuid4()) + ' ,uuid4.replace -- ' + str(uuid4()).replace('-', ''))
    return 'hello ' + str(uuid4()).replace('-', '') + ' ,welcome to BlockChain!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
