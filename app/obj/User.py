import json
from datetime import datetime

from django.http import JsonResponse

from app import models, staticFunc


class User:
    # get cookie to initialize the object
    def __init__(self, cookie=""):
        self.info = None
        self.cookie = cookie  # just individual cookie property
        self.validation = False
        self.testExist()

    # test whether query is existed or not
    def testExist(self):
        if self.cookie != "":
            query = models.User.objects.filter(cookie=self.cookie)
            if len(query) > 0:
                self.info = query[0]
                self.validation = True

    # test whether cookie is outdated or not
    def testOutdated(self):
        if not self.validation:
            return False
        date = datetime.now().date()
        if (date - self.info.date).days > 7:
            return False
        else:
            return True

    def login(self, username, password):
        query = models.User.objects.filter(username=username)
        if len(query) > 0:
            self.info = query[0]
            self.validation = True
        else:
            return {"validation": False}
        if password == self.info.password:
            date = datetime.now().date()
            if not self.info.cookie or (date - self.info.date).days > 7:  # update cookie if needed
                self.info.cookie = staticFunc.get_random_number_str(20)
                self.info.date = date
                self.info.save()
            return {'cookie': self.info.cookie, "validation": self.validation}
        else:
            return {"validation": False}

    # Create Account
    def createAccount(self, username, email, password, question, answer):

        if len(question) == 0:
            return {"validation": False, "errmess": "请先选择问题"}

        if len(answer) == 0:
            return {"validation": False, "errmess": "请先回答问题"}

        if models.User.objects.filter(username=username) or models.User.objects.filter(email=email):
            print('找到该用户，不用创建用户')
            return {"validation": self.validation, "errmess": "该用户已注册，请直接登录"}
        else:
            print('没有找到该用户，进行创建用户')
            self.cookie = staticFunc.get_random_number_str(20)
            print('开始创建用户表')
            models.User.objects.create(
                username=username,
                email=email,
                password=password,
                date=datetime.now(),
                admin=0,
                balance=0.0,
                cookie=self.cookie
            )
            print('用户创建完成')
            # 拿到user表中的id
            userObject = models.User.objects.get(username=username)

            question = int(question)
            print('开始创建密保问题表')
            models.SecurityQuestion.objects.create(
                question=question,
                answer=answer,
                user_id_id=userObject.id
            )
            print('密保问题表创建完成')
            self.testExist()  # change validation and self.info
            return {"validation": self.validation, 'cookie': self.cookie}

    def forgetPassword(self, username, newpassword, question, answer):
        # 进行判断 输入的密保问题是否正确
        # 先判断这个账号是否在数据库里存在
        if len(question) == 0:
            return {"validation": False, "errmess": "请先选择问题"}

        if len(answer) == 0:
            return {"validation": False, "errmess": "请先回答问题"}

        if models.User.objects.filter(username=username):
            print('找到该用户,进行重置密码操作')
            # 得到用户的id
            username = models.User.objects.get(username=username)
            print(username)
            print(username.id)
            # 根据用户id，从而确定他的密保表的数据
            data = models.SecurityQuestion.objects.get(user_id_id=username.id)
            # 先获取数据库的密保问题
            newquestion = int(question)
            # 将传过来的问题与数据库内部对比 如果不存在则返回密保选择错误
            if data.question != newquestion:
                return {"validation": False, "errmess": "密保选择错误"}
            # 将他的密保答案进行匹配
            if data.answer == answer:
                # 匹配正确，则进行修改密码
                username.password = newpassword
                username.save()
                return {"validation": True}
                # 匹配失败，则返回无效，返回密保答案错误
            else:
                return {"validation": False, "errmess": "密保回答错误"}
        # 如果用户不存在，则返回无效
        else:
            return {"validation": self.validation, "errmess": "用户不存在，请先注册"}
            # 用户不存在，请先注册

    # get two password, one for compare/confirm and the other one for reset
    def resetPassword(self, oldPassword, newPassword):
        if self.validation and self.testOutdated():
            if self.info.password == oldPassword:
                self.info.password = newPassword
                self.info.save()
                return {"validation": True}
            else:
                return {"validation": False, "mes": "old password incorrect"}
        elif not self.validation:
            return {"validation": self.validation, "mes": "no user exist"}
        elif not self.testOutdated():
            return {"validation": self.validation, "mes": "login expired"}

    # get information of user and return them (different requirement)
    def getProfileInfo(self, whole=True):
        if self.validation and self.testOutdated():
            if whole:
                goodsList, orderList = staticFunc.findInfo(self.info.id)
                return {'username': self.info.username,
                        "phoneNumber": self.info.phoneNumber,
                        "email": self.info.email,
                        'id': self.info.id,
                        "address": self.info.address,
                        "balance": float(self.info.balance),
                        "goodsList": goodsList,
                        "orderList": orderList,
                        "validation": self.validation}
            else:
                return {'username': self.info.username,
                        'id': self.info.id,
                        "validation": self.validation}
        elif not self.validation:
            return {"validation": self.validation}
        elif not self.testOutdated():
            return {"validation": self.validation, "mes": "login expired"}

    # def updateProfileInfo(self, username, phoneNumber, email, address):
    def updateProfileInfo(self, username, phoneNumber, email, address, securityProblem, securityAnswer):
        print('已拿到所有值')
        if len(securityProblem) == 0:
            return {"validation": False, "errmess": "please choose question"}

        if len(securityAnswer) == 0:
            return {"validation": False, "errmess": "please return answer"}

        if self.validation and self.testOutdated():
            self.info.username = username
            self.info.phoneNumber = phoneNumber
            self.info.email = email
            self.info.address = address
            self.info.save()
            # security problem & answer updation
            print('用户的id' + str(self.info.id))
            security = models.SecurityQuestion.objects.get(user_id=self.info.id)
            security.question = int(securityProblem)
            security.answer = securityAnswer
            security.save()
            return {'username': self.info.username,
                    "phoneNumber": self.info.phoneNumber,
                    "email": self.info.email,
                    "address": self.info.address,
                    "balance": float(self.info.balance),
                    "securityProblem": security.question,
                    "securityAnswer": security.answer,
                    "validation": self.validation}
            #
            # return {'username': self.info.username,
            #         "phoneNumber": self.info.phoneNumber,
            #         "email": self.info.email,
            #         "address": self.info.address,
            #         "balance": float(self.info.balance),
            #         "validation": self.validation}
        elif not self.validation:
            return {"validation": self.validation}
        elif not self.testOutdated():
            return {"validation": self.validation, "mes": "login expired"}

    def topUpMoney(self):
        pass

    def payMoney(self, amount, password):
        if self.validation and self.testOutdated():
            if self.info.password == password:
                if self.info.balance >= amount:
                    self.info.balance = float(self.info.balance) - amount
                    self.info.save()
                    return {"validation": True, "mes": "Successful payment"}
                else:
                    return {"validation": False, "mes": "Failed payment: No enough balance, please top up your account"}
            else:
                return {"validation": False, "mes": "Failed payment: Password wrong"}
        return {"validation": False, "mes": "Failed payment: login expire"}
