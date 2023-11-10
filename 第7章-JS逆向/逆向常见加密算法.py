# 导入摘要算法
import binascii
from hashlib import md5, sha1, sha256
# 导入URL
from urllib.parse import urlencode, unquote, quote
# 导入base64
import base64
# 导入对称加密相关模块
from Crypto.Cipher import AES, DES, DES3
from Crypto.Util.Padding import pad, unpad
# 导入非对称加密相关模块
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random

"""
            在这个文件中，介绍一下JS逆向中常见的加密算法，分别是摘要算法MD5(salt)，sha1，sha256和URLEncode、Base64、对称加密AES和DES、非对称加密RSA。
        在理解加密的时候，加密算法越复杂性能就越差，因此还是有很多仅仅使用MD5算法或MD5+salt算法
        摘要算法不存在解密的逻辑，本身就是散列直接做的摘要。URLEncode和Base64是转换的，可以直接还原原文。
"""

# TODO:MD5
"""
    MD5是一个不可逆的摘要算法，特点是速度快，并且非常难被破解，原本是128位二进制字符串，后来为了表示方便，一般显示的都是16进制的32位。（存在MD5相同的可能性）
"""
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
"""
    sha系列（最大加密长度为2^64位）
"""
# # 调用起来都是一样的
# sha = sha256("张狗蛋非常帅".encode("utf-8"))
# sha256_encrypt_data=sha.hexdigest()
# print(sha256_encrypt_data)

# TODO：URLEncode。
"""
    这个URL编码是为了防止URL在传输过程中出现歧义或URL注入问题。将汉字转换成字节，一个字节转换成两个16进制并在前面加上%分割。默认采用UTF-8
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
    / 换成_，+换成-（URLBase64变种，害怕对URL有影响）
"""

# bs = "张狗蛋非常帅A".encode("utf-8")  # 转换成字节
# print(base64.b64encode(bs).decode())  # 将字节数据转换成base64格式的。注意这里就会填充两个==，因为最后总字节数/6余2
#
# b64_encode_data = "5byg54uX6JuL6Z2e5bi45biFQQ=="
# print(base64.b64decode(b64_encode_data).decode())  # 将b64字符串解码，decode是为了从字节变成默认的中文。注意这里如果缺少=会报错，这里填充上=号就好了

# TODO:对称加密AES，DES
"""
        AES称为高级加密标准，通过加密秘钥的长度和加密轮数分为AES-128，AES-192,AES-256。但是加密的步骤是一模一样的。
    AES分为key，加密模式，IV(受加密模式影响)，pad这四个部分。
        key很简单，就是秘钥，是16位的字节。
        加密模式一般有CBC和ECB，CBC需要IV（初始向量），不同的IV加密出来的结果是不一样的，也是16位的字节
        pad是因为AES这个算法加密的数据需要是16的倍数，如果不是，那么就需要填充到16的倍数。
    逆向的时候需要找到key，mode和iv，一般都是CBC模式，因为安全性比较高
"""
# # 创建AES对象
# aes = AES.new(key=b"1234567890123456", IV=b'1234567890123456', mode=AES.MODE_CBC)
# ming = "张狗蛋很帅"
# # 添加填充，必须已经被编码成utf-8的形式了
# ming = pad(ming.encode("utf-8"), 16)
# aes_encrypt_data = aes.encrypt(ming)
# # print(aes_encrypt_data)
# # 一般加密完成以后会处理成字符串。
# str1 = base64.b64encode(aes_encrypt_data).decode()
# # print(str1)
# str2 = binascii.b2a_hex(aes_encrypt_data).decode()
# # print(str2)
#
# # 解密，假设之前加密的转换成字符串了
# aes_decrypt = AES.new(key=b"1234567890123456", IV=b'1234567890123456', mode=AES.MODE_CBC) # 这里一定得新创建一个AES
# mi = base64.b64decode(str1)
# aes_decrypt_data=aes_decrypt.decrypt(mi)
# aes_decrypt_data = unpad(aes_decrypt_data, 16)  #去掉填充
# print(aes_decrypt_data.decode())    #解码成字符串

"""
    DES是AES的降级版，所有步骤都跟AES一样，除了key和iv的填充从16个字节降低到了8个字节
"""
# # 加密
# des = DES.new(key=b'12345678', mode=DES.MODE_CBC, iv=b'12345678')
# data = "张狗蛋很帅"
# data = pad(data.encode("utf-8"), 16)  # 填充
# des_encrypt_data = des.encrypt(data)  # 加密
# des_encrypt_data = base64.b64encode(des_encrypt_data).decode()  # 处理成base64字符串
# print(des_encrypt_data)
#
# # 解密
# des_decrypt = DES.new(key=b'12345678', mode=DES.MODE_CBC, iv=b'12345678')  # 创建新的DES对象
# des_decrypt_data = des_decrypt.decrypt(base64.b64decode(des_encrypt_data))  # 解码成字节串
# des_decrypt_data = unpad(des_decrypt_data, 16)  # 去掉填充
# print(des_decrypt_data.decode())

# TODO:RSA
"""
        非对称加密常见的是RSA，非对称加密的原理是生成的时候有一个公钥还有一个私钥，数据被公钥加密只能被私钥解密，反之则不可以。原理是素数相乘。
    这里需要讨论PKCS（公钥密码学标准，具体也是根据加密数据是不是8的倍数进行填充，就不再深入讨论）。还有一个是没有填充的算法，这里py不能复现，必须使用JS。主要的流程为
    服务端生成一对公钥和私钥(必须同时生成)，加密的时候客户端使用公钥，并对数据进行填充，然后加密，解密的时候服务端找到私钥进行解密(公钥和私钥长度可以指定，一般是1024/2048)
"""
# # 创建私钥和公钥
# gen_random = Random.new  # 获取一个伪随机数生成器，用于最后解密时使用
# print(gen_random)
# rsa = RSA.generate(1024)
# with open('rsa.publickey.pem', mode='wb') as f:
#     f.write(rsa.public_key().exportKey())
# with open('rsa.privatekey.pem', mode='wb') as f:
#     f.write(rsa.exportKey())
#
# # 进行加密
# data = "张狗蛋很帅"
# with open("rsa.publickey.pem", mode='r') as f:
#     pk = f.read()
#     rsa_pk = RSA.importKey(pk)
#     rsa = PKCS1_v1_5.new(rsa_pk)  # 生成一个RSA对象
#
#     rsa_encrypt_data = rsa.encrypt(data.encode("utf-8"))  # 进行加密
#     b64_rsa_encrypt_data = base64.b64encode(rsa_encrypt_data).decode("utf-8")  # 处理成字符串格式
#     print(b64_rsa_encrypt_data)
# # 进行解密
# with open("rsa.privatekey.pem", mode='r') as f:
#     privatekey = f.read()
#     rsa_pk = RSA.importKey(privatekey)
#     rsa = PKCS1_v1_5.new(rsa_pk)
#
#     result = rsa.decrypt(base64.b64decode(b64_rsa_encrypt_data), gen_random)
#     print(result.decode("utf-8"))
