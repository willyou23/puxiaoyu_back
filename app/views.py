import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app import models, staticFunc
from app.obj.User import User


# from app.obj.IMG import IMG


# Create your views here.

# login view
def login(request):
    username = request.POST.get('username')
    password = request.POST.get("password")
    return User().login(username, password)


# createAccount view, accept a form info
def createAccount(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    return User().createAccount(username, email, password)


# use cookie to get user information  and form the profile
def profileInfo(request):
    cookie = request.POST.get('cookie')
    whole = request.POST.get('whole')
    return User(cookie=cookie).getProfileInfo(whole=whole)


# reset password view, compare old function firstly, and reset password if precondition is right.
def resetPassword(request):
    cookie = request.POST.get('cookie')
    oldPassword = request.POST.get('password')
    newPassword = request.POST.get('newPassword')
    return User(cookie=cookie).resetPassword(oldPassword, newPassword)


def updateProfileInfo(request):
    cookie = request.POST.get('cookie')
    username = request.POST.get('username')
    phoneNumber = request.POST.get('phoneNumber')
    email = request.POST.get('email')
    return User(cookie=cookie).updateProfileInfo(username=username, phoneNumber=phoneNumber, email=email)

# def uploadinfo(request):
#     if request.method == 'POST':
#         new_img = IMG(
#             img=request.FILES.get('img'),
#             name=request.FILES.get('img').name
#         )
#
#         new_img.save()
#
#     return render(request, 'Welcome.html')
