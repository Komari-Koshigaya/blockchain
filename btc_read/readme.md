#### **本次实验主要是区块链的读取操作，包括获取当前最新区块高度，获取指定高度的区块信息，获取指定hash的交易详情**
区块链的读取实验，最简单的方法是在各种比特币浏览器上查看，
这里我们用代码来实现这些功能，但其实也是调用了比特币浏览器的公开 api 实现的
实验中使用的是 blockchain 提供的api，api详情见 https://github.com/blockchain/api-v1-client-python/blob/master/docs/blockexplorer.md
实验前需要先安装第三方库 pip install blockchain
PS: 由于是外国网站，请求较慢，需要等待2-3秒

`from blockchain import blockexplorer`

### **1、获取当前最新区块**
`latest_block = blockexplorer.get_latest_block()`

### **2、获取指定高度的区块信息**

`blocks = blockexplorer.get_block_height(2570)
`
### **3、获取指定hash的区块信息**
`block = blockexplorer.get_block('000000000000000016f9a2c3e0f4c1245ff24856a79c34806969f5084f410680')
`
### **4、获取指定hash的交易详情**
`tx = get_tx('6d0419dc865d3f986130051208804c24ab45de4790eceb4d405087f14ad34c72')
`
### **5.查询账户地址的历史记录，如 可用余额、相关的交易数**
`block_addr = get_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd')
`
### **6.查看当前区块链上未确认的交易**
`txs_unconfirmed = get_unconfirmed_tx()
`
