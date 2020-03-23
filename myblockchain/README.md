## MyBlockChain

------

> 该项目是用于创建个人区块链的学习工程，使用python语言，基于Flask框架写的api

### requirement

python 3.7、

install third libraries： requests 、urllib、 Flask

Postman： it is used to test api

### explain

blockchain.py 里面只有一个 BlockChain类负责管理链式数据

app.py 使用Flask服务器来扮演区块链网络中的一个节点，封装了一些api，包括 挖矿、创建新交易、获取当前区块链信息、查询附近节点

app2.py 与 app.py一致，只是修改了flask的运行端口，用于模拟其他节点

## run & test

运行 app.py 打开浏览器输入网址 http://localhost:5000/  或者 使用 postman构造get/post请求 http://localhost:5000/  即可看到 结果。

http://localhost:5000/mine  执行挖矿