from datetime import datetime
import decimal
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.generic.base import View

from app.models import User, PayOrder
from puxiaoyu_backend.alipayApi.alipay_custom import AliPayPageTrade


def aliPay(A):
    # 初始化支付宝接口实例

    obj = A(
        appid="2021000117640263",  # 支付宝沙箱里面的APPID，需要改成你自己的
        # app_notify_url="http://127.0.0.1:8000/profile",
        app_notify_url=None,
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        # return_url="http://localhost:8080/alipay/page2",  # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        return_url=None,
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,  # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )
    return obj


# Create your views here.
class AlipayPageTrade(View):

    def post(self, request):
        # 判断cookie是否存在
        user_cookie = request.POST.get('cookie')
        print(user_cookie)
        # print(user_cookie)
        if not user_cookie:
            return JsonResponse({"message": 1, "errmsg": "Please login"})

        # 得到用户信息
        try:
            userinfo = User.objects.get(cookie=user_cookie)

        except User.DoesNotExist:
            return JsonResponse({"message": 2, "errmsg": "User does not exist"})

        # 初始化支付宝实例
        alipay = aliPay(AliPayPageTrade)

        # 初始化需要的数据
        money = request.POST.get("paymentMoney")  # 金额，前端获取
        # print(money)
        out_trade_no = uuid.uuid4().hex  # 订单号，后台生成，需不重复
        subject = userinfo.username + "充值"  # 商品名称

        # 拼接url
        query_params = alipay.direct_pay(
            subject=subject,
            out_trade_no=out_trade_no,
            total_amount=money,
        )
        #更新数据库

        user = User.objects.get(cookie=user_cookie)
        userid=User.objects.get(id= user.id)
        balance = decimal.Decimal(money)
        user.balance += balance
        user.save()

        #更新订单数据库
        payorder = PayOrder(
            user_id=userid,
            subject = subject,
            out_trade_no=out_trade_no,
            pay_time=datetime.now(),
            order_status=1,
            total_amount=balance

        )
        payorder.save()


        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        return JsonResponse({"message": 3, "pay_url": pay_url})
#
# class AlipayRedirect(View):
#
#     def post(self, request):
#         # 更新数据库操作
#         print("/////////////")
#         money = request.POST.get('paymentMoney')
#
#         user = User.objects.get(id=1)
#         balance = decimal.Decimal(money)
#         user.balance += balance
#         print(user.balance)
#         user.save()
#         return JsonResponse({"message": 3, "balance":user.balance})

# class getBalance(View):
#
#     def Balance(self,request):
#         user_cookie=request.POST.get('cookie')
#         userinfo = User.objects.get(user_cookie= 'cookie')
#         print(userinfo)
#         return JsonResponse({"balance":userinfo.balance})

# class AliBack(View):
#     def get(self, request):
#         data = request.data
#         data.pop("sign")
#         print(data)
#         return Response({"code": 200, "msg": 'ok'})
# def page2(request):
#     alipay = aliPay(AlipayPageTrade)
#
#     if request.method == "POST":
#         # 检测是否支付成功
#         # 去请求体中获取所有返回的数据：状态/订单号
#         from urllib.parse import parse_qs
#         body_str = request.body.decode('utf-8')
#         # print(body_str)
#         post_data = parse_qs(body_str)
#         # print('支付宝给我的数据:::---------', post_data)
#         post_dict = {}
#         for k, v in post_data.items():
#             post_dict[k] = v[0]
#         print('转完之后的字典', post_dict)
#
#         sign = post_dict.pop('sign', None)
#         status = alipay.verify(post_dict, sign)
#         print('POST验证', status)
#         return HttpResponse('POST返回')
#
#     else:
#         params = request.GET.dict()
#         sign = params.pop('sign', None)
#         status = alipay.verify(params, sign)
#         print('GET验证', status)
#         return HttpResponse('支付成功')


# def update_order(request):
#     """
#     支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
#     :param request:
#     :return:
#     """
#
#     if request.method == 'POST':
#         body_str = request.body.decode('utf-8')
#         post_data = parse_qs(body_str)
#
#         post_dict = {}
#         for k, v in post_data.items():
#             post_dict[k] = v[0]
#
#         alipay = aliPay(AliPayPageTrade)
#         sign = post_dict.pop('sign', None)
#         status = alipay.verify(post_dict, sign)
#         if status:
#             # 1.修改订单状态
#             out_trade_no = post_dict.get('out_trade_no')
#             print(out_trade_no)
#             # 2. 根据订单号将数据库中的数据进行更新
#             user_cookie = request.POST.get('cookie')
#             print(user_cookie)
#
#
#
#         #     return JsonResponse({"num":3,"message":"支付成功"})
#         # else:
#         #     return JsonResponse({"nnum":4,"errmsg":"支付失败"})
#         # return HttpResponse('')
#             return HttpResponse('支付成功')
#         else:
#             return HttpResponse('支付失败')
#     return HttpResponse('支付成功')


# class AlipayRedirect(View):
#
#     def post(self, request):
#         # 更新数据库操作
#         money = request.POST.get('paymentMoney')
#         user = User.objects.get(id=1)
#         balance = decimal.Decimal(money)
#         user.balance += balance
#         user.save()
#         pass

# class CheckPayView(View):
#     def post(self, request):
#         # 用户是否登录
#         # user = request.user
#         # if not user.is_authenticated():
#         #     return JsonResponse({"res":0,"errmsg":"用户未登录"})
#         # #接收参数
#         # order_id = request.POST.get("order_id")
#         # #校验参数
#         # if not order_id:
#         #     return JsonResponse({"res":0,"errmsg":"用户未登录"})
#         # #接收参数
#         order_id = request.POST.get("order_id")
#         #
#         # #校验参数
#         # if not order_id:
#         #     return JsonResponse({"res":1,"errmsg":"无效的订单id"})
#         # try:
#         #     order = OrderInfo.objects.get(order_id=order_id,user=user,pay_method=3,order_status=1)
#         # except OrderInfo.DoesNotExist:
#         #     return JsonResponse({"res":2,"errmsg":"订单错误"})
#         # 业务处理：使用python sdk调用支付宝的支付接口
#         # 初始化
#         alipay = AliPay(
#             appid='2016092200568545',
#             app_notify_url=None,
#             alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
#             app_private_key_path=settings.APP_PRIVATE,  # 应用私钥
#             sign_type="RSA2",
#             debug=True
#         )
#         # alipay = aliPay(CheckPayView)
#         while True:
#             response = alipay.api_alipay_trade_query()
#             code = response.get("code")
#             # 如果返回码为10000和交易状态为交易支付成功
#             if code == "10000" and response.get("trade_status") == "TRADE_SUCCESS":
#                 # 支付成功
#                 # 获取支付宝交易号
#                 trade_no = response.get("trade_no")
#                 # 更新订单状态
#                 # order.trade_no = trade_no
#                 # order.order_status = 4  #待评价
#                 # order.save()
#                 return JsonResponse({"num": 3, "message": "支付成功"})
#             # 返回码为40004 或 交易状态为等待买家付款
#             elif code == "40004" or (response.get("trade_status") == "WAIT_BUYER_PAY"):
#                 # 等待买家付款
#                 # 业务处理失败，可能一会就会成功
#                 import time
#                 time.sleep(5)
#                 continue
#             else:
#                 # 支付出错
#                 return JsonResponse({"nnum": 4, "errmsg": "支付失败"})
