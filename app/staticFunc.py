import datetime
import random


def get_random_number_str(length):
    """
    生成随机数字字符串
    :param length: 字符串长度
    :return:
    """
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str
