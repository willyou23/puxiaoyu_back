import json
from decimal import Decimal

from app import models, staticFunc
from django.http import JsonResponse
from rest_framework.decorators import action

from app.obj.User import User


class Goods:
    def __init1__(self, goodsId):
        # print('这是__init__中的', self)
        self.goodsId = goodsId
        # self.info = None
        # self.validation = False
        # self.imgList = []
        # self.category = None
        # self.seller = ""
        # self.user = None
        self.testExist()
        print('__init1__之后的', self.validation)

    def __init__(self):
        self.goodsId = None
        self.info = None
        self.validation = False
        self.imgList = []
        self.category = None
        self.seller = ""
        self.user = None
        # self.testExist()

    # test whether query is existed or not
    def testExist(self):
        try:
            # print("self_goodsId", self.goodsId)
            query = models.GoodsInfo.objects.get(id=self.goodsId)
            # print("testExist是否执行2")
            self.info = query
            # print("testExist是否执行3")
            self.validation = True
        except Exception as e:
            print(e)

    # whether category exists, get category name
    def getCategory(self, goodsId):
        self.__init1__(goodsId)
        # print('这是getCategory中的', self)
        if self.validation:
            try:
                # print("getCategory是否执行1")
                query = models.GoodsCategory.objects.get(id=self.info.categoryID_id)
                # print("getCategory是否执行2")
                self.category = query.name
                # print("getCategory是否执行3", self.category)
                return {'validation': True, 'category': self.category}
            except Exception as e:
                # print("error", self.category)
                print(e)
        return {'validation': False, 'category': 'Category not found'}

    # get image list
    def getIMG(self, goodsId):
        self.__init1__(goodsId)
        if self.validation:
            query = models.Img.objects.filter(goodsId_id=self.goodsId)
            for item in query:
                self.imgList.append(str(item.img))
            return True
        return False

    def getImg(self, goodsId):
        if self.getIMG(goodsId):
            return {"validation": True, "imgList": self.imgList}
        else:
            return {"validation": False}

    # get seller name
    def getSeller(self, goodsId):
        self.__init1__(goodsId)
        if self.validation:
            try:
                query = models.User.objects.get(id=self.info.sellerId_id)
                self.seller = query.username
                return self.seller
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

    # show goods info(all of information)
    def showInfo(self, goodsId):
        self.__init1__(goodsId)
        if self.validation:
            try:
                # print('what happened???1')
                self.getIMG(goodsId)
                print(self.imgList)
                # print('what happened???2')
                self.getCategory(goodsId)
                # print('what happened???3')
                self.getSeller(goodsId)
                print(self.category)
                return {"validation": True, "name": self.info.name,
                        "price": str(Decimal(self.info.price).quantize(Decimal('0.0'))), "desc": self.info.desc,
                        "inventory": self.info.inventory, "category": self.category,
                        "seller": self.seller, "imgList": self.imgList}
            except Exception as e:
                print(e)
        return {"validation": False}

    def initialGoods(self, category, cookie):

        userInfo = User(cookie=cookie).getProfileInfo(whole=False)

        if userInfo['validation']:

            models.GoodsInfo.objects.create(
                sellerId_id=userInfo['id'],
                categoryID_id=category,
                tag=userInfo['id'],
                show=False
            )
            try:
                # print('这步执行了吗3')
                query = models.GoodsInfo.objects.get(tag=userInfo['id'])
                goodsId = query.id
                query.tag = -1
                query.save()
                # print('这步执行了吗4')
                return {"validation": True, "goodsId": goodsId}
            except Exception as e:
                print(e)
        return {"validation": False}

    def storeGoods(self, name, price, desc, inventory, show, cookie, goodsId):
        self.__init1__(goodsId)
        # 加验证
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

    def updateInfo(self, name, price, desc, inventory, categoryId, goodsId):
        try:
            models.GoodsInfo.objects.filter(id=goodsId).update(name=name)
            models.GoodsInfo.objects.filter(id=goodsId).update(price=price)
            models.GoodsInfo.objects.filter(id=goodsId).update(desc=desc)
            models.GoodsInfo.objects.filter(id=goodsId).update(inventory=inventory)
            models.GoodsInfo.objects.filter(id=goodsId).update(categoryID_id=categoryId)
            return {'validation': True, 'update': True}
        except Exception as e:
            print(e)
        return {'validation': False}

    # 删除数据
    def deleteInfo(self, goodsId):
        try:
            models.GoodsInfo.objects.filter(id=goodsId).delete()
            return {'validation': True}
        except Exception as e:
            print(e)
        return {'validation': False}

    # order页面需要的功能

    # 根据goodsId获取卖家的ID和价钱
    def getSellerIdandPrice(self, goodsId):
        try:
            self.__init1__(goodsId)
            # 注意这里返回的price是一个str类型
            return {'validation': True, 'sellerId': self.info.sellerId_id,
                    'price': str(Decimal(self.info.price).quantize(Decimal('0.0')))}
        except Exception as e:
            print(e)
        return {'validation': False}

    # 确定某个user是不是这个商品的seller
    def customeOrSeller(self, UserId, goodsId):
        self.__init1__(goodsId)
        try:
            self.__init1__(goodsId)
            # int(UserId)表示拿到的UserId是Str需要转换成int
            if self.info.sellerId_id == int(UserId):
                return {'validation': True, 'custome': False}
            return {'validation': True, 'custome': True}
        except Exception as e:
            print(e)
        return {'validation': True}

    # 检查要购买的商品数量是否超过库存
    def isAvailable(self, goodsId, quantity):
        try:
            self.__init1__(goodsId)
            if self.info.inventory >= int(quantity):
                return {'validation': True, 'available': True}
            return {'validation': True, 'avaliable': False}
        except Exception as e:
            print(e)
        return {'validation': False}
