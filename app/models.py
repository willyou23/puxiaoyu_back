from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)  # 自增
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    admin = models.BooleanField(null=False)
    date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.0)
    description = models.CharField(max_length=1000, null=True)
    cookie = models.CharField(max_length=20, null=True)

    # 用户的地址存储


class Useraddr(models.Model):
    id = models.AutoField(primary_key=True)  # 自增
    address = models.CharField(max_length=100, null=True)  # 用户地址 可以多个
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)


class GoodsCategory(models.Model):
    id = models.AutoField(primary_key=True)  # 自增
    # 分类的名称 max_length 最大长度 字符串类型必须定义
    cag_name = models.CharField(max_length=30)  # 当前的变量对应的是字符串的字段 对应数据库中varchar
    # 分类的样式
    cag_css = models.CharField(max_length=20, null=True)
    # 分类的图片 当前图片存储到服务器里 （upload_to='cag'）定义存储的路径
    cag_img = models.ImageField(upload_to='cag', null=True)


# 商品表
# 模型类
class GoodsInfor(models.Model):
    # id = models.AutoField(primary_key=True)  # 自增
    # 商品的名字
    goods_name = models.CharField(max_length=100, null=True)
    # 商品的价格
    goods_price = models.IntegerField(default=0, null=True, blank=True)
    # 商品的描述
    goods_desc = models.CharField(max_length=1000, null=True)
    # 商品的图片
    # goods_img = models.ImageField(upload_to='goods')
    # goods_img = models.ForeignKey('GoodsImg',on_delete=models.DO_NOTHING)
    # 所属的分类
    goods_cag = models.ForeignKey('GoodsCategory', on_delete=models.CASCADE)
    # 商品的库存
    goods_inventory = models.IntegerField(default=1, null=True, blank=True)
    # 本商品对应的用户
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)


# 商品照片存储
class GoodsImg(models.Model):
    # 主键 id
    # id = models.AutoField(primary_key=True)
    # 图片存储路径
    img_path = models.ImageField(upload_to='goods')
    # 图片对应的商品id
    goods_id = models.ForeignKey('GoodsInfor', on_delete=models.CASCADE)
