import math
import random
import time
import uuid


# 生成uuid
def gen_uuid():
    uuid_sec = str(uuid.uuid4())
    time_sec = str(int(time.time() * 1000 % 1e5)).rjust(5, "0")
    return f"{uuid_sec}{time_sec}infoc"


# 生成b_lsid
def gen_b_lsid():
    data = ""
    for i in range(8):
        v1 = math.ceil(16 * random.uniform(0, 1))
        v2 = hex(v1)[2:].upper()
        data += v2
    result = data.rjust(8, "0")

    e = int(time.time() * 1000)
    t = hex(e)[2:].upper()

    b_lsid = f"{result}_{t}"
    return b_lsid
