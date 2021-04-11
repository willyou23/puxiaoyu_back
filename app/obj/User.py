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
            return JsonResponse(json.dumps({"validation": False}), safe=False)
        if password == self.info.password:
            date = datetime.now().date()
            if not self.info.cookie or (date - self.info.date).days > 7:  # update cookie if needed
                self.info.cookie = staticFunc.get_random_number_str(20)
                self.info.save()
            return JsonResponse(json.dumps({'cookie': self.info.cookie, "validation": self.validation}), safe=False)
        else:
            return JsonResponse(json.dumps({"validation": False}), safe=False)

    # Create Account
    def createAccount(self, username, email, password):
        if models.User.objects.filter(username=username) or models.User.objects.filter(email=email):
            return JsonResponse(json.dumps({"validation": self.validation}), safe=False)
        else:
            self.cookie = staticFunc.get_random_number_str(20)
            models.User.objects.create(
                username=username,
                email=email,
                password=password,
                date=datetime.now(),
                admin=0,
                balance=0.0,
                cookie=self.cookie
            )
            self.testExist()  # change validation and self.info
            return JsonResponse(json.dumps({"validation": self.validation, 'cookie': self.cookie}), safe=False)

    # get two password, one for compare/confirm and the other one for reset
    def resetPassword(self, oldPassword, newPassword):
        if self.validation and self.testOutdated():
            if self.info.password == oldPassword:
                self.info.password = newPassword
                self.info.save()
                return JsonResponse(json.dumps({"validation": True}), safe=False)
            else:
                return JsonResponse(json.dumps({"validation": False, "mes": "old password incorrect"}), safe=False)
        elif not self.validation:
            return JsonResponse(json.dumps({"validation": self.validation, "mes": "no user exist"}), safe=False)
        elif not self.testOutdated():
            return JsonResponse(json.dumps({"validation": self.validation, "mes": "login expired"}), safe=False)

    # get information of user and return them (different requirement)
    def getProfileInfo(self, whole=True):
        if self.validation and self.testOutdated():
            if whole:
                return JsonResponse(json.dumps({'username': self.info.username,
                                                "phoneNumber": self.info.phoneNumber,
                                                "email": self.info.email,
                                                "balance": float(self.info.balance),
                                                "validation": self.validation}), safe=False)
            else:
                return JsonResponse(json.dumps({'username': self.info.username,
                                                "validation": self.validation}), safe=False)
        elif not self.validation:
            return JsonResponse(json.dumps({"validation": self.validation}), safe=False)
        elif not self.testOutdated():
            return JsonResponse(json.dumps({"validation": self.validation, "mes": "login expired"}), safe=False)

    def updateProfileInfo(self, username, phoneNumber, email):
        if self.validation and self.testOutdated():
            self.info.username = username
            self.info.phoneNumber = phoneNumber
            self.info.email = email
            self.info.save()
            return JsonResponse(json.dumps({'username': self.info.username,
                                            "phoneNumber": self.info.phoneNumber,
                                            "email": self.info.email,
                                            "balance": float(self.info.balance),
                                            "validation": self.validation}), safe=False)
        elif not self.validation:
            return JsonResponse(json.dumps({"validation": self.validation}), safe=False)
        elif not self.testOutdated():
            return JsonResponse(json.dumps({"validation": self.validation, "mes": "login expired"}), safe=False)



