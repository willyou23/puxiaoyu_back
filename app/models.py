from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    admin = models.BooleanField(null=False)
    date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.0)
    description = models.CharField(max_length=1000, null=True)
    cookie = models.CharField(max_length=20, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)


class GoodsCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)


class GoodsInfo(models.Model):
    id = models.AutoField(primary_key=True)
    # 商品的名字
    name = models.CharField(max_length=100, null=True)
    # 商品的价格
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    # 商品的描述
    desc = models.TextField(null=True)
    # 商品的库存
    inventory = models.IntegerField(default=1, null=True, blank=True)
    # 本商品对应的用户
    sellerId = models.ForeignKey('User', to_field="id", on_delete=models.CASCADE)
    # 所属的分类
    categoryID = models.ForeignKey('GoodsCategory', to_field="id", on_delete=models.CASCADE)
    # whether show or not
    show = models.BooleanField(default=False)
    # current tag
    tag = models.CharField(max_length=20, null=True)


class Img(models.Model):
    goodsId = models.ForeignKey('GoodsInfo', to_field="id", on_delete=models.CASCADE)
    img = models.ImageField("img", upload_to='img/', null=True, blank=True)


class OrderInfo(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    customerId = models.ForeignKey('User', to_field="id", on_delete=models.CASCADE)
    goodsId = models.ForeignKey('GoodsInfo', to_field="id", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    address = models.CharField(max_length=100, null=True)
    receiver = models.CharField(max_length=20, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    totalPrice = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    remark = models.TextField(null=True)
    paid = models.BooleanField(default=False)   # whether paid
    removal = models.BooleanField(default=False)  # whether exist, -> cancel create, remove after finished
    finished = models.BooleanField(default=False)  # whether finished -> delivery confirm
    sign = models.CharField(max_length=20, null=True)  # used in creating order


class PayOrder(models.Model):
    """订单模型"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )

    subject = models.CharField(max_length=150)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    out_trade_no = models.CharField(max_length=64, verbose_name="订单号", unique=True)
    trade_no = models.CharField(max_length=64, null=True, verbose_name="流水号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0)
    pay_time = models.DateTimeField(null=True)
    user_id = models.ForeignKey('User', to_field="id", on_delete=models.CASCADE)

