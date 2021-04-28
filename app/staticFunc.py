import datetime
import json
import random
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from app import models
from app.obj.User import User


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


def getUserId(cookie):
    ans = User(cookie).getProfileInfo(whole=False)
    if ans['validation']:
        return {"validation": True, "uid": ans['id']}
    else:
        return {"validation": False, "mes": "invalid user"}


def payMoney(cookie, amount, password):
    ans = User(cookie).payMoney(amount=amount, password=password)
    return ans


# def findOrders(viewId):
#     query1 = models.OrderInfo.objects.filter(customerId=viewId)
#     query2 = models.GoodsInfo.objects.filter(sellerId=viewId)
#     orderIdList = []
#     for i in query1:
#         orderIdList.append(i.id)
#     for i in query2:
#         query3 = models.OrderInfo.objects.filter(goodsId=i)
#         for j in query3:
#             orderIdList.append(j.id)
#     return orderIdList

def findInfo(viewId):
    query1 = models.OrderInfo.objects.filter(customerId=viewId)
    query2 = models.GoodsInfo.objects.filter(sellerId=viewId)
    orderList = []
    goodsList = []
    for i in query1:
        if i.removal:
            continue
        data = {"id": i.id, "name": i.goodsId.name, "identity": "customer", "status": ""}
        if i.finished and i.paid:
            data["status"] = "finished"
        elif not i.finished and i.paid:
            data["status"] = "not receive"
        elif not i.finished and not i.paid:
            data["status"] = "unpaid"
        else:
            data["status"] = "Error"
        orderList.append(data)
    for i in query2:
        query3 = models.OrderInfo.objects.filter(goodsId=i.id)
        show = ""
        if i.show:
            show = "show"
        else:
            show = "not show"
        goodsList.append(
            {"id": i.id, "name": i.name, "category": i.categoryID.name, "status": show})
        for j in query3:
            if j.removal:
                continue
            data = {"id": j.id, "name": j.goodsId.name, "identity": "seller", "status": ""}
            if j.finished and j.paid:
                data["status"] = "finished"
            elif not j.finished and j.paid:
                data["status"] = "not receive"
            elif not j.finished and not j.paid:
                data["status"] = "unpaid"
            else:
                data["status"] = "Error"
            orderList.append(data)
    return goodsList, orderList
