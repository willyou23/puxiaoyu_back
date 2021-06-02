# puxiaoyu_back
CPT202 group work puxiaoyu_backend



pycharm：创建django project

在里面创建app文件夹

```
python manage.py startapp app
```

复制model和setting，仔细比对

实现跨域

```
pip install django-cors-headers
```

安装pillow，ImageField才可以运行

```
pip install pillow
```

安装mysql包

安装

```
pip install pycryptodomex
```

安装djangorestframework

```
pip install djangorestframework
```

修改setting.py

```
INSTALLED_APPS = [
······
    'rest_framework',
]

```

确保migrations内没有多余文件，除了\_\_init\_\_.py

连接数据库

运行下两条语句

```
python manage.py makemigrations
python manage.py migrate
```


