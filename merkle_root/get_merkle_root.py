# 从交易列表中两两计算得到默克尔树根
# 交易数量不止一笔且数量位奇数时，会复制最后一笔交易，从而凑成偶数；注意不是直接使用最后一笔的交易哈希
# 只有一笔币基交易的默克尔树根就是币基交易的交易哈希
# 时间复杂度 O(nlogn)


import hashlib
import codecs

def merkle_tree(txs_hash):
    length = len(txs_hash)
    if length == 1:
        return txs_hash[0]

    new_list = []
    # len(txs_hash)-1为列表末尾数的下标
    
    for i in range(0, length, 2):
        # print(i, " index: ", txs_hash[i], "\n")
        if (i == length - 1):
            new_list.append(merkle_hash(txs_hash[i], txs_hash[i]))
        else:
            new_list.append(merkle_hash(txs_hash[i], txs_hash[i + 1]))


    return merkle_tree(new_list)

def merkle_hash(a, b):
    merge_hex_str = hashlib.sha256(hashlib.sha256(a + b).digest()).digest()
    return merge_hex_str




# toLittleEdianTxs 将交易哈希字符串 转成16进制小端序列
def to_little_edian_txs(txs):
    new_txs = []
    for i in range(0, len(txs)):
        hex_str = codecs.getdecoder('hex')(txs[i].encode())[0][::-1]
        new_txs.append(hex_str)
    # print("new_txs: ", new_txs, " len: ", len(new_txs))
    return new_txs


def cal_merkle_root(txs_hash):
    if len(txs_hash) < 1:
        return "illegal txs"
    if len(txs_hash) == 1:
        return txs_hash[0]

    little_edian_txs = to_little_edian_txs(txs_hash)
    root_hex = merkle_tree(little_edian_txs)
    root_str = codecs.getencoder('hex_codec')(root_hex[::-1])[0]
    return root_str.decode()


def cal_merkle_root_test():
    cases = [
        {
            "txs": [
                "b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082",
                "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"
            ],
            "root": "7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff"
        },
        {
            "txs": [
                "8347cee4a1cb5ad1bb0d92e86e6612dbf6cfc7649c9964f210d4069b426e720a",
                "a16f3ce4dd5deb92d98ef5cf8afeaf0775ebca408f708b2146c4fb42b41e14be"
            ],
            "root": "ed92b1db0b3e998c0a4351ee3f825fd5ac6571ce50c050b4b45df015092a6c36"
        },
        {
            "txs": [
                "09e5c4a5a089928bbe368cd0f2b09abafb3ebf328cd0d262d06ec35bdda1077f",
                "591e91f809d716912ca1d4a9295e70c3e78bab077683f79350f101da64588073"
            ],
            "root": "2f0f017f1991a1393798ff851bfc02ce7ba3f5e066815ed3104afb4bd3a0c230"
        },
        {
            "txs": [
                "8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87",
                "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4",
                "6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4",
                "e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d"
            ],
            "root": "f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766"
        },
        {
            "txs": [
                "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
            ],
            "root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
        },
        {
            "txs": [
                "ef1d870d24c85b89d92ad50f4631026f585d6a34e972eaf427475e5d60acf3a3",
                "f9fc751cb7dc372406a9f8d738d5e6f8f63bab71986a39cf36ee70ee17036d07",
                "db60fb93d736894ed0b86cb92548920a3fe8310dd19b0da7ad97e48725e1e12e",
                "220ebc64e21abece964927322cba69180ed853bb187fbc6923bac7d010b9d87a",
                "71b3dbaca67e9f9189dad3617138c19725ab541ef0b49c05a94913e9f28e3f4e",
                "fe305e1ed08212d76161d853222048eea1f34af42ea0e197896a269fbf8dc2e0",
                "21d2eb195736af2a40d42107e6abd59c97eb6cffd4a5a7a7709e86590ae61987",
                "dd1fd2a6fc16404faf339881a90adbde7f4f728691ac62e8f168809cdfae1053",
                "74d681e0e03bafa802c8aa084379aa98d9fcd632ddc2ed9782b586ec87451f20"
            ],
            "root": "2fda58e5959b0ee53c5253da9b9f3c0c739422ae04946966991cf55895287552"
        }
    ]

    for i in range(0, len(cases)): 
        data = cases[i]
        cal_root = cal_merkle_root(data["txs"])
        print("index: ", i, ", merkle_root: ", cal_root, ", equals: ", cal_root == data["root"], "\n")

if __name__ == '__main__':
    # txs = [
    #     "09e5c4a5a089928bbe368cd0f2b09abafb3ebf328cd0d262d06ec35bdda1077f",
    #     "591e91f809d716912ca1d4a9295e70c3e78bab077683f79350f101da64588073"
    # ]
    # ori_root = "2f0f017f1991a1393798ff851bfc02ce7ba3f5e066815ed3104afb4bd3a0c230"

    # cal_root = cal_merkle_root(txs)
    # print("merkle_root: ", cal_root, ", equals: ", ori_root == cal_root)

    cal_merkle_root_test()


