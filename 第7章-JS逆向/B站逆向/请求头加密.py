import hashlib
import json
import struct



# 获取秘钥
def get_secret_key(res):
    # print(json.loads(res.text)['data']['wbi_img']['img_url'], json.loads(res.text)['data']['wbi_img']['sub_url'])
    t = json.loads(res.text)['data']['wbi_img']['img_url']
    r = json.loads(res.text)['data']['wbi_img']['sub_url']
    # 提取 t 和 r 中的特定部分
    t_extracted = t[t.rfind('/') + 1:].split('.')[0]
    r_extracted = r[r.rfind('/') + 1:].split('.')[0]

    # 拼接 t 和 r 的提取部分
    e = t_extracted + r_extracted

    # 定义索引数组
    indices = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14,
               39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59,
               6, 63, 57, 62, 11, 36, 20, 34, 44, 52]

    # 根据索引数组提取字符并拼接
    result = ''.join(e[i] for i in indices if i < len(e))

    # 截取前 32 个字符
    return result[:32]


def s(input_string):
    """
    计算字符串的 MD5 散列，并返回四个整数值组成的数组。
    """
    md5_hash = hashlib.md5(input_string.encode())
    # 将 16 字节的 MD5 哈希分成四个 32 位的整数
    return list(struct.unpack('>4I', md5_hash.digest()))


def words_to_bytes(words):
    """
    将整数数组转换为字节序列。
    """
    # 每个整数转换为 4 字节
    return [byte for word in words for byte in struct.pack('>I', word)]


def convert_md5(input_string, as_bytes=False, as_string=False):
    """
    根据选项返回 MD5 哈希的不同表示。
    """
    # 计算 MD5 整数数组
    md5_words = s(input_string)

    if as_bytes:
        # 返回字节序列
        return words_to_bytes(md5_words)
    elif as_string:
        # 返回字符串表示（假设是 UTF-8 编码的字符串）
        return ''.join(chr(byte) for byte in words_to_bytes(md5_words))
    else:
        # 返回十六进制表示
        return ''.join(f'{word:08x}' for word in md5_words)


# 测试字符串
# 前面请求的
test_string = 'aid=325318514&cid=1381936481&web_location=1315873&wts=1703944676ea1db124af3c7062474693fa704f4ff8'
# 模拟的
test_string2 = 'w_aid=325318514&w_ftime=1703944675&w_part=1&w_stime=1703944674&w_type=3&web_location=1315873&wts=17039446769d86b01094b49f0347055bdfa8cb479f'
test_string3 = 'w_aid=325318514&w_ftime=1704012605&w_part=1&w_stime=1704012604&w_type=3&web_location=1315873&wts=17040126619d86b01094b49f0347055bdfa8cb479f'

# 测试函数
md5_as_bytes = convert_md5(test_string, as_bytes=True)
md5_as_string = convert_md5(test_string, as_string=True)
md5_as_hex = convert_md5(test_string2)

# 156c3c9ccf38bbe3e32c2a8481540e07
# 156c3c9ccf38bbe3e32c2a8481540e07
# print(md5_as_hex)
