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
                # print('what happened???2')
                self.getCategory(goodsId)
                # print('what happened???3')
                self.getSeller(goodsId)
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

    def updateInfo(self, viewId, name, price, desc, inventory, categoryId, goodsId):
        try:
            query = models.GoodsInfo.objects.get(id=goodsId)
            if query.sellerId.id != viewId:
                return {'validation': False, "mes": "invalid user"}
            else:
                query.name = name
                query.price = price
                query.desc = desc
                query.inventory = inventory
                query.categoryID = models.GoodsCategory.objects.get(id=categoryId)
                query.save()
                newQuery = models.GoodsInfo.objects.get(id=goodsId)
                imgList = self.getImg(goodsId=goodsId)["imgList"]
                return {'validation': True,
                        "name": newQuery.name,
                        "price": str(Decimal(newQuery.price).quantize(Decimal('0.0'))),
                        "desc": newQuery.desc,
                        "inventory": newQuery.inventory,
                        "category": newQuery.categoryID.name,
                        "seller": newQuery.sellerId.username,
                        "imgList": imgList,
                        "mes": "update successfully"}
        except Exception as e:
            print(e)
        return {'validation': False, "mes": "unknown error"}

    # 删除数据
    def deleteInfo(self, goodsId, viewId, delete):
        try:
            query = models.GoodsInfo.objects.get(id=goodsId)
            if query.sellerId.id != viewId:
                return {'validation': False, "mes": "invalid user"}
            elif delete:
                query.show = False
                query.save()
                return {'validation': True, "mes": "delete successfully"}
        except Exception as e:
            print(e)
        return {'validation': False, "mes": "unknown error"}

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

        # 点击分类的名字获取该类型的goods
    def getSortGoods(self, category):
        # 根据名字获取类型的ID
        try:
            print('需要获取的是', category, '的商品.')
            categoryId = models.GoodsCategory.objects.filter(name=category).get().id
            goodsId = models.GoodsInfo.objects.filter(categoryID_id=categoryId).values('id')
            # 获取商品名字
            goodsName = []
            # 商品价格
            goodsPrice = []
            # 商品图片
            goodsImg = []
            # 将query set转换成list
            newGoodsId = list(goodsId)
            newGoodsId1 = []
            # 将收集好的信息按商品放到gatherInfo中
            gatherInfo = []
            # 通过goodsId筛选出name不为none的商品,并将筛选之后的商品添加到新的数列newGoodsId1和goodsName中
            for i in range(0, len(newGoodsId)):
                if not models.GoodsInfo.objects.get(id=newGoodsId[i].get('id')).show:
                    continue
                singlegoodsName = models.GoodsInfo.objects.filter(id=newGoodsId[i].get('id')).get().name
                if singlegoodsName is not None:
                    goodsName.append({'name': singlegoodsName})
                    newGoodsId1.append(newGoodsId[i])
            # 通过goodsId筛选出price,并将筛选之后的商品价格添加到goodsPrice中
            for i in range(0, len(newGoodsId1)):
                # print(newGoodsId1[i].get('id'))
                # print(models.GoodsInfo.objects.filter(id=newGoodsId1[i].get('id')).get().id)
                price = models.GoodsInfo.objects.filter(id=newGoodsId1[i].get('id')).get().price
                # print(newGoodsId1[i], ' price=', price)
                goodsPrice.append({"price": str(Decimal(price).quantize(Decimal('0.0')))})
            # 通过goodsId找出商品对应的图片
            for i in range(0, len(newGoodsId1)):
                try:
                    # print(models.Img.objects.filter(goodsId_id=15).get().goodsId_id)
                    img = models.Img.objects.filter(goodsId_id=newGoodsId1[i].get('id')).first().img
                    goodsImg.append({'img': str(img)})
                    # print('这一次她可以了')
                except Exception as e:
                    print(e)
                    # i += 1
                    goodsImg.append({'img': 'None'})
            # print(goodsImg)
            # 将收集好的信息按商品放到gatherInfo中
            for i in range(0, len(newGoodsId1)):
                gatherInfo.append({'id': newGoodsId1[i].get('id'), 'name': goodsName[i].get('name'),
                                   'price': goodsPrice[i].get('price'), 'img': goodsImg[i].get('img')})
            return {'validation': True, 'goodsinfo': gatherInfo}
        except Exception as e:
            print(e)
        return {'validation': False}

    # homepage调用这个函数获取数据库中的name，price和img
    def getName_Price_Img(self):
        try:
            # 商品ID
            goodsId = models.GoodsInfo.objects.values('id')

            # 获取商品名字
            goodsName = []
            # 商品价格
            goodsPrice = []
            # 商品图片
            goodsImg = []
            # 将query set转换成list
            newGoodsId = list(goodsId)
            newGoodsId1 = []
            # 将收集好的信息按商品放到gatherInfo中
            gatherInfo = []
            # 通过goodsId筛选出name不为none的商品,并将筛选之后的商品添加到新的数列newGoodsId1和goodsName中
            for i in range(0, len(newGoodsId)):
                if not models.GoodsInfo.objects.get(id=newGoodsId[i].get('id')).show:
                    continue
                singlegoodsName = models.GoodsInfo.objects.filter(id=newGoodsId[i].get('id')).get().name
                if singlegoodsName is not None:
                    goodsName.append({'name': singlegoodsName})
                    newGoodsId1.append(newGoodsId[i])
            # 通过goodsId筛选出price,并将筛选之后的商品价格添加到goodsPrice中
            for i in range(0, len(newGoodsId1)):
                # print(newGoodsId1[i].get('id'))
                # print(models.GoodsInfo.objects.filter(id=newGoodsId1[i].get('id')).get().id)
                price = models.GoodsInfo.objects.filter(id=newGoodsId1[i].get('id')).get().price
                # print(newGoodsId1[i], ' price=', price)
                goodsPrice.append({"price": str(Decimal(price).quantize(Decimal('0.0')))})
            # 通过goodsId找出商品对应的图片
            for i in range(0, len(newGoodsId1)):
                try:
                    # print(models.Img.objects.filter(goodsId_id=15).get().goodsId_id)
                    img = models.Img.objects.filter(goodsId_id=newGoodsId1[i].get('id')).first().img
                    goodsImg.append({'img': str(img)})
                    # print('这一次她可以了')
                except Exception as e:
                    print(e)
                    # i += 1
                    goodsImg.append({'img': 'None'})
            # print(goodsImg)
            # 将收集好的信息按商品放到gatherInfo中
            for i in range(0, len(newGoodsId1)):
                gatherInfo.append({'id': newGoodsId1[i].get('id'), 'name': goodsName[i].get('name'),
                                   'price': goodsPrice[i].get('price'), 'img': goodsImg[i].get('img')})
            return {'validation': True, 'goodsinfo': gatherInfo}
        except Exception as e:
            print(e)
        return {'validation': False}

    def search(self, name):
        try:
            gatherInfo = []
            try:
                manyGoods = models.GoodsInfo.objects.filter(name__icontains=name)
            except Exception as e:
                manyGoods = models.GoodsInfo.objects.none()

            try:
                newManyGoods = models.GoodsInfo.objects.none()

                UserId = models.User.objects.filter(username__icontains=name)

                for Id in UserId:
                    newManyGoods = models.GoodsInfo.objects.filter(sellerId=Id.id)
                    manyGoods = manyGoods | newManyGoods

            except Exception as e:

                newManyGoods = models.GoodsInfo.objects.none()
            manyGoods = manyGoods | newManyGoods
            if manyGoods.count() == 0:
                return {'validation': False, 'goodsinfo': gatherInfo}

            # manyGoods = models.GoodsInfo.objects.filter(name__iregex="^" + name)
            recordedGoodsId = []
            recordedGoodsName = []
            recordedGoodsPrice = []
            recordedGoodsImg = []

            for goods in manyGoods:
                # if (str(name) in goods.name) :
                if goods.show == 1:
                    recordedGoodsId.append({'id': goods.id})
                    recordedGoodsName.append({'name': goods.name})
                    recordedGoodsPrice.append({"price": str(Decimal(goods.price).quantize(Decimal('0.0')))})
                    # recordedGoodsImg.append({'img': goods})

            for i in range(0, len(recordedGoodsId)):
                try:
                    # print(newGoodsId1[i].get('id'))
                    # print(models.Img.objects.filter(goodsId_id=15).get().goodsId_id)
                    img = models.Img.objects.filter(goodsId_id=recordedGoodsId[i].get('id')).first().img
                    # print(img)
                    recordedGoodsImg.append({'img': str(img)})
                    # print('这一次她可以了')
                except Exception as e:
                    recordedGoodsImg.append({'img': 'None'})
            for i in range(0, len(recordedGoodsId)):
                gatherInfo.append({'id': recordedGoodsId[i].get('id'), 'name': recordedGoodsName[i].get('name'),
                                   'price': recordedGoodsPrice[i].get('price'), 'img': recordedGoodsImg[i].get('img')})
                # print(goods.name)
            return {'validation': True, 'goodsinfo': gatherInfo}
        except Exception as e:
            print(e)
        return {'validation': False}
