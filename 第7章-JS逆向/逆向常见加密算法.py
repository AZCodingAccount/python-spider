from hashlib import md5, sha1, sha256

from urllib.parse import urlencode, unquote, quote

import base64

"""
            在这个文件中，介绍一下JS逆向中常见的加密算法，分别是摘要算法MD5(salt)，sha1，sha256和URLEncode、Base64、对称加密AES和DES、非对称加密RSA。
        在理解加密的时候，加密算法越复杂性能就越差，因此还是有很多仅仅使用MD5算法或MD5+salt算法
        摘要算法不存在解密的逻辑，本身就是散列直接做的摘要。URLEncode和Base64是转换的，可以直接还原原文。
"""

# TODO:MD5是一个不可逆的摘要算法，特点是速度快，并且非常难被破解，原本是128位二进制字符串，后来为了表示方便，一般显示的都是16进制的32位。（存在MD5相同的可能性）
# # 创建md5对象
# obj = md5("张狗蛋".encode("utf-8"))
# obj.update("非常帅".encode("utf-8"))  # 添加加密的内容
# md5_encrypt_data = obj.hexdigest()  # 生成16进制的md5摘要
# print(md5_encrypt_data)

# 网上有很多穷举出来md5的网站，如https://www.cmd5.com/。我们可以加盐让md5穷举（撞库）不出来。
# # 这个的实现原理就是直接在后面拼接。之前那个字符串还需要付费，现在这个它就撞不出来了。常见搭配时间戳+原始数据+非常大串的自定义字符串
# salt = "我是张狗蛋非常帅的盐"
# obj=md5(salt.encode("utf-8"))
# obj.update("张狗蛋非常帅".encode("utf-8"))
# md5salt_encrypt_data = obj.hexdigest()
# print(md5salt_encrypt_data)

# TODO:sha1算法和sha256算法。sha1和sha256可以认为是md5的升级版。sha1被证实会发生碰撞。（长度为40位）sha256是sha1的升级版，产生64位16进制数。
#  sha系列（最大加密长度为2^64位）
# # 调用起来都是一样的
# sha = sha256("张狗蛋非常帅".encode("utf-8"))
# sha256_encrypt_data=sha.hexdigest()
# print(sha256_encrypt_data)

# TODO：URLEncode。
"""
    这个编码是为了防止URL在传输过程中出现歧义或URL注入问题。将汉字转换成字节，一个字节转换成两个16进制并在前面加上%分割。默认采用UTF-8
"""
# base_url = "https://www.bugdesigner.cn/?"
# params = {
#     "s": "实用资源"
# }
# url = base_url + urlencode(params)
# print(url)
# 也可以对单个字符串进行编码或解码
# print(quote("张狗蛋"))
# print(unquote("%E5%BC%A0%E7%8B%97%E8%9B%8B"))

# TODO:Base64。Base64是一种将二进制转换为字符串的方式，可以方便在互联网上传播。它的数据量会增加1/3左右
"""
        Base64的编码方式是首先二进制数据按照字节分组，接下来这些字节按照每组6位分组，接着每组将会映射到Base64表中的一个字符，这个表包含了64个字符分别是
    26个大写字母+26个小写字母+10个数字+2个特殊符号(+和/)。！！！注意。如果最后组不满6位，则会填充=，最后的字符串不是4的倍数会报错，这个时候需要自己手动填充
"""

# bs = "张狗蛋非常帅A".encode("utf-8")  # 转换成字节
# print(base64.b64encode(bs).decode())  # 将字节数据转换成base64格式的。注意这里就会填充两个==，因为最后总字节数/6余2
#
# b64_encode_data = "5byg54uX6JuL6Z2e5bi45biFQQ=="
# print(base64.b64decode(b64_encode_data).decode())  # 将b64字符串解码，decode是为了从字节变成默认的中文。注意这里如果缺少=会报错，这里填充上=号就好了

# TODO:对称加密AES，DES