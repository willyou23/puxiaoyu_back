import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from app import models, staticFunc
from app.obj.Goods import Goods
from app.obj.User import User


# Create your views here.

# login view
def login(request):
    username = request.POST.get('username')
    password = request.POST.get("password")
    return staticFunc.JsonPackage(User().login(username, password))


# createAccount view, accept a form info
def createAccount(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    return staticFunc.JsonPackage(User().createAccount(username, email, password))


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
    return staticFunc.JsonPackage(User(cookie=cookie).updateProfileInfo(username=username,
                                                                        phoneNumber=phoneNumber,
                                                                        email=email,
                                                                        address=address))


# save the image added to good
def saveImage(request):
    goodsId = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods(goodsId=goodsId).saveImg(request))


# show goods information
def showGoodsInfo(request):
    goodsId = request.POST.get('goodsId')
    return staticFunc.JsonPackage(Goods(goodsId=goodsId).showInfo())


# before creating real goodsInfo, initial it
def intialGoodsInfo(request):
    cookie = request.POST.get('cookie')
    category = request.POST.get('category')
    return staticFunc.JsonPackage(Goods().initialGoods(cookie=cookie,
                                                       category=category))


# deliver the goods
def deliverGoodsInfo(request):
    goodsId = request.POST.get('goodsId')
    name = request.POST.get('name')
    price = request.POST.get('price')
    desc = request.POST.get('desc')
    inventory = request.POST.get('inventory')
    show = request.POST.get('show')
    cookie = request.POST.get('cookie')
    return staticFunc.JsonPackage(Goods(goodsId=goodsId).storeGoods(name=name,
                                                                    price=price,
                                                                    desc=desc,
                                                                    inventory=inventory,
                                                                    show=show,
                                                                    cookie=cookie
                                                                    ))
