import json
import os
from datetime import datetime
from uuid import uuid4

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from app import models, staticFunc
from app.obj.Goods import Goods
from app.obj.Order import Order
from app.obj.User import User
from app import models

# Create your views here.

# login view
from puxiaoyu_backend import settings


def login(request):
    username = request.POST.get('username')
    password = request.POST.get("password")
    return staticFunc.JsonPackage(User().login(username, password))


# createAccount view, accept a form info
def createAccount(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    question = request.POST.get('value')
    print(type(question))
    print(question)
    answer = request.POST.get('answer')
    print(answer)
    return staticFunc.JsonPackage(User().createAccount(username, email, password, question, answer))


def forgetPassword(request):
    question = request.POST.get('value')
    print(question)
    answer = request.POST.get('answer')
    print(answer)
    newpassword = request.POST.get('password')
    username = request.POST.get('username')
    return staticFunc.JsonPackage(User().forgetPassword(username, newpassword, question, answer))


# use cookie to get user information  and form the profile
def profileInfo(request):
    cookie = request.POST.get('cookie')
    whole = request.POST.get('whole')
    return staticFunc.JsonPackage(User(cookie=cookie).getProfileInfo(whole=whole))


# reset password view, compare old function firstly, and reset password if precondition is right.
def resetPassword(request):
    cookie = request.POST.get('cookie')
    oldPassword = request.POST.get('password')
    newPassword = request.POST.get('newPassword')
    return staticFunc.JsonPackage(User(cookie=cookie).resetPassword(oldPassword, newPassword))


# update profileInfo
def updateProfileInfo(request):
    cookie = request.POST.get('cookie')
    username = request.POST.get('username')
    phoneNumber = request.POST.get('phoneNumber')
    email = request.POST.get('email')
    address = request.POST.get('address')
    # security value
    # securityProblem = int(request.POST.get('value'))
    securityProblem = request.POST.get('value')
    securityAnswer = request.POST.get('securityAnswer')
    print('??????????????????'+ securityAnswer )
    print('?????????????????????????????????????????????')
    return staticFunc.JsonPackage(User(cookie=cookie).updateProfileInfo(username=username,
                                                                        phoneNumber=phoneNumber,
                                                                        email=email,
                                                                        address=address,
                                                                        securityProblem=securityProblem,
                                                                        securityAnswer=securityAnswer
                                                                        ))
    # return staticFunc.JsonPackage(User(cookie=cookie).updateProfileInfo(username=username,
    #                                                                     phoneNumber=phoneNumber,
    #                                                                     email=email,
    #                                                                     address=address))



def validateId(request):
    cookie = request.POST.get('cookie')
    goodsId = request.POST.get('goodsId')
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)

    try:
        goods = models.GoodsInfo.objects.get(id=goodsId)
        if goods.sellerId.id == viewId:
            return staticFunc.JsonPackage({"validation": False})
    except Exception as e:
        print(e)
    return staticFunc.JsonPackage({"validation": True})


# order views


def confirmOrder(request):
    orderId = request.POST.get('orderId')
    quantity = request.POST.get('quantity')
    remark = request.POST.get('remark')
    address = request.POST.get('address')
    phoneNumber = request.POST.get('phoneNumber')
    receiver = request.POST.get('receiver')
    return Order(orderId=orderId).confirmOrder(quantity=quantity,
                                               remark=remark,
                                               address=address,
                                               phoneNumber=phoneNumber,
                                               receiver=receiver)


# show basic order information
def showOrder(request):
    orderId = request.POST.get('orderId')
    cookie = request.POST.get('cookie')
    ans = staticFunc.getUserId(cookie)
    if ans['validation']:
        return staticFunc.JsonPackage(Order(orderId=orderId).showOrder(viewId=ans['uid']))
    else:
        return staticFunc.JsonPackage({"validation": False})


def confirmReceive(request):
    orderId = request.POST.get('orderId')
    cookie = request.POST.get('cookie')
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Order(orderId=orderId).confirmReceive(viewId=viewId))


def confirmSend(request):
    orderId = request.POST.get('orderId')
    cookie = request.POST.get('cookie')
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Order(orderId=orderId).confirmSend(viewId=viewId))


def payment(request):
    print(request.POST)
    orderId = request.POST.get('orderId')
    money = float(request.POST.get("amount"))
    password = request.POST.get("password")
    cookie = request.POST.get('cookie')
    return staticFunc.JsonPackage(Order(orderId=orderId).transaction(cookie=cookie, password=password, amount=money))


def editOrder(request):
    orderId = request.POST.get('orderId')
    quantity = int(request.POST.get('quantity'))
    remark = request.POST.get('remark')
    address = request.POST.get('address')
    phoneNumber = request.POST.get('receiverPhone')
    receiver = request.POST.get('receiver')
    price = request.POST.get('amount')
    cookie = request.POST.get('cookie')
    viewId = staticFunc.getUserId(cookie)
    print(request.POST)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Order(orderId=orderId).editOrder(quantity=quantity,
                                                                   remark=remark,
                                                                   address=address,
                                                                   receiverPhone=phoneNumber,
                                                                   receiver=receiver,
                                                                   totalPrice=price,
                                                                   viewId=viewId))


def deleteOrder(request):
    orderId = request.POST.get('orderId')
    cookie = request.POST.get('cookie')
    viewId = staticFunc.getUserId(cookie)
    print(request.POST)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Order(orderId=orderId).cancel(viewId=viewId))


def createOrder(request):
    goodsId = request.POST.get('goodsId')
    cookie = request.POST.get('cookie')
    status = request.POST.get('status')
    quantity = int(request.POST.get('quantity'))
    phoneNumber = request.POST.get('phoneNumber')
    receiver = request.POST.get('receiver')
    address = request.POST.get('address')
    remark = request.POST.get('remark')
    dataDict = {
        "phoneNumber": phoneNumber,
        "receiver": receiver,
        "address": address,
        "remark": remark,
        "quantity": quantity,
    }
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    ans = Order().createOrder(goodsId=goodsId, customerId=viewId, status=status, data=dataDict)
    print(ans)
    return staticFunc.JsonPackage(ans)


# static func
def writeFile(filePath, file, goodsId):
    # ??????goods_Id???????????????
    # filedir=("", "media", "?????????")
    filedir = filePath.split('/')
    # goodsId???int????????????????????????str??????
    folder = "../puxiaoyu_frontend/src/assets/"
    # / Users / apple / Desktop / puxiaoyu_frontend - main / src / assets
    # print('writeFile ??????2???')
    isExists = os.path.exists(folder)
    if not isExists:
        os.makedirs(folder)
    folder = folder + "/" + filedir[2]
    # ??????????????????????????????
    with open(folder, "wb") as f:
        if file.multiple_chunks():
            for content in file.chunks():
                f.write(content)
        else:
            data = file.read()  ###.decode('utf-8')
            f.write(data)
    # print('writeFile ??????3???')


def uploadGoods(request):
    # if request.method == "POST":
    deliverGoodsInfo(request)
    fileDict = request.FILES.items()
    print(fileDict)
    # ?????????????????????????????????????????????????????????None
    if not fileDict:
        return JsonResponse({'msg': 'no image upload'})
    for (k, v) in fileDict:
        print("dic[%s]=%s" % (k, v))
        fileData = request.FILES.getlist(k)
        for file in fileData:
            fileName = file._get_name()
            print('???????????????filename???', fileName)
            ext = fileName.split('.')[-1]
            fileName = '{}.{}'.format(uuid4().hex, ext)
            filePath = os.path.join(settings.MEDIA_URL, fileName)
            # print('filepath = [%s]'%filePath)
            # ????????????????????????ID
            goods_id = models.GoodsInfo.objects.last()
            print(goods_id.id)
            # ???????????????????????????
            models.Img.objects.create(
                img=fileName,
                goodsId_id=goods_id.id
            )
            try:
                # ??????????????????ID?????????????????????????????????????????????????????????
                writeFile(filePath, file, goods_id.id)
            except:
                return JsonResponse({'msg': 'Upload image failed'})
    return JsonResponse({'msg': 'success'})


# good operations

# save the image added to good

def showGoodsInfo(request):
    print("zhaohaodong", request.POST)
    # print('showGoodsInfo1')
    goodsId = request.POST.get('goodsId')
    # print('goodsId=', goodsId)
    return staticFunc.JsonPackage(Goods().showInfo(goodsId))

    # before creating real goodsInfo, initial it
    # ?????????ChooseCategory?????????


def intialGoodsInfo(request):
    cookie = request.POST.get('cookie')
    category = request.POST.get('category')
    print('??????view??????intialGoodsInfof???cookie', cookie)
    print('??????view??????intialGoodsInfo', category)
    categoryid = models.GoodsCategory.objects.filter(name=category).get().id
    print('??????view??????intialGoodsInfo, categoryid1=', categoryid)
    return staticFunc.JsonPackage(Goods().initialGoods(cookie=cookie, category=categoryid))

    # ????????????profile?????????????????????????????????????????????????????????cookie


def updateGoodsInfo(request):
    cookie = request.POST.get('cookie')
    goodsId = request.POST.get('goodsId')
    name = request.POST.get('name')
    price = request.POST.get('price')
    desc = request.POST.get('desc')
    inventory = request.POST.get('inventory')
    category = request.POST.get('category')
    categoryId = models.GoodsCategory.objects.filter(name=category).get().id
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Goods().updateInfo(viewId, name, price, desc, inventory,
                                                     categoryId, goodsId))

    # Store the goods information
    # ?????????????????????test???????????????????????????????????????????????????????????????


def deliverGoodsInfo(request):
    goodsId = request.POST.get('goodsId')
    print('goodsId=', goodsId)
    name = request.POST.get('name')
    print('name=', name)
    price = request.POST.get('price')
    print('price=', price)
    desc = request.POST.get('desc')
    print('desc=', desc)
    inventory = request.POST.get('inventory')
    print('inventory=', inventory)
    show = request.POST.get('show')
    print('show=', show)
    cookie = request.POST.get('cookie')
    print('cookie=', cookie)
    return staticFunc.JsonPackage(Goods().storeGoods(name=name, price=price, desc=desc,
                                                     inventory=inventory, show=show,
                                                     cookie=cookie, goodsId=int(goodsId)))


def deleteGoodsInfo(request):
    goodsId = request.POST.get('goodsId')
    cookie = request.POST.get('cookie')
    delete = request.POST.get('delete')
    viewId = staticFunc.getUserId(cookie)
    if viewId['validation']:
        viewId = viewId["uid"]
    else:
        return staticFunc.JsonPackage(viewId)
    return staticFunc.JsonPackage(Goods().deleteInfo(goodsId, viewId, delete))


def testGetCategory(request):
    goodsId = intialGoodsInfo(request).get('goodsId')
    # content=json.loads(intialGoodsInfo(request))
    # print(content)
    # goodsId=content.get('goodsId')
    print('goodsId=', goodsId)
    id = request.POST.get('id')
    category = request.POST.get('category')
    cookie = request.POST.get('cookie')
    name = request.POST.get('name')
    price = request.POST.get('price')
    desc = request.POST.get('desc')
    inventory = request.POST.get('inventory')
    show = request.POST.get('show')
    print('id=', id)
    print('price=', price)
    # cookie=request.POST.get(cookie)
    # content = json.loads(request.body)
    # print(content)
    # id=content.get("id")
    # category=content.get("category")
    # cookie=content.get("cookie")
    # ??????categoryID
    print(models.GoodsInfo.objects.values().filter(id=1))
    categoryid = models.GoodsCategory.objects.filter(name=category).get().id
    print('categoryid2=', categoryid)

    # data=Goods(id).initialGoods(categoryid, cookie)
    # goodsid=data.get('goodsId')
    # Goods(id).initialGoods(2, cookie)

    # cookie = request.POST.get('cookie')
    # staticFunc.JsonPackage()
    # print('??????testGetCategory', Goods(1).getCategory())
    # print('????????????????????????')
    # Goods().__init1__(goodsId)
    return staticFunc.JsonPackage(Goods().storeGoods(name, price, desc, inventory, show, cookie, goodsId))

    # ?????????order????????????


def testGetSellerIdandPrice(request):
    goodsId = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods().getSellerIdandPrice(goodsId))


def testCustomeOrSeller(request):
    UserId = request.POST.get('userId')
    GoodsID = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods().customeOrSeller(UserId, GoodsID))


def testIsAvailable(request):
    quantity = request.POST.get('quantity')
    goodsId = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods().isAvailable(goodsId, quantity))

    # ??????????????????????????????


def testPostIMG(request):
    # if request.method=='GET':
    goodsId = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods().getIMG(goodsId))


def index(request):
    if request.method == 'GET':
        price = models.GoodsInfo.objects.filter()
        Img = models.Img.objects.all().get().img
        return render(request, 'showImg.html', {'Img': Img, 'price': price})


# homepage
def testgetName_Price_Img(request):
    return staticFunc.JsonPackage(Goods().getName_Price_Img())


def getSortGoods(request):
    category = request.POST.get('category')
    return staticFunc.JsonPackage(Goods().getSortGoods(category))


def searchGoods(request):
    name = request.POST.get('name')
    print(name)
    return staticFunc.JsonPackage(Goods().search(name))
