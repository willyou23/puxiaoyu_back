import datetime
import decimal
import uuid


from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from requests import Response

from app.models import User, PayOrder
from puxiaoyu_backend.alipayApi.alipay_custom import AliPayPageTrade


def aliPay(A):
    # 初始化支付宝接口实例

    obj = A(
        appid="2021000117640263",  # 支付宝沙箱里面的APPID，需要改成你自己的
        # app_notify_url=None,
        app_notify_url="http://localhost:8000/alipay/page2/",
        # app_notify_url=None,
        # app_notify_url='http://localhost:8080/#/profile?cookie=39203158365987335408',
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://localhost:8080/pay/success",  # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        # return_url=None,
        # return_url='http://localhost:8080/profile?cookie=39203158365987335408',
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,  # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )
    return obj


# Create your views here.
class AlipayPageTrade(View):
    cookie = ""

    def post(self, request):
        # 判断cookie是否存在
        user_cookie = request.POST.get('cookie')
        print(user_cookie)
        # print(user_cookie)
        if not user_cookie:
            return JsonResponse({"message": 1, "errmsg": "Please login"})
        self.cookie = user_cookie
        # 得到用户信息
        try:
            userinfo = User.objects.get(cookie=user_cookie)

        except User.DoesNotExist:
            return JsonResponse({"message": 2, "errmsg": "User does not exist"})

        # 初始化支付宝实例
        alipay = aliPay(AliPayPageTrade)

        # 初始化需要的数据
        money = request.POST.get("paymentMoney")
        print(type(money))# 金额，前端获取
        # print(money)
        out_trade_no = uuid.uuid4().hex  # 订单号，后台生成，需不重复
        # out_trade_no = 123139132  # 订单号，后台生成，需不重复

        subject = userinfo.username + "deposit"  # 商品名称

        # 拼接url
        query_params = alipay.direct_pay(
            subject=subject,
            out_trade_no=out_trade_no,
            total_amount=money,


        )

        # 更新数据库2
        user = User.objects.get(cookie=user_cookie)
        user.out_trade_no=out_trade_no

        user.save()
        userid = User.objects.get(id=user.id)

        payorder = PayOrder(
            out_trade_no=out_trade_no,
            order_status=0,
            subject=subject,
            user_id=userid
        )
        payorder.save()
        # #更新数据库
        #
        # user = User.objects.get(cookie=user_cookie)
        # # userid=User.objects.get(id= user.id)
        # balance = decimal.Decimal(money)
        # user.balance += balance
        # user.save()
        #
        # #更新订单数据库
        # payorder = PayOrder(
        #     # user_id=userid,
        #     subject = subject,
        #     out_trade_no=out_trade_no,
        #     pay_time=datetime.now(),
        #     order_status=1,
        #     total_amount=balance
        #
        # )
        # payorder.save()
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        return JsonResponse({"message": 3, "pay_url": pay_url})

class AlipayRedirect(View):
    # 支付宝同步回调给前台，在同步通知给后台处理

    def get(self, request):
        # return Response('后台已知晓，Over！！！')
        print('后台已知晓，Over！！！')
        data=request.GET
        print(data)
        result_data=data.dict()
        alipay = aliPay(AliPayPageTrade)
        signature = result_data.pop('sign')
        result = alipay.verify(result_data,signature)
        if result:
            print("获取数据")
            out_trade_no = result_data.get('out_trade_no', '')
            total_amount = result_data.get('total_amount','')
            pay_time = result_data.get('timestamp')
            print(pay_time)
            paytime=datetime.datetime.strptime(pay_time, "%Y-%m-%d %H:%M:%S")
            trade_no=result_data.get('trade_no')
            payorder=PayOrder.objects.get(out_trade_no=out_trade_no)
            if payorder.order_status == 1:
                print("此订单已经支付，返回数据")
                # out_trade_no = result_data.get('out_trade_no', '')
                payorder = PayOrder.objects.get(out_trade_no=out_trade_no)
                userid = payorder.user_id_id
                cookie = User.objects.get(id=userid).cookie
                return JsonResponse({"num":'3',"succmess":"Payment is Successful, Please Return to the Profile","cookie":cookie,
                                     "result": result_data})
            print("进行更新数据库")
            payorder.order_status = 1  # 支付成功
            orderstatus="Finished"
            payorder.total_amount = total_amount
            payorder.pay_time = paytime
            payorder.trade_no = trade_no


            payorder.save()
            # 更新用户账户
            id = payorder.user_id_id
            print(id)
            user1 = User.objects.get(id=id)
            cookie = user1.cookie
            print(cookie)
            print(type(total_amount))
            # print(type(user1.balance))

            total_amountnew = decimal.Decimal(total_amount)
            user1.balance +=total_amountnew


            user1.save()

            return JsonResponse({"num":'1',"succmess":"Payment is Successful, Please Return to the Profile",
                                     "result":result_data,
                                     "orderstatus":orderstatus,
                                     "cookie":cookie})

        out_trade_no = result_data.get('out_trade_no', '')
        payorder = PayOrder.objects.get(out_trade_no=out_trade_no)
        userid= payorder.user_id_id
        cookie = User.objects.get(id=userid).cookie
        return JsonResponse({"num":'2',"errmesage":"Payment Failed, Please Retry","cookie":cookie,
                             "out_trade_no":payorder.out_trade_no})
