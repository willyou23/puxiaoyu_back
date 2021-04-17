import datetime
import json
import random
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse


def get_random_number_str(length):
    """
    生成随机数字字符串
    :param length: 字符串长度
    :return:
    """
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str


def processImg(pic, id):
    im_pic = Image.open(pic)
    w, h = im_pic.size
    if w >= h:
        w_start = (w - h) * 0.618
        box = (w_start, 0, w_start + h, h)
        region = im_pic.crop(box)
    else:
        h_start = (h - w) * 0.618
        box = (0, h_start, w, h_start + w)
        region = im_pic.crop(box)
    # region就是PIL处理后的正方形了
    #  先保存到磁盘io
    pic_io = BytesIO()
    region.save(pic_io, im_pic.format)
    # 再转化为InMemoryUploadedFile数据
    pic_file = InMemoryUploadedFile(
        file=pic_io,
        field_name=None,
        name=id + get_random_number_str(10) + '.' + pic.name.split('.')[-1],
        content_type=pic.content_type,
        size=pic.size,
        charset=None
    )
    return pic_file


def JsonPackage(targetDict):
    return JsonResponse(json.dumps(targetDict), safe=False)
