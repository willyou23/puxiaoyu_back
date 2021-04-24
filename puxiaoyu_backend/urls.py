"""puxiaoyu_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('login/', views.login),
    path('createAccount/', views.createAccount),
    path('profileInfo/', views.profileInfo),
    path('updateProfileInfo/', views.updateProfileInfo),
    path('resetPassword/', views.resetPassword),
    path('order/showOrder/', views.showOrder),
    path('order/confirmReceive/', views.confirmReceive),
    path('order/payment/', views.payment),
    path('order/editOrder/', views.editOrder),
    path('order/deleteOrder/', views.deleteOrder),
    path('order/createOrder/', views.createOrder),
    path('uploadGoods/', views.uploadGoods),
    path('deliverGoodsInfo/', views.deliverGoodsInfo),
    path('intialGoodsInfo/', views.intialGoodsInfo),
    path('showGoodsInfo/', views.showGoodsInfo),
    path('updateGoodsInfo/', views.updateGoodsInfo),
    path('deleteGoodsInfo/', views.deleteGoodsInfo),
]