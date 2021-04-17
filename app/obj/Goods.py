import json

from app import models, staticFunc
from django.http import JsonResponse
from rest_framework.decorators import action

from app.obj.User import User


class Goods:
    def __init__(self, goodsId=""):
        self.goodsId = goodsId
        self.info = None
        self.validation = False
        self.imgList = []
        self.category = None
        self.seller = ""
        self.user = None
        self.testExist()

    # test whether query is existed or not
    def testExist(self):
        try:
            query = models.GoodsInfo.objects.get(id=self.goodsId)
            self.info = query
            self.validation = True
        except Exception as e:
            print(e)

    # whether category exists, get category name
    def getCategory(self):
        if self.validation:
            try:
                query = models.GoodsCategory.objects.get(id=self.info.categoryID)
                self.category = query.name
                return True
            except Exception as e:
                print(e)
        return False

    # get image list
    def getIMG(self):
        if self.validation:
            query = models.Img.objects.filter(goodsId=self.goodsId)
            for item in query:
                self.imgList.append(item.img)
            return True
        return False

    # get seller name
    def getSeller(self):
        if self.validation:
            try:
                query = models.User.objects.get(id=self.info.sellerId)
                self.seller = query.username
                return True
            except Exception as e:
                print(e)
        return False

    # save img
    @action(methods=['post'], detail=False)
    def saveImg(self, request):
        goodsId = request.POST['goodsId']
        file = request.FILES.get('file')

        try:
            file = staticFunc.processImg(file, goodsId)
            img = models.Img(img=file, goodsId=goodsId)
            img.save()
            response = {'file': file.name, 'code': 200, 'msg': "添加成功"}
        except Exception as e:
            response = {'file': '', 'code': 201, 'msg': "添加失败"}
            print(e)
        return JsonResponse(response)

    # show goods info
    def showInfo(self):
        if self.validation:
            try:
                self.getIMG()
                self.getCategory()
                return JsonResponse(json.dumps({"validation": True,
                                                "name": self.info.name,
                                                "price": self.info.price,
                                                "desc": self.info.desc,
                                                "inventory": self.info.inventory,
                                                "category": self.category,
                                                "seller": self.seller,
                                                "imgList": self.imgList
                                                }), safe=False)
            except Exception as e:
                print(e)
        return JsonResponse(json.dumps({"validation": False}), safe=False)

    def initialGoods(self, category, cookie):
        userInfo = User(cookie=cookie).getProfileInfo(whole=False)
        if userInfo['validation']:
            models.GoodsInfo.objects.create(
                sellerId=userInfo['id'],
                categoryID=category,
                tag=userInfo['id'],
                show=False
            )
            try:
                query = models.GoodsInfo.objects.get(tag=userInfo['id'])
                goodsId = query.id
                query.tag = -1
                query.save()
                return JsonResponse(json.dumps({"validation": True, "goodsId": goodsId}), safe=False)
            except Exception as e:
                print(e)
        return JsonResponse(json.dumps({"validation": False}), safe=False)

    def storeGoods(self, name, price, desc, inventory, show, cookie):
        userInfo = User(cookie=cookie).getProfileInfo(whole=False)
        if userInfo['validation'] and self.validation:
            if userInfo['id'] == self.info.sellerId:
                try:
                    self.info.name = name
                    self.info.price = price
                    self.info.desc = desc
                    self.info.inventory = inventory
                    self.info.show = show
                    self.info.save()
                    self.testExist()
                    return {"validation": True}
                except Exception as e:
                    print(e)
        return {"validation": False}
