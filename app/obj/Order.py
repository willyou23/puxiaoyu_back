from datetime import datetime

from app import models, staticFunc
from app.obj.Goods import Goods


class Order:
    def __init__(self, orderId=""):
        self.orderId = orderId
        self.sellerId = None
        self.customerId = None
        self.goodsId = None
        self.info = None
        self.validation = False
        self.testOrderId()

    def testOrderId(self):
        if self.orderId == "":
            return False
        else:
            try:
                self.info = models.OrderInfo.objects.get(id=self.orderId)
                self.validation = True
                self.customerId = self.info.customerId.id
                self.goodsId = self.info.goodsId.id
                self.sellerId = self.info.goodsId.sellerId.id
            except Exception as e:
                print(e)
            return True

    def showOrder(self, viewId):
        # print(viewId, self.sellerId, self.customerId)
        # print(self.isSeller(viewId), self.isCustomer(viewId))
        if (self.isSeller(viewId) or self.isCustomer(viewId)) and self.validation:
            ans = Goods().getImg(self.goodsId)
            imgList = []
            if ans["validation"]:
                imgList = ans["imgList"]

            ans = {"validation": True,
                   "date": str(self.info.date),
                   "quantity": self.info.quantity,
                   "address": self.info.address,
                   "price": float(self.info.goodsId.price),
                   "totalPrice": float(self.info.totalPrice),
                   "remark": self.info.remark,

                   "isSeller": self.isSeller(viewId),
                   "isCustomer": self.isCustomer(viewId),
                   "goodsId": self.info.goodsId.id,
                   "goodsName": self.info.goodsId.name,
                   "img": imgList,
                   "paid": self.info.paid,
                   "finished": self.info.finished,

                   "receiver": self.info.receiver,
                   "phoneNumber": self.info.phoneNumber,

                   "customerName": self.info.customerId.username,
                   "customerPhoneNumber": self.info.customerId.phoneNumber,

                   "sellerName": self.info.goodsId.sellerId.username,
                   "sellerPhoneNumber": self.info.goodsId.sellerId.phoneNumber}
            print(ans)
            return ans
        else:
            return {"validation": False, "mes": "no  authorization"}

    def confirmReceive(self, viewId):
        if self.isCustomer(viewId):
            if not self.info.finished:
                if self.info.paid:
                    self.info.finished = True
                    self.info.save()
                    return {"validation": True, "mes": "Complete successfully"}
                else:
                    return {"validation": False, "mes": "Order has not been paid"}
            else:
                return {"validation": False, "mes": "can't be confirmed repeatedly"}
        return {"validation": False, "mes": "invalid user"}

    def transaction(self, cookie, amount, password):
        if self.validation:
            if amount == float(self.info.totalPrice):
                ans = staticFunc.payMoney(cookie=cookie, amount=amount, password=password)
                if ans['validation']:
                    self.info.goodsId.sellerId.balance = float(self.info.goodsId.sellerId.balance) + amount
                    self.info.paid = True
                    self.info.save()
                    self.info.goodsId.sellerId.save()
                print(ans)
                return ans

        return {"validation": False, 'mes': "Order Error: not exist"}

        # change quantity, address, phoneNumber, receiver

    def editOrder(self, viewId, quantity, address, receiverPhone, receiver, remark, totalPrice):
        if self.isCustomer(viewId):
            self.info.quantity = quantity
            self.info.address = address
            self.info.phoneNumber = receiverPhone
            self.info.receiver = receiver
            self.info.remark = remark
            self.info.totalPrice = totalPrice
            self.info.save()
            return {"validation": True, "mes": "Update successfully"}
        elif self.isSeller(viewId):
            self.info.totalPrice = totalPrice
            self.info.save()
            return {"validation": True, "mes": "Update successfully"}
        else:
            return {"validation": False, "mes": "Update error"}

    def cancel(self, viewId):
        if self.isCustomer(viewId):
            if self.info.finished or not self.info.paid:
                self.info.removal = True
                self.info.save()
                return {"validation": True, "mes": "Delete successfully"}
        return {"validation": False, "mes": "Error: Invalid user"}

    def isSeller(self, viewId):
        return self.sellerId == viewId

    def isCustomer(self, viewId):
        return self.customerId == viewId

    def createOrder(self, goodsId, customerId, status, data):
        if status == "initial":
            try:
                models.OrderInfo.objects.create(
                    goodsId=models.GoodsInfo.objects.get(id=goodsId),
                    customerId=models.User.objects.get(id=customerId),
                    sign=customerId,
                    date=datetime.now()
                )
                query = models.OrderInfo.objects.get(sign=customerId)
                self.orderId = query.id
                query.sign = "-1"  # release current process lock
                query.save()
                self.testOrderId()
                if self.validation:
                    return {"orderId": self.orderId,
                            "goodsName": self.info.goodsId.name,
                            "goodsQuantity": self.info.goodsId.inventory,
                            "goodsPrice": float(self.info.goodsId.price),
                            "customer": self.info.customerId.username,
                            "phoneNumber": self.info.customerId.phoneNumber,
                            "address": self.info.customerId.address,
                            "validation": True}
            except Exception as e:
                print(e)
            return {"validation": False, "mes": "create order failed"}
        else:
            if self.validation:
                try:
                    self.info.receiver = data['receiver']
                    self.info.quantity = data['quantity']
                    self.info.phoneNumber = data['phoneNumber']
                    self.info.address = data['address']
                    self.info.remark = data['remark']
                    self.info.totalPrice = data['quantity'] * float(self.info.goodsId.price)
                    self.info.save()
                    self.testOrderId()
                    print("hello",self.validation)
                    if self.validation:
                        return {"orderId": self.orderId,
                                "goodsName": self.info.goodsId.name,
                                "quantity": self.info.quantity,
                                "goodsPrice": float(self.info.goodsId.price),
                                "customer": self.info.customerId.username,
                                "phoneNumber": self.info.phoneNumber,
                                "goodsQuantity": self.info.goodsId.inventory,
                                "receiver": self.info.receiver,
                                "address": self.info.address,
                                "remark": self.info.remark,
                                "mes": "successfully",
                                "validation": True}
                    else:
                        return {"validation": False,
                                "mes": "get date query failed"}
                except Exception as e:
                    print(e)
                return {"validation": False,
                        "mes": "save data failed"}
            return {"validation": False,
                    "mes": "order doesn't exist"}

    def confirmOrder(self, quantity, remark, address, phoneNumber, receiver):
        try:
            self.info.receiver = receiver
            self.info.remark = remark
            self.info.address = address
            self.info.phoneNumber = phoneNumber
            self.info.quantity = quantity
            self.info.save()
            self.testOrderId()  # refresh
            return {"validation": True,
                    "quantity": self.info.quantity,
                    "address": self.info.address,
                    "receiver": self.info.receiver,
                    "phoneNumber": self.info.phoneNumber,
                    "price": self.info.price,
                    "remark": self.info.remark}
        except Exception as e:
            print(e)
        return {"validation": True}

    def whetherPaid(self, validation):  # connect to transaction
        if validation:
            self.info.paid = True
            self.info.save()
            return {}
        return {}
