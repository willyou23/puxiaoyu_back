import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app import models, staticFunc


# Create your views here.

# login view
def login(request):
    try:
        query = models.User.objects.filter(username=request.POST.get('username'))[0]
        if request.POST.get("password") == query.password:
            date = datetime.now().date()
            # print((date-query.date).days)
            if not query.cookie or (date - query.date).days > 7:  # update cookie if needed
                query.cookie = staticFunc.get_random_number_str(20)
                query.save()
                print("update cookie successfully")
            return JsonResponse(json.dumps({'cookie': query.cookie, "validation": True}), safe=False)
    except Exception as e:
        print(e)
    return JsonResponse(json.dumps({"validation": False}), safe=False)


# createAccount view, accept a form info
def createAccount(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if models.User.objects.filter(username=username) or models.User.objects.filter(email=email):
        return JsonResponse(json.dumps({"validation": False}), safe=False)
    else:
        cookie = staticFunc.get_random_number_str(20)
        models.User.objects.create(
            username=username,
            email=email,
            password=password,
            date=datetime.now(),
            admin=0,
            balance=0.0,
            cookie=cookie
        )
        return JsonResponse(json.dumps({"validation": True, 'cookie': cookie}), safe=False)


# use cookie to find user information. Increase the security
def getInfo1(request):
    cookie = request.POST.get('cookie')
    try:
        query = models.User.objects.filter(cookie=cookie)[0]
        date = datetime.now().date()
        if (date - query.date).days > 7:  # update cookie if needed
            return JsonResponse(json.dumps({"validation": False, "mes": "login expired"}), safe=False)
        return JsonResponse(json.dumps({'username': query.username, "validation": True}), safe=False)
    except Exception as e:
        print(e)
    return JsonResponse(json.dumps({"validation": False}), safe=False)


# use cookie to get user information  and form the profile
def profileInfo(request):
    cookie = request.POST.get('cookie')
    try:
        query = models.User.objects.filter(cookie=cookie)[0]
        date = datetime.now().date()
        if (date - query.date).days > 7:  # update cookie if needed
            return JsonResponse(json.dumps({"validation": False, "mes": "login expired"}), safe=False)
        return JsonResponse(json.dumps({'username': query.username,
                                        "phoneNumber": query.phoneNumber,
                                        "email": query.email,
                                        "balance": float(query.balance),
                                        "validation": True}), safe=False)
    except Exception as e:
        print(e)
    return JsonResponse(json.dumps({"validation": False}), safe=False)


# reset password view, compare old function firstly, and reset password if precondition is right.
def resetPassword(request):
    cookie = request.POST.get('cookie')
    oldPassword = request.POST.get('oldPassword')
    newPassword = request.POST.get('newPassword')
    try:
        query = models.User.objects.filter(cookie=cookie)[0]
        date = datetime.now().date()
        if (date - query.date).days > 7:  # update cookie if needed
            return JsonResponse(json.dumps({"validation": False, "mes": "login expired"}), safe=False)
        if query.password == oldPassword:
            query.password = newPassword
            query.save()
        else:
            return JsonResponse(json.dumps({"validation": False, "mes": "old password incorrect"}), safe=False)
        return JsonResponse(json.dumps({"validation": True}), safe=False)

    except Exception as e:
        print(e)
    return JsonResponse(json.dumps({"validation": False}), safe=False)
